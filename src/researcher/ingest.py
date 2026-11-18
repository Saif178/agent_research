"""Index PDF papers into a local ChromaDB collection for retrieval."""
from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader
import chromadb

from .config import CHROMA_PATH


def chunks(text: str, size: int = 1200, overlap: int = 180):
    text = " ".join(text.split())
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunk = text[start:end].strip()
        if chunk:
            yield chunk
        if end == len(text):
            break
        start = end - overlap


def ingest_pdf(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection("research_papers")
    ids, docs, metas = [], [], []
    for page_no, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        for chunk_no, chunk in enumerate(chunks(page_text)):
            ids.append(f"{pdf_path.stem}-p{page_no}-c{chunk_no}")
            docs.append(chunk)
            metas.append({"source": pdf_path.name, "page": page_no})
    if docs:
        collection.upsert(ids=ids, documents=docs, metadatas=metas)
    return len(docs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="PDF file or directory containing PDFs")
    args = parser.parse_args()
    path = Path(args.pdf)
    pdfs = list(path.glob("*.pdf")) if path.is_dir() else [path]
    total = 0
    for pdf in pdfs:
        if pdf.exists() and pdf.suffix.lower() == ".pdf":
            count = ingest_pdf(pdf)
            print(f"{pdf.name}: indexed {count} text chunks")
            total += count
    print(f"Total indexed chunks: {total}")


if __name__ == "__main__":
    main()
