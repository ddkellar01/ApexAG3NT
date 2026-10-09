import pytest
from unittest.mock import MagicMock
from src.sandbox.repl_container import REPLSandbox
from src.verification.inner_loop import InnerVerificationLoop

def test_inner_verification_loop_pass():
    mock_sandbox = MagicMock(spec=REPLSandbox)
    mock_sandbox.execute_code.return_value = {"status": "success", "output": "1 passed"}
    
    inner_loop = InnerVerificationLoop(mock_sandbox)
    res = inner_loop.verify_diff("pytest")
    
    assert res.passed is True
    assert res.stack_trace == ""

def test_inner_verification_loop_fail():
    mock_sandbox = MagicMock(spec=REPLSandbox)
    mock_sandbox.execute_code.return_value = {"status": "error", "traceback": "AssertionError"}
    
    inner_loop = InnerVerificationLoop(mock_sandbox)
    res = inner_loop.verify_diff("pytest")
    
    assert res.passed is False
    assert "AssertionError" in res.stack_trace
