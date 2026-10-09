import asyncio
import time
from typing import Dict, Any

async def mock_api_call(model_name: str, delay: float) -> float:
    start = time.time()
    await asyncio.sleep(delay)
    return (time.time() - start) * 1000

async def run_benchmarks() -> Dict[str, float]:
    """Measures simulated inference latency across models."""
    models = {
        "gemini-3-pro-thinking": 0.45,
        "claude-opus-4-8": 0.30,
        "gpt-5-3-codex": 0.20,
        "grok-4-7-router": 0.10
    }
    
    results = {}
    for model, latency in models.items():
        ms = await mock_api_call(model, latency)
        results[model] = round(ms, 2)
        
    return results

if __name__ == "__main__":
    print("[*] Running ApexAgent Multi-Model Latency Benchmarks...")
    bench_results = asyncio.run(run_benchmarks())
    for model, ms in bench_results.items():
        print(f"  - {model}: {ms}ms")
