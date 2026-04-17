from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocumentChunk:
    doc_id: str
    chunk_id: str
    text: str
    source_path: str



def load_text_files(directory: Path) -> list[tuple[str, str]]:
    files = sorted([p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md"}])
    results: list[tuple[str, str]] = []
    for file_path in files:
        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        if content:
            results.append((str(file_path), content))
    return results



def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    normalized = " ".join(text.split())
    if len(normalized) <= chunk_size:
        return [normalized]

    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start = max(0, end - overlap)
    return chunks



def build_chunks(directory: Path, chunk_size: int = 800, overlap: int = 120) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for source_path, content in load_text_files(directory):
        doc_id = Path(source_path).stem
        parts = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
        for index, part in enumerate(parts):
            chunks.append(
                DocumentChunk(
                    doc_id=doc_id,
                    chunk_id=f"{doc_id}-{index}",
                    text=part,
                    source_path=source_path,
                )
            )
    return chunks
