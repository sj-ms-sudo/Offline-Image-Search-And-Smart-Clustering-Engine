from pathlib import Path

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