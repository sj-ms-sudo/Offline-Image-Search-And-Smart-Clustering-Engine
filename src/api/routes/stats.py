from fastapi import APIRouter
from backend.database import get_stats_from_database

router = APIRouter()


@router.get("/stats")
def get_stats():
    return get_stats_from_database()