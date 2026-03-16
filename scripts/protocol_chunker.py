import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ProtocolChunk:
    chunk_id: str
    section_title: str
    text: str


SECTION_PATTERN = re.compile(r"^(?:\d+(?:\.\d+)*)\s+.+$", re.MULTILINE)


def chunk_protocol(protocol_text: str) -> List[ProtocolChunk]:
    matches = list(SECTION_PATTERN.finditer(protocol_text))
    chunks: List[ProtocolChunk] = []

    if not matches:
        return [
            ProtocolChunk(
                chunk_id="chunk_001",
                section_title="FULL_DOCUMENT",
                text=protocol_text.strip(),
            )
        ]

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(protocol_text)
        block = protocol_text[start:end].strip()
        lines = block.splitlines()
        title = lines[0].strip()
        text = "\n".join(lines[1:]).strip()

        chunks.append(
            ProtocolChunk(
                chunk_id=f"chunk_{i+1:03d}",
                section_title=title,
                text=text,
            )
        )

    return chunks


def load_protocol(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


if __name__ == "__main__":
    protocol = load_protocol("data/sample_inputs/sample_protocol.txt")
    chunks = chunk_protocol(protocol)

    for chunk in chunks[:5]:
        print("=" * 60)
        print(chunk.chunk_id)
        print(chunk.section_title)
        print(chunk.text[:300])
