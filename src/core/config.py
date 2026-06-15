from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PHOTOS_DIR = (BASE_DIR / "../photos").resolve()
OUTPUT_DIR = (BASE_DIR / "../output").resolve()
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
FAISS_INDEX_PATH = BASE_DIR / "faces.index"
EMBEDDING_DIM = 512

ALLOWED_ORIGINS = ["http://localhost:5173","https://offline-image-search-and-smart-clustering-engine-12721sqx5.vercel.app/"]

PHOTOS_DIR.mkdir(exist_ok=True, parents=True)