from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from core.config import PHOTOS_DIR
from utils.image_utils import save_uploaded_file
from utils.path_utils import clear_system_data

router = APIRouter()


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a valid image.")
        save_uploaded_file(file, PHOTOS_DIR / file.filename)

    return {"message": f"Successfully uploaded {len(files)} file(s)"}


@router.delete("/files")
def delete_files():
    try:
        clear_system_data()
        return {"message": "All pipeline data cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))