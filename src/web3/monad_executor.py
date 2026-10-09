import os
from web3 import Web3
from typing import Dict, Any

class MonadExecutor:
    """Modular execution environment optimized for high-throughput smart contract interaction on Monad."""
    
    def __init__(self, rpc_url: str = "https://testnet-rpc.monad.xyz"):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.private_key = os.getenv("MONAD_PRIVATE_KEY")
        
        if self.private_key:
            self.account = self.w3.eth.account.from_key(self.private_key)
            self.w3.eth.default_account = self.account.address

    def estimate_transaction(self, contract_address: str, abi: list, function_name: str, *args) -> Dict[str, Any]:
        """Simulates transaction execution to catch revert errors before broadcast."""
        contract = self.w3.eth.contract(address=self.w3.to_checksum_address(contract_address), abi=abi)
        func = getattr(contract.functions, function_name)
        
        try:
            gas_estimate = func(*args).estimate_gas({'from': self.w3.eth.default_account})
            return {"status": "success", "gas_estimate": gas_estimate}
        except Exception as e:
            return {"status": "reverted", "error": str(e)}

    def execute_call(self, contract_address: str, abi: list, function_name: str, *args) -> Any:
        """Executes a read-only smart contract call."""
        contract = self.w3.eth.contract(address=self.w3.to_checksum_address(contract_address), abi=abi)
        func = getattr(contract.functions, function_name)
        return func(*args).call()
