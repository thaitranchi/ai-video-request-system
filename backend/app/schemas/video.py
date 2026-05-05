from pydantic import BaseModel
from typing import Optional
from enum import Enum

class VideoStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class VideoRequestCreate(BaseModel):
    query: str

class VideoRequestResponse(BaseModel):
    id: str
    query: str
    status: VideoStatus
    video_url: Optional[str] = None

    class Config:
        from_attributes = True