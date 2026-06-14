
from detector.detector import create_detector
from utils.image_utils import create_index
from utils.image_utils import find_matching_images
from utils.image_utils import create_embeddings
from backend.database import create_tables
from utils.image_utils import create_clusters
from utils.image_utils import show_clusters
from backend.database import get_image_count_from_database
from backend.database import get_face_count_from_database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import faiss

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {
        "message":"Hello World"
    }

@app.get("/images/count")
def get_image_count():
    count = get_image_count_from_database()
    return {
        "count":count
    }

@app.get("/faces/count")
def get_face_count():
    count = get_face_count_from_database()
    return {
        "count":count
    }
def main():
    choice = int(input("1.Create Faiss index\n2.Load image to find matching faces\n3.Create embeddings\n4.Create database\n5.Create clusters\n6. Show clusters"))
    detector = create_detector()
    if choice ==1:
        create_index()
    elif choice ==2:
        find_matching_images(detector,)
    elif choice ==3:
        try:
            faiss_index = faiss.read_index("faces.index")
        except:
            print("Faiss index not found")
            return
        create_embeddings(detector,faiss_index)
    elif choice ==4:
        create_tables()
    elif choice == 5:
        create_clusters()
    elif choice == 6:
        show_clusters()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
