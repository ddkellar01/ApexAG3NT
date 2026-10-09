import pytest
import asyncio
from src.ingestion.stream_listener import StreamListener
from src.ingestion.repo_graph import RepoGraphMapper

@pytest.mark.asyncio
async def test_stream_listener_queue():
    listener = StreamListener(buffer_size=5)
    await listener.push_event("github_webhook", {"action": "push"})
    
    # Test generator consumption
    async for event in listener.stream_generator():
        assert event["source"] == "github_webhook"
        assert event["data"]["action"] == "push"
        break  # Break to avoid infinite loop in test

def test_repo_graph_mapper(tmp_path):
    # Setup mock workspace
    file_a = tmp_path / "a.py"
    file_b = tmp_path / "b.py"
    
    file_a.write_text("import b")
    file_b.write_text("def run(): pass")
    
    mapper = RepoGraphMapper(root_dir=str(tmp_path))
    graph = mapper.build_graph()
    
    assert "a" in graph.nodes
    assert "b" in graph.nodes
    assert graph.has_edge("a", "b")
    
    impacted = mapper.get_impacted_modules("b")
    assert "a" in impacted
