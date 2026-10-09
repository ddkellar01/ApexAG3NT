import os
import aiohttp
from typing import Dict, Any, Optional
import json

class GeminiClient:
    """Async client for Google Gemini (e.g., 2.5 Pro / 3.1 Pro) API for high-level planning."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
    async def generate_plan(self, model: str, prompt: str, system_instruction: str) -> Dict[str, Any]:
        """Calls the Gemini API to generate structured DAG plans."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
            
        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    text = await response.text()
                    raise RuntimeError(f"Gemini API Error: {text}")
                data = await response.json()
                
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_text)
