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
            "You are a chemistry expert. Create a short educational video script. "
            "Return the response as a JSON object with a list of 'slides'. "
            "Each slide should have 'title', 'content', and 'narration'."
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