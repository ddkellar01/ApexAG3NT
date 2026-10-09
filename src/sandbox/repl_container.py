import subprocess
import tempfile
import os
from typing import Dict, Any

class REPLSandbox:
    """Executes generated code in an isolated environment (simulating Docker/Termux)."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def execute_code(self, code_string: str, cmd_override: str = "python") -> Dict[str, Any]:
        """Writes code to a temp file and executes it, capturing stdout/stderr."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code_string)
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [cmd_override, temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                return {"status": "success", "output": result.stdout.strip()}
            else:
                return {"status": "error", "traceback": result.stderr.strip()}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "traceback": f"Execution timed out after {self.timeout}s."}
        finally:
            os.remove(temp_path)
