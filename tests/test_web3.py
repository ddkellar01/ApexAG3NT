import pytest
from unittest.mock import MagicMock
from src.web3.monyield_router import MonYieldRouter
from src.web3.monad_executor import MonadExecutor

def test_monyield_router_simulation_success():
    mock_executor = MagicMock(spec=MonadExecutor)
    # Mocking successful gas estimations
    mock_executor.estimate_transaction.return_value = {"status": "success", "gas_estimate": 21000}
    
    router = MonYieldRouter(mock_executor, "0xMockAddress")
    result = router.simulate_donation_flow(1000, "0xBeneficiary")
    
    assert result["success"] is True
    assert result["gas_estimates"]["deposit"] == 21000

def test_monyield_router_simulation_revert():
    mock_executor = MagicMock(spec=MonadExecutor)
    # Mocking a reverted deposit
    mock_executor.estimate_transaction.return_value = {"status": "reverted", "error": "Insufficient balance"}
    
    router = MonYieldRouter(mock_executor, "0xMockAddress")
    result = router.simulate_donation_flow(9999999, "0xBeneficiary")
    
    assert result["success"] is False
    assert result["step"] == "deposit"
    assert "Insufficient balance" in result["error"]
