import pytest
from unittest.mock import patch, AsyncMock
from src.adapters.gemini_client import GeminiClient
from src.adapters.claude_client import ClaudeClient

@pytest.mark.asyncio
@patch('aiohttp.ClientSession.post')
async def test_gemini_client_generate_plan(mock_post):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": '{"nodes": ["parse"], "edges": []}'}]}}
        ]
    }
    mock_post.return_value.__aenter__.return_value = mock_response

    client = GeminiClient(api_key="fake-key")
    result = await client.generate_plan("gemini-2.5-pro", "Fix issue", "Act as architect")
    
    assert "nodes" in result
    assert result["nodes"][0] == "parse"

@pytest.mark.asyncio
@patch('aiohttp.ClientSession.post')
async def test_claude_client_critique_code(mock_post):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "content": [{"text": "def fixed(): return True"}]
    }
    mock_post.return_value.__aenter__.return_value = mock_response

    client = ClaudeClient(api_key="fake-key")
    result = await client.critique_code("def bad(): pass", "SyntaxError")
    
    assert "fixed()" in result
