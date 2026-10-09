import hashlib
import json
from typing import Any, Dict

class ThoughtSignatureManager:
    """Preserves and encrypts internal reasoning states across multi-turn interactions."""
    
    @staticmethod
    def generate_signature(thought_state: Dict[str, Any]) -> str:
        """Creates a unique hash representing the current reasoning state."""
        state_str = json.dumps(thought_state, sort_keys=True)
        return hashlib.sha256(state_str.encode('utf-8')).hexdigest()

    @staticmethod
    def pack_signature_payload(thought_state: Dict[str, Any], trace_error: str = None) -> Dict[str, Any]:
        """Packs a previous thought signature with new execution context (like a stack trace) for self-healing."""
        return {
            "signature": ThoughtSignatureManager.generate_signature(thought_state),
            "original_reasoning": thought_state,
            "verification_feedback": trace_error
        }
