from pathlib import Path
import os
import numpy as np

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".png",
    ".webp",
    ".jpeg"
}

def get_image_files(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        print("Folder not found")
        return
    if not folder.is_dir():
        print(f"{folder} is not a director")
    image_files = []
    for item in folder.rglob("*"):
        if not item.is_file:
            continue
        if not item.suffix.lower() in SUPPORTED_EXTENSIONS:
            continue 
        image_files.append(item)
    return image_files

def create_output_path(image_path):
    image_path = Path(image_path)
    output_dir = Path("../output")
    output_dir.mkdir(exist_ok=True)
    return output_dir/f"{image_path.stem}_faces.jpg"

def return_embeddings():
    embeddings = []
    paths = []
    # Sort filenames numerically to ensure index matches database ID (1.npy, 2.npy...)
    filenames = sorted(os.listdir("embeddings"), 
                       key=lambda x: int(os.path.splitext(x)[0]) if x.endswith(".npy") else 0)
    for filename in filenames:
        if filename.endswith(".npy"):
            file_path = os.path.join("embeddings", filename)
            embedding = np.load(file_path)
            embeddings.append(embedding)
            paths.append(file_path)
    
    Embeddings = np.array(embeddings)
    return Embeddings