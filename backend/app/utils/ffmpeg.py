import os
import sys
import subprocess
from app.core.config import settings

class FFmpegUtil:
    def create_slide_clip(self, image_path: str, audio_path: str, output_path: str):
        """Combines a single image and audio file into a video clip."""
        command = [
            settings.FFMPEG_BINARY, '-y',
            '-loop', '1', '-i', str(image_path),
            '-i', str(audio_path),
            '-r', '25',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-ar', '44100',
            '-ac', '2',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            str(output_path)
        ]
        try:
            subprocess.run(command, capture_output=True, check=True, shell=sys.platform == 'win32')
        except FileNotFoundError:
            print("ERROR: FFmpeg not found. Please ensure FFmpeg is installed and added to your PATH.")
            raise
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Error: {e.stderr.decode()}")
            raise

    def concatenate_clips(self, clip_paths: list, final_output_path: str):
        """Concatenate clips using filter_complex (audio-safe)."""
        inputs = []
        filter_parts = []

        for i, path in enumerate(clip_paths):
            inputs.extend(['-i', str(path)])
            filter_parts.append(f"[{i}:v:0][{i}:a:0]")

        filter_complex = "".join(filter_parts)
        filter_complex += f"concat=n={len(clip_paths)}:v=1:a=1[outv][outa]"

        command = [
            settings.FFMPEG_BINARY, '-y',
            *inputs,
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-map', '[outa]',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-ar', '44100',
            '-ac', '2',
            '-pix_fmt', 'yuv420p',
            str(final_output_path)
        ]

        try:
            subprocess.run(command, capture_output=True, check=True, shell=sys.platform == 'win32')
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Concat Error: {e.stderr.decode()}")
            raise

ffmpeg_util = FFmpegUtil()