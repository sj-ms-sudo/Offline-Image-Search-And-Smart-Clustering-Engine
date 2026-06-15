from fastapi import APIRouter, BackgroundTasks
from services.pipeline_service import (
    run_clustering_pipeline,
    get_cluster_progress,
)
from backend.database import get_all_clusters_from_database

router = APIRouter()


@router.post("/clusters")
async def create_face_clusters(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_clustering_pipeline)
    return {"message": "Cluster process started"}


@router.get("/clusters/status")
def get_cluster_status():
    return {"progress": get_cluster_progress()}


@router.get("/clusters/all")
def get_all_clusters():
    return get_all_clusters_from_database()