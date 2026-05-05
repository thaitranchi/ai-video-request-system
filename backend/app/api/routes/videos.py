from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.video import VideoRequestResponse
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[VideoRequestResponse])
async def list_videos(db: dict = Depends(deps.get_db)):
    return list(db.values())

@router.get("/{video_id}", response_model=VideoRequestResponse)
async def get_video(video_id: str, db: dict = Depends(deps.get_db)):
    video = db.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video request not found")
    return video