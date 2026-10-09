from pydantic import BaseModel

class VerificationResult(BaseModel):
    passed: bool
    stack_trace: str = ""

class InnerVerificationLoop:
    """Runs automated AST compilation and unit tests; feeds back to Planner if failed."""
    
    def __init__(self, sandbox_engine):
        self.sandbox = sandbox_engine

    def verify_diff(self, test_command: str = "pytest tests/") -> VerificationResult:
        """Executes tests in the sandbox. Returns tracebacks for the dual-loop healer."""
        result = self.sandbox.execute_code(
            code_payload="import subprocess; subprocess.run(['pytest'])", 
            command="python3"
        )
        
        if result["status"] == "success":
            return VerificationResult(passed=True)
            
        # Trigger Self-Healing Protocol
        return VerificationResult(
            passed=False, 
            stack_trace=result.get("traceback", "Unknown AST Compilation Error")
        )
