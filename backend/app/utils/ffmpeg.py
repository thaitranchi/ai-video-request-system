import asyncio
from app.core.config import settings

class FFmpegUtil:
    async def merge_audio_visual(self, image_path: str, audio_path: str, request_id: str) -> str:
        await asyncio.sleep(2)  # Simulate FFmpeg processing
        output_filename = f"{request_id}.mp4"
        # In a real app, we'd run a subprocess here
        return str(settings.OUTPUT_DIR / output_filename)

ffmpeg_util = FFmpegUtil()