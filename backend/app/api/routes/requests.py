from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.schemas.video import VideoRequestCreate, VideoRequestResponse, VideoStatus
from app.api import deps
from app.services.video_pipeline import video_pipeline
import uuid

router = APIRouter()

@router.post("/", response_model=VideoRequestResponse, status_code=202)
async def create_video_request(
    request_in: VideoRequestCreate,
    background_tasks: BackgroundTasks,
    db: dict = Depends(deps.get_db)
):
    request_id = str(uuid.uuid4())
    
    new_request = {
        "id": request_id,
        "query": request_in.query,
        "status": VideoStatus.PENDING,
        "video_url": None
    }
    
    db[request_id] = new_request
    
    # Kick off the background pipeline
    background_tasks.add_task(
        video_pipeline.process_request, request_id, request_in.query
    )
    
    return new_request