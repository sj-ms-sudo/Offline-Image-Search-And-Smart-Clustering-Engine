from fastapi import APIRouter, BackgroundTasks
from services.pipeline_service import (
    run_embedding_pipeline,
    get_embedding_progress,
)
from services.index_service import get_index, reset_index

router = APIRouter()


@router.post("/indexing")
def create_faiss_index():
    reset_index()
    return {"message": "Faiss index created"}


@router.post("/embeddings")
async def create_face_embeddings(background_tasks: BackgroundTasks):
    # Lazily ensures index file exists; no heavy load yet
    get_index()
    background_tasks.add_task(run_embedding_pipeline)
    return {"message": "Embedding process started"}


@router.get("/embeddings/status")
def get_embeddings_status():
    return {"progress": get_embedding_progress()}