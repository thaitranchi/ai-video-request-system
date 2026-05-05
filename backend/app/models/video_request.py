from typing import Optional
from dataclasses import dataclass
from app.schemas.video import VideoStatus

@dataclass
class VideoRequest:
    """Internal domain model for a Video Request"""
    id: str
    query: str
    status: VideoStatus
    video_url: Optional[str] = None