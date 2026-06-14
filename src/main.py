
from detector.detector import create_detector
from utils.image_utils import create_index
from utils.image_utils import find_matching_images
from utils.image_utils import create_embeddings
from backend.database import create_tables
from utils.image_utils import create_clusters
from utils.image_utils import show_clusters
import faiss
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
