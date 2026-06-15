import cv2 as cv
from pathlib import Path
import numpy as np
import faiss
from detector.detector import detect_faces
from backend.database import show_nearest_images
from utils.path_utils import get_image_files
from backend.database import save_image_to_database
from backend.database import save_faces_to_database
from backend.database import save_embeddings_to_database
from utils.path_utils import create_output_path
from utils.path_utils import return_embeddings
from sklearn.cluster import DBSCAN
from backend.database import get_image_path_by_embeddings
from backend.database import add_cluster_to_database
from backend.database import get_images_by_cluster
from backend.database import clear_clusters
import shutil
from fastapi import UploadFile

embedding_progress = {"current": 0, "total": 0, "status": "idle"}
cluster_progress = {"current":0 , "total":0, "status":"idle"}

def get_cluster_progress():
    return cluster_progress

def get_embedding_progress():
    return embedding_progress

def load_image(path):
    return cv.imread(path)

def draw_rectangle(image,faces):
    for face in faces:
        x1,y1,x2,y2 = face.bbox.astype(int)
        cv.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
    return image
    
def save_image(image,path):
    cv.imwrite(path,image)

def save_embeddings(face,face_id):
    EMBEDDINGS_DIR = Path("embeddings")
    EMBEDDINGS_DIR.mkdir(exist_ok=True)
    EMBEDDINGS_FILE = EMBEDDINGS_DIR/f"{face_id}.npy"
    np.save(EMBEDDINGS_FILE,face.embedding)
    return EMBEDDINGS_FILE

def create_index():
    try:
        dimension = 512
        index = faiss.IndexFlatL2(dimension)
        faiss.write_index(index,"faces.index")
        return "Faiss index created"
    except Exception as e:
        return f"Faiss index creation failed : {e}"
def add_embeddings_to_faiss(index,target_embedding):

    faiss.normalize_L2(target_embedding.reshape(1,-1))
    index.add(target_embedding.reshape(1,-1))
    

def find_nearest_neighbor(index,query_embedding):
    faiss.normalize_L2(query_embedding.reshape(1,-2))
    distance,indices = index.search(query_embedding.reshape(1,-1),k=1)
    return distance,indices

def find_matching_images(detector):
    faiss_index = faiss.read_index("faces.index")
    query_image = cv.imread("../photos/query.jpg")
    query_faces = detect_faces(query_image,detector)
    initial_comparison_embedding = query_faces[0].embedding.astype("float32")
    distance,indices = find_nearest_neighbor(faiss_index,initial_comparison_embedding)
    print("Distance____________",distance)
    print("Indices______________",indices)
    image_arr = show_nearest_images(indices)
    for image in image_arr:
        path,name,x,y,width,height = image
        image = cv.imread(str(Path(path)))
        cv.rectangle(image,(x,y),(x+width,y+height),(0,255,0),2)

        cv.imshow("Frame", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

def create_embeddings(detector,faiss_index):
    global embedding_progress
    path = "../photos"
    images = get_image_files(path)
    image_count = len(images)
    
    embedding_progress["total"] = image_count
    embedding_progress["current"] = 0
    embedding_progress["status"] = "processing"

    for index,image_path in enumerate(images,start=1):
        embedding_progress["current"] = index
        print(f"[{index}/{image_count}] Processing {image_path.name}")
        image = load_image(image_path)
        image_id = save_image_to_database(image_path)
        if image_id is None:
            continue
        faces = detect_faces(image,detector)
        if not faces:
            continue
        for face in faces:
            face_id = save_faces_to_database(face,image_id)
            embedding_path_saved = save_embeddings(face,face_id)
            save_embeddings_to_database(face_id,embedding_path_saved)
            add_embeddings_to_faiss(faiss_index,face.embedding)
        image = draw_rectangle(image,faces)
        output_path = create_output_path(image_path)
        save_image(image,output_path)
        print(f"Saved {output_path}\n")

    faiss.write_index(faiss_index,"faces.index")
    print(
        f"FAISS index saved with "
        f"{faiss_index.ntotal} vectors"
    )
    embedding_progress["status"] = "completed"
    return "FAISS index created"

def create_clusters():
    global cluster_progress
    embeddings= return_embeddings()
    cluster_progress["total"] = embeddings.shape[0]
    cluster_progress["current"] = 0
    cluster_progress["status"] = "processing"
    db = DBSCAN(eps=0.5 , min_samples=3,metric="cosine")
    labels = db.fit_predict(embeddings)
    for index , label in enumerate(labels):
        cluster_progress["current"] = index
        if label == -1:
            continue
        face_data = get_image_path_by_embeddings(index)
        if face_data is None:
            continue
        add_cluster_to_database(label, face_data)
    cluster_progress["status"] = "completed"
    return "Cluster created"

def show_clusters():
    cluster_id = int(input("Enter the cluster id: "))
    cluster_data = get_images_by_cluster(cluster_id)
    
    if not cluster_data:
        print(f"No images found for cluster {cluster_id}")
        return

    print(f"Showing images for cluster {cluster_id}. Press any key to see the next one.")
    for row in cluster_data:
        path, x, y, w, h = row
        image = cv.imread(path)
        if image is not None:   
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.imshow(f"Cluster {cluster_id}", image)
            cv.waitKey(0)
    cv.destroyAllWindows()

def save_uploaded_file(file: UploadFile, file_path: Path) -> None:
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)