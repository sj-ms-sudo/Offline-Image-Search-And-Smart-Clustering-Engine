
from detector.detector import create_detector
from utils.image_utils import create_index
from utils.image_utils import find_matching_images
from utils.image_utils import create_embeddings
from backend.database import create_tables
from utils.image_utils import create_clusters
from utils.image_utils import show_clusters
from backend.database import get_stats_from_database
from fastapi import FastAPI,UploadFile,File,HTTPException,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import faiss
from utils.path_utils import clear_system_data
from utils.image_utils import save_uploaded_file, get_embedding_progress, get_cluster_progress
from backend.database import get_all_clusters_from_database


app = FastAPI()

# Initialize detector at startup so it's available for the background tasks
detector = create_detector()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
PHOTOS_DIR = Path("../photos").resolve()
PHOTOS_DIR.mkdir(exist_ok=True)
app.mount("/images", StaticFiles(directory=PHOTOS_DIR), name="images")
@app.get("/")
def home():
    return {
        "message":"Hello World"
    }
@app.get("/stats")
def get_stats():
    return get_stats_from_database()

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    PHOTOS_DIR = Path("../photos")
    PHOTOS_DIR.mkdir(exist_ok=True)
    
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a valid image.")
            
        file_path = PHOTOS_DIR / file.filename
        save_uploaded_file(file, file_path)
        
        
    return {"message": f"Successfully uploaded {len(files)} file(s)"}

@app.post("/database/sync")
def sync_database():
    message = create_tables()
    return{
        "message" : message
    }

@app.post("/indexing")
def create_faiss_index():
    message = create_index()
    return {
        "message" : message
    }

@app.post("/embeddings")
async def create_face_embeddings(background_tasks: BackgroundTasks):
    try:
        faiss_index = faiss.read_index("faces.index")
    except:
        raise HTTPException(status_code=404, detail="FAISS index not found")
    
    background_tasks.add_task(create_embeddings, detector, faiss_index)
    
    return {
        "message": "Embedding process started"
    }

@app.get("/embeddings/status")
def get_embeddings_status():
    return {
        "progress": get_embedding_progress()
    }
@app.post("/clusters")
async def create_face_clusters(background_tasks: BackgroundTasks):
    background_tasks.add_task(create_clusters)
    return {
        "message":"Cluster process started"
    }
@app.get("/clusters/status")
def get_cluster_status():
    return {
        "progress": get_cluster_progress()
    }

@app.delete("/files")
def delete_files():
    try:
        clear_system_data()
        return {"message": "All pipeline data cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clusters/all")
def get_all_clusters():
    return get_all_clusters_from_database()


if __name__ == "__main__":
    main()
