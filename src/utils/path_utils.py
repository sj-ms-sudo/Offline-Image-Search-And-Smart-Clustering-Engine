from pathlib import Path
import os
import shutil
import numpy as np
from backend.database import drop_database_tables
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

def clear_system_data():

    from backend.database import DB_PATH
    
    dirs = [Path("../photos"), Path("../output"), Path("embeddings")]
    for d in dirs:
        if d.exists() and d.is_dir():
            shutil.rmtree(d)
            d.mkdir(parents=True, exist_ok=True)
            print(f"Cleared directory: {d}")

    files = [Path("faces.index")]
    for f in files:
        if f.exists() and f.is_file():
            f.unlink()
            print(f"Deleted file: {f}")
    drop_database_tables()