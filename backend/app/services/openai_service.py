from openai import AsyncOpenAI
from app.core.config import settings
import json

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL
        )

    async def generate_video_script(self, query: str):
        """
        Generates a structured script for a chemistry video based on the query.
        """
        system_prompt = (
            "You are an expert scriptwriter creating content specifically for text-to-speech voice generation. "
            "Generate a structured video script. Return ONLY valid JSON with a 'slides' list. "
            "Each slide must have: 'title' (max 6 words), 'content' (max 2 lines), and 'narration'.\n\n"
            "CRITICAL Narration Rules:\n"
            "- Must not be empty and minimum 20 characters.\n"
            "- Use simple punctuation only (periods and commas).\n"
            "- Avoid all symbols, emojis, abbreviations, or special characters.\n"
            "- Write out all numbers and symbols as full words.\n"
            "- No bullet points or newline characters.\n"
            "- Must sound natural when spoken aloud.\n\n"
            "General Rules:\n"
            "- 4 to 6 slides total.\n"
            "- Do not repeat titles in the narration."
        )
        
        response = await self.client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Topic: {query}"}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content or "{}")

openai_service = OpenAIService()