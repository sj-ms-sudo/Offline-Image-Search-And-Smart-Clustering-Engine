from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import PHOTOS_DIR, ALLOWED_ORIGINS
from api.routes import stats, files, embeddings, clusters

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=PHOTOS_DIR), name="images")

app.include_router(stats.router)
app.include_router(files.router)
app.include_router(embeddings.router)
app.include_router(clusters.router)


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.post("/database/sync")
def sync_database():
    from backend.database import create_tables
    return {"message": create_tables()}