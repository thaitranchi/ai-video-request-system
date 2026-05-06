import asyncio
import traceback
import os
import shutil
import re
import time
from PIL import Image, ImageDraw, ImageFont
from app.services.openai_service import openai_service
from app.api.deps import get_db
from app.core.config import settings
from app.services.tts_service import tts_service
from app.utils.ffmpeg import ffmpeg_util

class VideoPipeline:
    def _wrap_text(self, text, chars_per_line=50):
        """Simple utility to wrap text for Pillow rendering."""
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            if len(' '.join(current_line + [word])) <= chars_per_line:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return '\n'.join(lines)

    async def process_request(self, request_id: str, query: str):
        db = next(get_db())
        # Ensure target directory exists before starting
        os.makedirs(settings.VIDEO_OUTPUT_DIR, exist_ok=True)
        
        try:
            # 1. Generate content using OpenRouter
            script_data = await openai_service.generate_video_script(query)
            slides = script_data.get('slides', [])
            
            if not slides:
                # Fallback if AI fails to return structured slides
                slides = [{"title": "Chemistry Lesson", "content": query, "narration": "Today we learn about " + query}]
            
            # 2. Setup temporary directory for assets
            temp_dir = settings.VIDEO_OUTPUT_DIR / f"temp_{request_id}"
            os.makedirs(temp_dir, exist_ok=True)
            
            def generate_assets():
                clip_paths = []
                for i, slide in enumerate(slides):
                    # Professional Dark Theme UI
                    bg_color = (30, 33, 39)      # Modern dark background
                    header_bg = (45, 49, 58)     # Slightly lighter header
                    accent_color = (0, 122, 255) # Electric blue accent
                    title_text_color = (255, 255, 255)
                    body_text_color = (210, 214, 220)

                    img = Image.new('RGB', (1280, 720), color=bg_color)
                    d = ImageDraw.Draw(img)
                    
                    # Draw Header Area
                    d.rectangle([0, 0, 1280, 100], fill=header_bg)
                    d.rectangle([0, 97, 1280, 100], fill=accent_color) # Accent border

                    # Attempt to load a clean font (Arial is standard on Windows)
                    try:
                        title_font = ImageFont.truetype("arial.ttf", 48)
                        content_font = ImageFont.truetype("arial.ttf", 36)
                    except:
                        title_font = ImageFont.load_default()
                        content_font = ImageFont.load_default()
                    
                    # Render Title
                    title_text = slide.get('title', 'Chemistry').upper()
                    d.text((60, 25), title_text, fill=title_text_color, font=title_font)
                    
                    # Render Body Content
                    wrapped_content = self._wrap_text(slide.get('content', ''), chars_per_line=55)
                    d.text((60, 160), wrapped_content, fill=body_text_color, font=content_font, spacing=15)
                    
                    img_path = temp_dir / f"slide_{i}.png"
                    img.save(img_path)
                    
                    # Generate Narration Audio using the dedicated TTS service
                    audio_path = temp_dir / f"audio_{i}.mp3"
                    tts_service.synthesize(slide.get('narration', ''), audio_path)
                    
                    # Create individual clip
                    clip_path = temp_dir / f"clip_{i}.mp4"
                    ffmpeg_util.create_slide_clip(img_path, audio_path, clip_path)
                    clip_paths.append(clip_path)
                return clip_paths

            # Offload blocking CPU/IO to a thread to keep the event loop free
            clip_paths = await asyncio.to_thread(generate_assets)

            # 3. Concatenate all clips into final video
            file_name = f"{request_id}.mp4"
            file_path = settings.VIDEO_OUTPUT_DIR / file_name
            
            await asyncio.to_thread(ffmpeg_util.concatenate_clips, clip_paths, file_path)
            
            # Atomic update to prevent race conditions in UI polling
            db[request_id].update({
                "status": "completed",
                "video_url": f"/videos/{file_name}"
            })
        except Exception as e:
            print(f"VIDEO_PIPELINE_ERROR for {request_id}: {str(e)}")
            traceback.print_exc()
            db[request_id]["status"] = "failed"
        finally:
            # Ensure cleanup happens even on failure and handle Windows file locking.
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                def robust_cleanup(path):
                    for i in range(5):
                        try:
                            shutil.rmtree(path)
                            return
                        except PermissionError:
                            time.sleep(0.5)
                    print(f"Warning: Could not delete temp directory {path} after 5 attempts.")
                
                await asyncio.to_thread(robust_cleanup, temp_dir)

video_pipeline = VideoPipeline()