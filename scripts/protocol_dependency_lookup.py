import re
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def parse_dependency_file(file_path: Path) -> Dict[str, List[str]]:
    """
    Parse the protocol_section_dependencies.md file into a dictionary like:
    {
        "eligibility criteria": ["inclusion criteria", "exclusion criteria", ...],
        ...
    }
    """
    text = load_text(file_path)

    dependency_map: Dict[str, List[str]] = {}
    current_section: Optional[str] = None
    current_items: List[str] = []

    lines = text.splitlines()

    for raw_line in lines:
        line = raw_line.strip()

        # Match section headings like: # 3. Eligibility Criteria
        heading_match = re.match(r"^#+\s+\d+\.\s+(.+)$", line)
        if heading_match:
            if current_section and current_items:
                dependency_map[current_section] = current_items

            current_section = normalize_heading(heading_match.group(1))
            current_items = []
            continue

        # Match dependency bullets
        bullet_match = re.match(r"^- (.+)$", line)
        if bullet_match and current_section:
            current_items.append(bullet_match.group(1).strip())

    if current_section and current_items:
        dependency_map[current_section] = current_items

    return dependency_map


def get_review_areas(
    category: str,
    dependency_map: Dict[str, List[str]]
) -> List[str]:
    key = normalize_heading(category)
    return dependency_map.get(key, [])


def build_dependency_guidance_block(
    category: str,
    dependency_map: Dict[str, List[str]]
) -> str:
    review_areas = get_review_areas(category, dependency_map)

    if not review_areas:
        return (
            f"No dependency guidance found for category: {category}\n"
            f"Use general domain reasoning and flag uncertain areas for review."
        )

    bullet_block = "\n".join(f"- {item}" for item in review_areas)
    return f"{category} may affect:\n{bullet_block}"


def main() -> None:
    dependency_file = KNOWLEDGE_DIR / "protocol_section_dependencies.md"
    dependency_map = parse_dependency_file(dependency_file)

    print("=== Protocol Dependency Lookup ===")
    category = input("Enter amendment category: ").strip()

    guidance = build_dependency_guidance_block(category, dependency_map)

    print("\n=== Dependency Guidance ===\n")
    print(guidance)


if __name__ == "__main__":
    main()
