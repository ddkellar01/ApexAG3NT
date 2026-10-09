import os
import aiohttp
from typing import Dict, Any, Optional

class ClaudeClient:
    """Async client for Anthropic Claude (e.g., 3.5 Sonnet) for code critiquing and CLI scaffolding."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1/messages"
        
    async def critique_code(self, code_snippet: str, error_trace: str) -> str:
        """Acts as the secondary loop in a dual-loop AI verification architecture."""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment.")
            
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        prompt = f"Critique this code:\n{code_snippet}\n\nGiven this error trace:\n{error_trace}\n\nProvide the fixed AST patch."
        payload = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                return data["content"][0]["text"]
