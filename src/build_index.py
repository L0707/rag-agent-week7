import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from config import CHUNKS_PATH, DOCS_DIR, INDEX_PATH, ensure_dirs
from document_loader import chunk_text, load_documents


def build_index():
    ensure_dirs()

    documents = load_documents(DOCS_DIR)
    if not documents:
        raise RuntimeError(f"No documents found in {DOCS_DIR}")

    rows = []
    for document in documents:
        chunks = chunk_text(document["text"])
        for chunk_id, chunk in enumerate(chunks):
            rows.append({
                "source": document["source"],
                "chunk_id": chunk_id,
                "text": chunk,
            })

    chunks_df = pd.DataFrame(rows)
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(chunks_df["text"].tolist())

    payload = {
        "vectorizer": vectorizer,
        "matrix": matrix,
        "chunks": chunks_df.to_dict(orient="records"),
    }

    with INDEX_PATH.open("wb") as f:
        pickle.dump(payload, f)

    chunks_df.to_csv(CHUNKS_PATH, index=False, encoding="utf-8-sig")

    print("RAG index built.")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks_df)}")
    print(f"Index saved to: {INDEX_PATH}")
    print(f"Chunks saved to: {CHUNKS_PATH}")


if __name__ == "__main__":
    build_index()

