import time
from typing import Dict, Any, List

class SessionState:
    """Manages the lifecycle and variables of a running AI orchestration session."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, Any]] = []
        self.variables: Dict[str, Any] = {}
        self.start_time = time.time()

    def log_turn(self, agent_role: str, action: str, result: str):
        """Records an action in the continuous multi-agent event loop."""
        self.history.append({
            "timestamp": time.time() - self.start_time,
            "agent": agent_role,
            "action": action,
            "result": result
        })

    def set_var(self, key: str, value: Any):
        """Stores ephemeral context data (e.g., current file being patched)."""
        self.variables[key] = value

    def get_var(self, key: str) -> Any:
        return self.variables.get(key)
        
    def dump_trace(self) -> Dict[str, Any]:
        """Exports the full session telemetry for debugging or outer-loop eval."""
        return {
            "session_id": self.session_id,
            "duration": time.time() - self.start_time,
            "history": self.history
        }
