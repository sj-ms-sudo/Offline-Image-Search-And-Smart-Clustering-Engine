import shutil
from pathlib import Path
from fastapi import UploadFile


def save_uploaded_file(file: UploadFile, file_path: Path) -> None:
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)