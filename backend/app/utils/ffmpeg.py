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
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
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
        """Concatenates multiple mp4 clips into one final video."""
        list_file = final_output_path.with_suffix('.txt')
        with open(list_file, 'w') as f:
            for path in clip_paths:
                # FFmpeg concat demuxer requires forward slashes or escaped backslashes on Windows
                abs_path = os.path.abspath(path).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")

        command = [
            settings.FFMPEG_BINARY, '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(list_file),
        ]

        command.extend(['-map', '0', '-c', 'copy', str(final_output_path)])

        try:
            subprocess.run(command, capture_output=True, check=True, shell=sys.platform == 'win32')
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Concat Error: {e.stderr.decode()}")
            raise
        if os.path.exists(list_file):
            os.remove(list_file)

ffmpeg_util = FFmpegUtil()