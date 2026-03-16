import re
from typing import List, Tuple

from protocol_chunker import ProtocolChunk, chunk_protocol, load_protocol


STOPWORDS = {
    "the", "and", "or", "of", "to", "for", "in", "on", "with", "a", "an",
    "is", "are", "be", "by", "from", "that", "this", "as", "at", "it",
    "updated", "change"
}


def tokenize(text: str) -> List[str]:
    words = re.findall(r"[A-Za-z0-9\-]+", text.lower())
    return [w for w in words if w not in STOPWORDS]


def score_chunk(change_text: str, chunk: ProtocolChunk) -> float:
    change_terms = set(tokenize(change_text))
    section_terms = set(tokenize(chunk.section_title))
    body_terms = set(tokenize(chunk.text))

    title_overlap = len(change_terms & section_terms)
    body_overlap = len(change_terms & body_terms)

    # Boost section-title matches because they are often more meaningful
    score = (title_overlap * 2.5) + body_overlap

    # Small boost for especially relevant keywords
    keyword_boost_terms = {
        "eligibility", "inclusion", "exclusion", "endpoint", "safety",
        "population", "dose", "dosing", "schedule", "assessment",
        "statistics", "analysis", "renal", "hepatic", "biomarker"
    }
    if change_terms & keyword_boost_terms and (section_terms & keyword_boost_terms):
        score += 1.5

    return score


def retrieve_relevant_chunks(
    change_text: str,
    protocol_text: str,
    top_k: int = 5
) -> List[Tuple[ProtocolChunk, float]]:
    chunks = chunk_protocol(protocol_text)
    scored = []

    for chunk in chunks:
        score = score_chunk(change_text, chunk)
        if score > 0:
            scored.append((chunk, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    amendment_change = "Inclusion criteria updated to allow patients with mild renal impairment."
    protocol = load_protocol("data/sample_inputs/sample_protocol.txt")

    results = retrieve_relevant_chunks(amendment_change, protocol, top_k=5)

    for chunk, score in results:
        print("=" * 60)
        print(f"Score: {score}")
        print(f"{chunk.chunk_id} | {chunk.section_title}")
        print(chunk.text[:400])
