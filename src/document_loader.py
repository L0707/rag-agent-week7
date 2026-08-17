from pathlib import Path

from pypdf import PdfReader


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def load_documents(docs_dir: Path):
    documents = []
    supported_suffixes = {".md", ".txt", ".pdf"}

    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in supported_suffixes:
            continue

        if path.suffix.lower() == ".pdf":
            text = read_pdf_file(path)
        else:
            text = read_text_file(path)

        documents.append({
            "source": str(path.relative_to(docs_dir.parent)),
            "text": text,
        })

    return documents


def chunk_text(text: str, chunk_size: int = 450, overlap: int = 80):
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks

