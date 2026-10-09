import pytest
from src.core.rust_bridge import RustBridge

def test_rust_bridge_fallback():
    bridge = RustBridge(lib_path="/non/existent/path.so")
    res = bridge.fast_ast_parse("def test(): pass")
    assert "[Fallback]" in res
