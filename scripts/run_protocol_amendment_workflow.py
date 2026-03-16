from pathlib import Path

from protocol_retriever import retrieve_relevant_chunks
from protocol_chunker import load_protocol


ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def build_amendment_prompt(amendment_change: str, candidate_passages: str) -> str:
    prompt_template = load_text(PROMPTS_DIR / "protocol_amendment_assistant.md")
    prompt = prompt_template.replace("[INSERT AMENDMENT CHANGE HERE]", amendment_change)
    prompt = prompt.replace("[INSERT RETRIEVED PROTOCOL PASSAGES HERE]", candidate_passages)
    return prompt


def main() -> None:
    print("=== Protocol Amendment Workflow Runner ===")
    amendment_path = input("Path to amendment change text file: ").strip()
    protocol_path = input("Path to protocol text file: ").strip()
    top_k = int(input("Number of protocol chunks to retrieve (e.g. 5): ").strip())

    amendment_change = load_text(Path(amendment_path)).strip()
    protocol_text = load_protocol(protocol_path)

    results = retrieve_relevant_chunks(amendment_change, protocol_text, top_k=top_k)
    candidate_passages = build_candidate_passage_block(results)
    final_prompt = build_amendment_prompt(amendment_change, candidate_passages)

    print("\n=== TOP RETRIEVED PASSAGES ===\n")
    print(candidate_passages)

    print("\n=== COPY THIS INTO YOUR WORD TOOL ===\n")
    print(final_prompt)
    print("\n=== END PROMPT ===")


if __name__ == "__main__":
    main()
