from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from services.pipeline_service import (
    run_clustering_pipeline,
    get_cluster_progress,
)
from backend.database import get_all_clusters_from_database, update_name_in_cluster, get_images_by_cluster
class ClusterRenameRequest(BaseModel):
    cluster_id:int
    name:str

router = APIRouter()


@router.post("/clusters")
async def create_face_clusters(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_clustering_pipeline)
    return {"message": "Cluster process started"}


@router.get("/clusters/status")
def get_cluster_status():
    return {"progress": get_cluster_progress()}

# Get all clusters with 4 images as limit
@router.get("/clusters/all")
def get_all_clusters():
    return get_all_clusters_from_database()

@router.patch("/clusters/editName")
def edit_cluster_name(data:ClusterRenameRequest):
    cluster_id = data.cluster_id
    name = data.name
    update_name_in_cluster(cluster_id,name)

@router.get("/clusters/{id}")
def get_cluster_by_id(id:int):
    return get_images_by_cluster(id)
