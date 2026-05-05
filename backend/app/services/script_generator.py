import os
import requests
import json
from app.core.config import settings

class ScriptGenerator:
    def __init__(self):
        # Load configuration from environment variables
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate_script(self, query: str) -> str:
        """
        Calls OpenRouter API to generate a structured educational chemistry script.
        """
        if not self.api_key:
            print("ERROR: OPENROUTER_API_KEY not found in environment.")
            return self._get_fallback(query)

        # Prompt designed for educational structure and word count (100-150 words)
        prompt = (
            f"Write a chemistry education script about: {query}. "
            "Include: 1. Hook (1 sentence), 2. simple Explanation, 3. real-world Example, "
            "and 4. Summary (1 sentence). Keep the total length between 100 and 150 words."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            print(f"Request sent to OpenRouter for query: {query}")
            response = requests.post(self.url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            
            print("Response received successfully from OpenRouter.")
            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return self._get_fallback(query)

    async def generate(self, query: str) -> str:
        # Maintained async interface for compatibility with existing pipeline calls
        return self.generate_script(query)

    def _get_fallback(self, query: str) -> str:
        """Simple hardcoded explanation used when the API call fails."""
        return (f"Educational overview of {query}: This topic covers the essential chemical principles, "
                "atomic interactions, and molecular behaviors fundamental to understanding this concept.")

script_gen = ScriptGenerator()