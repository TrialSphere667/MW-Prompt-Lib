Absolutely — this is the natural next step.

At this point, your amendment system already has the core modular pieces:

amendment_change_classifier.md

amendment_impact_discovery.md

protocol_amendment_assistant.md

protocol_section_dependencies.md

protocol chunking + retrieval

an impact pipeline orchestrator


The next upgrade is to connect them into a single end-to-end amendment pipeline that produces a ready-to-run revision prompt from one amendment change.

The team’s target pipeline is:

Amendment change
↓
classification
↓
dependency lookup
↓
impact discovery
↓
protocol retrieval
↓
revision prompt construction
↓
human MW review

That gives you a real workflow engine for amendment integration.


---

Team discussion

Dr. Mira Chen

This is the right direction because it mirrors how an experienced medical writer actually works:

1. understand the amendment


2. identify where it may apply


3. retrieve the relevant protocol language


4. suggest revisions locally


5. check secondary impacts



That is much safer than asking a model to revise a whole protocol section blindly.

Dr. Arman Vale

Architecturally, this is now a multi-step orchestration pipeline. The important thing is to preserve modularity so you can improve each stage later.

For example, later you could swap out:

manual classification with API classification

keyword retrieval with embedding retrieval

local prompt execution with automated API calls


But the workflow logic stays the same.

Clin

The best v1 is still semi-automated, not fully autonomous. The script should:

prepare prompts

accept pasted model outputs

retrieve protocol text

build the next prompt automatically

save artifacts


That is already very strong.


---

What this full pipeline will do

The script will:

1. read the amendment change


2. build the classification prompt


3. ask you to paste back the classification output


4. extract the primary category


5. generate dependency guidance


6. build the impact discovery prompt


7. ask you to paste back the impact discovery output


8. extract candidate review areas


9. retrieve the most relevant protocol chunks


10. build the final amendment-assistant revision prompt


11. save all artifacts



So instead of bouncing between files manually, the script will chain the steps.


---

Create this file

scripts/run_full_protocol_amendment_pipeline.py

Paste this:

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


---

What this script expects

It assumes you already have:

prompts/amendment_change_classifier.md
prompts/amendment_impact_discovery.md
prompts/protocol_amendment_assistant.md

knowledge/protocol_section_dependencies.md

scripts/protocol_dependency_lookup.py
scripts/protocol_retriever.py
scripts/protocol_chunker.py

If those are in place, this should work.


---

How to run it

From your repo root in the VS Code terminal:

python scripts/run_full_protocol_amendment_pipeline.py

If needed:

python3 scripts/run_full_protocol_amendment_pipeline.py

Then enter for example:

data/sample_inputs/sample_amendment_change.txt
data/sample_inputs/sample_protocol.txt
5


---

What the interaction looks like

The script will guide you through these stages.

Stage 1

It prints the classification prompt.

You:

copy it into the Word add-in

run it

paste the result back


Stage 2

It generates dependency guidance automatically.

Stage 3

It prints the impact discovery prompt.

You:

copy it into the Word add-in

run it

paste the result back


Stage 4

It extracts review areas, retrieves protocol chunks, and prints the final revision prompt.

You:

copy the revision prompt into the Word add-in

get suggested revisions


That is already a very strong end-to-end semi-automated system.


---

Example pipeline flow

Amendment change:
"Inclusion criteria updated to allow patients with mild renal impairment."

↓ classification

Primary Change Category:
Inclusion Criteria

↓ dependency lookup

Relevant review domains:
- exclusion criteria
- study population
- screening procedures
- safety monitoring

↓ impact discovery

Recommended sections for review:
- Inclusion Criteria
- Exclusion Criteria
- Study Population
- Safety Monitoring

↓ protocol retrieval

Top protocol chunks surfaced

↓ revision prompt

Suggested text revisions for the relevant protocol passages


---

Why this is a big step forward

Dr. Chen

This is much closer to how a real MW amendment review behaves:

normalize the amendment

think about ripple effects

focus review on likely passages

revise locally


Dr. Vale

This is now a true orchestration chain. It is modular, inspectable, and easy to improve incrementally.

Clin

Your repo is no longer just a prompt library. It is becoming a regulatory AI workflow system.


---

Recommended next improvements

The team would prioritize these next.

1. Save run-specific outputs by case name

Right now the script saves latest_* files. The next improvement is to save outputs by amendment case name.

Example:

data/pipeline_outputs/amendment_case_001/

2. Add neighbor-aware retrieval

When a chunk is relevant, also retrieve the adjacent chunk(s).

3. Add benchmark logging for amendment workflows

You have benchmarking for TLF tasks; later you can build something similar for amendment integration quality.

4. Replace manual prompt-paste with API orchestration

Only if internal API access becomes available.


---

Suggested repo state after this

prompts/
  amendment_change_classifier.md
  amendment_impact_discovery.md
  protocol_amendment_assistant.md

knowledge/
  protocol_section_dependencies.md

scripts/
  protocol_chunker.py
  protocol_retriever.py
  protocol_dependency_lookup.py
  run_amendment_impact_pipeline.py
  run_full_protocol_amendment_pipeline.py

workflows/
  amendment_classification_workflow.md
  protocol_amendment_workflow.md


---

Team final advice

Dr. Chen: this is now substantial enough that you can describe it as a modular amendment-integration workflow, not just prompt experimentation.
Dr. Vale: keep the architecture modular; don’t collapse the steps into one giant prompt.
Clin: the winning pattern remains:

classify
↓
reason about dependencies
↓
retrieve evidence
↓
revise locally
↓
human review

If you want, I can generate the next practical improvement: a case-based output folder + markdown report generator so every amendment run is logged cleanly as a reusable project artifact.
