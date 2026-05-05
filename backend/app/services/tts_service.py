from openai import OpenAI
from app.core.config import settings

class TTSService:
    def __init__(self):
        # Initialize the OpenAI client for professional-grade TTS.
        # Uses TTS_API_KEY or falls back to OPENAI_API_KEY from config.
        api_key = settings.TTS_API_KEY or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=api_key) if api_key else None

    def synthesize(self, text: str, output_path: str):
        """
        Converts text to professional-quality speech using OpenAI TTS.
        Falls back to gTTS if the API key is missing or the request fails.
        """
        clean_text = text.strip() if text else "Continuing the explanation."

        # Attempt professional API synthesis
        if self.client:
            try:
                # 'tts-1' is optimized for speed/latency; 'alloy' is a clear academic voice
                response = self.client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=clean_text
                )
                response.write_to_file(str(output_path))
                return
            except Exception as e:
                print(f"AI TTS API Error: {e}. Falling back to gTTS.")

        # Fallback to basic gTTS if API is unavailable
        try:
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang='en', slow=False)
            tts.save(str(output_path))
        except Exception as e:
            print(f"Critical Audio Error: Both AI and Fallback TTS failed: {e}")

tts_service = TTSService()