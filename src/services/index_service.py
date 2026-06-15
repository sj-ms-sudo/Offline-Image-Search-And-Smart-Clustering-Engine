import threading
import faiss
from core.config import FAISS_INDEX_PATH, EMBEDDING_DIM

_index = None
_lock = threading.Lock()

def get_index():
    global _index
    if _index is None:
        with _lock:
            if _index is None:
                if FAISS_INDEX_PATH.exists():
                    _index = faiss.read_index(str(FAISS_INDEX_PATH))
                else:
                    _index = faiss.IndexFlatL2(EMBEDDING_DIM)
    return _index

def save_index():
    if _index is not None:
        faiss.write_index(_index, str(FAISS_INDEX_PATH))

def reset_index():
    global _index
    with _lock:
        _index = faiss.IndexFlatL2(EMBEDDING_DIM)
        faiss.write_index(_index, str(FAISS_INDEX_PATH))

def unload_index():
    global _index
    with _lock:
        _index = None

def add_embedding(embedding):
    idx = get_index()
    faiss.normalize_L2(embedding.reshape(1, -1))
    idx.add(embedding.reshape(1, -1))

def search_embedding(embedding, k=1):
    idx = get_index()
    faiss.normalize_L2(embedding.reshape(1, -1))
    return idx.search(embedding.reshape(1, -1), k=k)