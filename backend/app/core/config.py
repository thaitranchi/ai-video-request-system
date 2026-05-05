import asyncio
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# On Windows, the default event loop policy must be changed to support subprocesses (FFmpeg)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    print(f"DEBUG: Asyncio Policy initialized: {asyncio.get_event_loop_policy().__class__.__name__}")

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Video Request System"
    API_V1_STR: str = "/api/v1"
    
    # AI Provider
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "openai/gpt-3.5-turbo"

    # Text-to-Speech Provider
    TTS_API_KEY: str = ""
    FFMPEG_BINARY: str = "ffmpeg"

    # File Storage
    # This resolves to the project root (ai-video-request-system-demo)
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / "backend"
    VIDEO_OUTPUT_DIR: Path = ROOT_DIR / "generated_videos"
    OUTPUT_DIR: Path = ROOT_DIR / "generated_videos"
    
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.parent / ".env",
        case_sensitive=True
    )
        
settings = Settings()