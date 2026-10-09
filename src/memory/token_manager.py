from typing import List, Dict
import json

class TokenManager:
    """Approximates token counts and manages the sliding context window for LLMs."""

    def __init__(self, max_context_tokens: int = 128000):
        self.max_tokens = max_context_tokens
        # Simple heuristic: 1 token ~= 4 characters in English
        self.chars_per_token = 4

    def count_tokens(self, text: str) -> int:
        """Approximates token length without heavy tokenizer dependencies."""
        return len(text) // self.chars_per_token

    def slide_window(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Evicts older messages (excluding system prompts) to stay under budget."""
        current_tokens = sum(self.count_tokens(json.dumps(m)) for m in messages)
        
        if current_tokens <= self.max_tokens:
            return messages

        # Keep system prompt at index 0, truncate from the oldest user/assistant interactions
        system_prompt = messages[0] if messages[0].get("role") == "system" else None
        active_messages = messages[1:] if system_prompt else messages[:]

        while current_tokens > self.max_tokens and len(active_messages) > 1:
            evicted = active_messages.pop(0)
            current_tokens -= self.count_tokens(json.dumps(evicted))

        if system_prompt:
            active_messages.insert(0, system_prompt)

        return active_messages
