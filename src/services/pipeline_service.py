from pathlib import Path
import numpy as np
import cv2 as cv
import faiss

from core.config import PHOTOS_DIR, EMBEDDINGS_DIR
from services.face_service import detect_faces, unload_detector
from services.index_service import get_index, save_index, add_embedding
from backend.database import (
    save_image_to_database,
    save_faces_to_database,
    save_embeddings_to_database,
    get_image_path_by_embeddings,
    add_cluster_to_database,
    clear_clusters,
)
from utils.path_utils import get_image_files, create_output_path, return_embeddings
from sklearn.cluster import DBSCAN

embedding_progress = {"current": 0, "total": 0, "status": "idle"}
cluster_progress = {"current": 0, "total": 0, "status": "idle"}


def get_embedding_progress():
    return embedding_progress


def get_cluster_progress():
    return cluster_progress


def _save_embedding_file(face, face_id):
    EMBEDDINGS_DIR.mkdir(exist_ok=True)
    path = EMBEDDINGS_DIR / f"{face_id}.npy"
    np.save(path, face.embedding)
    return path


def run_embedding_pipeline():
    global embedding_progress
    images = get_image_files(str(PHOTOS_DIR)) or []
    total = len(images)
    embedding_progress.update(current=0, total=total, status="processing")

    try:
        for i, image_path in enumerate(images, start=1):
            embedding_progress["current"] = i
            image = cv.imread(str(image_path))
            if image is None:
                continue

            image_id = save_image_to_database(image_path)
            if image_id is None:
                continue

            faces = detect_faces(image)
            if not faces:
                continue

            for face in faces:
                face_id = save_faces_to_database(face, image_id)
                emb_path = _save_embedding_file(face, face_id)
                save_embeddings_to_database(face_id, emb_path)
                add_embedding(face.embedding)

            for face in faces:
                x1, y1, x2, y2 = face.bbox.astype(int)
                cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            output_path = create_output_path(image_path)
            cv.imwrite(str(output_path), image)

        save_index()
        embedding_progress["status"] = "completed"
    finally:
        # Free ~1-2GB RAM held by the detection model after the batch job
        unload_detector()

    return "Embeddings created"


def run_clustering_pipeline():
    global cluster_progress
    embeddings = return_embeddings()
    cluster_progress.update(current=0, total=embeddings.shape[0], status="processing")

    clear_clusters()
    db = DBSCAN(eps=0.5, min_samples=3, metric="cosine")
    labels = db.fit_predict(embeddings)

    for index, label in enumerate(labels):
        cluster_progress["current"] = index
        if label == -1:
            continue
        face_data = get_image_path_by_embeddings(index)
        if face_data is None:
            continue
        add_cluster_to_database(label, face_data)

    cluster_progress["status"] = "completed"
    return "Clusters created"