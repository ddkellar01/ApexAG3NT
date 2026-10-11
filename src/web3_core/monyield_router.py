from typing import Dict, Any
from src.web3.monad_executor import MonadExecutor

class MonYieldRouter:
    """Handles time-locked principal protection and dynamic yield routing on Monad."""

    def __init__(self, executor: MonadExecutor, contract_address: str):
        self.executor = executor
        self.contract_address = contract_address
        self.abi = [
            {"inputs": [{"name": "amount", "type": "uint256"}], "name": "depositPrincipal", "type": "function"},
            {"inputs": [{"name": "beneficiary", "type": "address"}], "name": "routeYield", "type": "function"}
        ]

    def simulate_donation_flow(self, amount: int, beneficiary: str) -> Dict[str, Any]:
        """Simulates the deposit and yield routing before committing state changes."""
        deposit_sim = self.executor.estimate_transaction(
            self.contract_address, self.abi, "depositPrincipal", amount
        )
        
        if deposit_sim["status"] == "reverted":
            return {"success": False, "step": "deposit", "error": deposit_sim.get("error")}

        route_sim = self.executor.estimate_transaction(
            self.contract_address, self.abi, "routeYield", beneficiary
        )
        
        return {
            "success": route_sim["status"] == "success",
            "gas_estimates": {
                "deposit": deposit_sim.get("gas_estimate"),
                "route": route_sim.get("gas_estimate")
            }
        }
