import pytest
from src.router.dag_decomposer import DAGRouter

def test_dag_router_building_and_topological_sort():
    router = DAGRouter()
    proposed = {"nodes": ["analyze_code", "refactor_ast", "run_tests"]}
    
    router.build_graph(proposed)
    order = router.get_execution_order()
    
    assert order == ["analyze_code", "refactor_ast", "run_tests"]
    assert router.graph.nodes["refactor_ast"]["model"] == "gpt-5-3-codex"

def test_dag_router_handles_empty_dag():
    router = DAGRouter()
    router.build_graph({"nodes": []})
    assert router.get_execution_order() == []
