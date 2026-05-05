from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Video Request System"
    API_V1_STR: str = "/api/v1"
    
    # File Storage
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    OUTPUT_DIR: Path = BASE_DIR.parent / "generated_videos"
    
    class Config:
        case_sensitive = True

settings = Settings()