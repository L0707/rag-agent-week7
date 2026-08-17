from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
RESULTS_DIR = ROOT_DIR / "results"
VECTOR_STORE_DIR = ROOT_DIR / "vector_store"

INDEX_PATH = VECTOR_STORE_DIR / "rag_index.pkl"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.csv"


def ensure_dirs():
    for directory in [DATA_DIR, DOCS_DIR, RESULTS_DIR, VECTOR_STORE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

