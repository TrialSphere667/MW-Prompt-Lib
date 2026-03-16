import re
from pathlib import Path

from protocol_dependency_lookup import (
    parse_dependency_file,
    build_dependency_guidance_block,
)


ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
KNOWLEDGE_DIR = ROOT / "knowledge"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def extract_primary_category(classification_output: str) -> str | None:
    """
    Extract the primary category from model output like:
    - Primary Change Category: Inclusion Criteria
    """
    match = re.search(
        r"Primary Change Category:\s*(.+)",
        classification_output,
        flags=re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()
    return None


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    print("=== Amendment Impact Pipeline Runner ===")

    amendment_path = input("Path to amendment change text file: ").strip()
    amendment_change = Path(amendment_path).read_text(encoding="utf-8").strip()

    # Step 1: Build and print classifier prompt
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

    # Step 2: Dependency lookup
    dependency_file = KNOWLEDGE_DIR / "protocol_section_dependencies.md"
    dependency_map = parse_dependency_file(dependency_file)
    dependency_guidance = build_dependency_guidance_block(
        primary_category,
        dependency_map,
    )

    print("\n=== STEP 2: DEPENDENCY GUIDANCE ===\n")
    print(dependency_guidance)

    # Step 3: Build and print impact discovery prompt
    impact_prompt = build_impact_discovery_prompt(
        amendment_change=amendment_change,
        dependency_guidance=dependency_guidance,
    )

    print("\n=== STEP 3: COPY THIS INTO YOUR WORD TOOL FOR IMPACT DISCOVERY ===\n")
    print(impact_prompt)
    print("\n=== END IMPACT DISCOVERY PROMPT ===\n")

    # Optional: save artifacts
    save_dir = ROOT / "data" / "pipeline_outputs"
    save_text(save_dir / "latest_amendment_change.txt", amendment_change)
    save_text(save_dir / "latest_classification_output.txt", classification_output)
    save_text(save_dir / "latest_dependency_guidance.txt", dependency_guidance)
    save_text(save_dir / "latest_impact_discovery_prompt.txt", impact_prompt)

    print("\nSaved pipeline artifacts to:")
    print(save_dir)


if __name__ == "__main__":
    main()
