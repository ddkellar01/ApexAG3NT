import hashlib
import json
from typing import Dict, Any, Optional

class ThoughtSignatureManager:
    """Hashes planner states to ensure traceability across the dual-loop verification cycle."""

    @staticmethod
    def generate_signature(state: Dict[str, Any]) -> str:
        """Generates a deterministic SHA-256 hash of the current planner state."""
        state_str = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_str.encode('utf-8')).hexdigest()

    @staticmethod
    def pack_signature_payload(state: Dict[str, Any], trace_error: Optional[str] = None) -> Dict[str, Any]:
        """Packages the state signature with optional feedback for the next LLM turn."""
        signature = ThoughtSignatureManager.generate_signature(state)
        
        payload = {
            "signature": signature,
            "timestamp_nonce": hash(signature) % 10000,
            "state_snapshot": state
        }
        
        if trace_error:
            payload["verification_feedback"] = trace_error
            
        return payload
