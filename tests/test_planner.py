import pytest
from src.planner.thinking_engine import ThinkingEngine
from src.planner.thought_signatures import ThoughtSignatureManager

@pytest.mark.asyncio
async def test_thinking_engine_deliberative_budget():
    engine = ThinkingEngine(level="high")
    assert engine.max_tokens == 32768
    
    result = await engine.deliberate("Refactor database schema", "mock context")
    assert "Context indicates" in result.reasoning_chain
    assert "nodes" in result.proposed_dag

def test_thought_signature_generation_and_packing():
    state = {"step": 1, "plan": "refactor_pool"}
    sig = ThoughtSignatureManager.generate_signature(state)
    assert isinstance(sig, str) and len(sig) == 64  # SHA256 length

    packed = ThoughtSignatureManager.pack_signature_payload(state, trace_error="SyntaxError: invalid syntax")
    assert packed["signature"] == sig
    assert packed["verification_feedback"] == "SyntaxError: invalid syntax"
