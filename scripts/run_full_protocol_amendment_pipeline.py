import re
from pathlib import Path
from typing import List, Optional

from protocol_dependency_lookup import (
    parse_dependency_file,
    build_dependency_guidance_block,
)
from protocol_retriever import retrieve_relevant_chunks
from protocol_chunker import load_protocol


ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
KNOWLEDGE_DIR = ROOT / "knowledge"
OUTPUT_DIR = ROOT / "data" / "pipeline_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_classifier_prompt(amendment_change: str) -> str:
    template = load_text(PROMPTS_DIR / "amendment_change_classifier.md")
    return template.replace("[INSERT AMENDMENT CHANGE HERE]", amendment_change)


def build_impact_discovery_prompt(
    amendment_change: str,
    dependency_guidance: str,
) -> str:
    template = load_text(PROMPTS_DIR / "amendment_impact_discovery.md")
    prompt = template.replace("[INSERT AMENDMENT CHANGE HERE]", amendment_change)
    prompt = prompt.replace(
        "[INSERT PROTOCOL DEPENDENCY GUIDANCE HERE]",
        dependency_guidance,
    )
    return prompt


def build_protocol_amendment_prompt(
    amendment_change: str,
    candidate_passages: str,
) -> str:
    template = load_text(PROMPTS_DIR / "protocol_amendment_assistant.md")
    prompt = template.replace("[INSERT AMENDMENT CHANGE HERE]", amendment_change)
    prompt = prompt.replace(
        "[INSERT RETRIEVED PROTOCOL PASSAGES HERE]",
        candidate_passages,
    )
    return prompt


def extract_primary_category(classification_output: str) -> Optional[str]:
    match = re.search(
        r"Primary Change Category:\s*(.+)",
        classification_output,
        flags=re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()
    return None


def extract_review_areas(impact_output: str) -> List[str]:
    """
    Extract numbered or bulleted review areas from the
    'Recommended Protocol Areas for Review' section if present.
    Falls back to empty list if not found.
    """
    lines = impact_output.splitlines()
    areas: List[str] = []
    capture = False

    for raw_line in lines:
        line = raw_line.strip()

        if re.search(r"Recommended Protocol Areas for Review", line, re.IGNORECASE):
            capture = True
            continue

        if capture:
            if not line:
                continue

            # Stop if a new markdown section starts
            if line.startswith("##") or line.startswith("#"):
                break

            numbered = re.match(r"^\d+\.\s+(.+)$", line)
            bulleted = re.match(r"^- (.+)$", line)

            if numbered:
                areas.append(numbered.group(1).strip())
            elif bulleted:
                areas.append(bulleted.group(1).strip())

    return areas


def build_retrieval_query(amendment_change: str, review_areas: List[str]) -> str:
    """
    Build a retrieval query from the amendment change and review areas.
    """
    if review_areas:
        return amendment_change + " " + " ".join(review_areas)
    return amendment_change


def build_candidate_passage_block(results) -> str:
    blocks = []
    for chunk, score in results:
        blocks.append(
            f"Passage ID: {chunk.chunk_id}\n"
            f"Section: {chunk.section_title}\n"
            f"Relevance Score: {score}\n"
            f"Text:\n{chunk.text}\n"
        )
    return "\n---\n".join(blocks)


def main() -> None:
    print("=== Full Protocol Amendment Pipeline Runner ===")

    amendment_path = input("Path to amendment change text file: ").strip()
    protocol_path = input("Path to protocol text file: ").strip()
    top_k = int(input("Number of protocol chunks to retrieve (e.g. 5): ").strip())

    amendment_change = Path(amendment_path).read_text(encoding="utf-8").strip()
    protocol_text = load_protocol(protocol_path)

    # --------------------------------------------------
    # STEP 1: Build and run classification prompt
    # --------------------------------------------------
    classifier_prompt = build_classifier_prompt(amendment_change)

    print("\n=== STEP 1: COPY THIS INTO YOUR WORD TOOL FOR CLASSIFICATION ===\n")
    print(classifier_prompt)
    print("\n=== END CLASSIFICATION PROMPT ===\n")

    classification_output = input(
        "\nPaste the classification output here, then press Enter:\n"
    ).strip()

    primary_category = extract_primary_category(classification_output)
    if not primary_category:
        print(
            "\nCould not automatically extract the Primary Change Category."
            "\nPlease enter it manually."
        )
        primary_category = input("Primary Change Category: ").strip()

    # --------------------------------------------------
    # STEP 2: Dependency lookup
    # --------------------------------------------------
    dependency_file = KNOWLEDGE_DIR / "protocol_section_dependencies.md"
    dependency_map = parse_dependency_file(dependency_file)
    dependency_guidance = build_dependency_guidance_block(
        primary_category,
        dependency_map,
    )

    print("\n=== STEP 2: DEPENDENCY GUIDANCE ===\n")
    print(dependency_guidance)

    # --------------------------------------------------
    # STEP 3: Build and run impact discovery prompt
    # --------------------------------------------------
    impact_prompt = build_impact_discovery_prompt(
        amendment_change=amendment_change,
        dependency_guidance=dependency_guidance,
    )

    print("\n=== STEP 3: COPY THIS INTO YOUR WORD TOOL FOR IMPACT DISCOVERY ===\n")
    print(impact_prompt)
    print("\n=== END IMPACT DISCOVERY PROMPT ===\n")

    impact_output = input(
        "\nPaste the impact discovery output here, then press Enter:\n"
    ).strip()

    review_areas = extract_review_areas(impact_output)

    print("\n=== STEP 4: EXTRACTED REVIEW AREAS ===\n")
    if review_areas:
        for idx, area in enumerate(review_areas, start=1):
            print(f"{idx}. {area}")
    else:
        print("No explicit review areas extracted; using amendment change only.")

    # --------------------------------------------------
    # STEP 4: Protocol retrieval
    # --------------------------------------------------
    retrieval_query = build_retrieval_query(amendment_change, review_areas)
    retrieval_results = retrieve_relevant_chunks(
        change_text=retrieval_query,
        protocol_text=protocol_text,
        top_k=top_k,
    )

    candidate_passages = build_candidate_passage_block(retrieval_results)

    print("\n=== STEP 5: RETRIEVED PROTOCOL PASSAGES ===\n")
    print(candidate_passages)

    # --------------------------------------------------
    # STEP 5: Build final revision prompt
    # --------------------------------------------------
    revision_prompt = build_protocol_amendment_prompt(
        amendment_change=amendment_change,
        candidate_passages=candidate_passages,
    )

    print("\n=== STEP 6: COPY THIS INTO YOUR WORD TOOL FOR REVISION SUGGESTIONS ===\n")
    print(revision_prompt)
    print("\n=== END REVISION PROMPT ===\n")

    # --------------------------------------------------
    # Save artifacts
    # --------------------------------------------------
    save_text(OUTPUT_DIR / "latest_amendment_change.txt", amendment_change)
    save_text(OUTPUT_DIR / "latest_classification_output.txt", classification_output)
    save_text(OUTPUT_DIR / "latest_dependency_guidance.txt", dependency_guidance)
    save_text(OUTPUT_DIR / "latest_impact_discovery_output.txt", impact_output)
    save_text(OUTPUT_DIR / "latest_retrieval_query.txt", retrieval_query)
    save_text(OUTPUT_DIR / "latest_candidate_passages.txt", candidate_passages)
    save_text(OUTPUT_DIR / "latest_revision_prompt.txt", revision_prompt)

    print("\nSaved pipeline artifacts to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
