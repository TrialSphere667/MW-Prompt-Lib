from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_classifier_prompt(amendment_change: str) -> str:
    template = load_text(PROMPTS_DIR / "amendment_change_classifier.md")
    return template.replace("[INSERT AMENDMENT CHANGE HERE]", amendment_change)


def main() -> None:
    print("=== Amendment Change Classification Runner ===")
    amendment_path = input("Path to amendment change text file: ").strip()
    amendment_change = Path(amendment_path).read_text(encoding="utf-8").strip()

    final_prompt = build_classifier_prompt(amendment_change)

    print("\n=== COPY THIS INTO YOUR WORD TOOL ===\n")
    print(final_prompt)
    print("\n=== END PROMPT ===")


if __name__ == "__main__":
    main()
