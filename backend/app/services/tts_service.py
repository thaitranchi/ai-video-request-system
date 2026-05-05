import asyncio

class TTSService:
    async def synthesize(self, text: str, request_id: str) -> str:
        await asyncio.sleep(1.5)  # Simulate TTS latency
        # Returning a placeholder path
        return f"temp/audio_{request_id}.mp3"

tts_service = TTSService()