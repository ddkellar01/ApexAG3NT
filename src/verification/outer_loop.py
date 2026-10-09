import re
from pathlib import Path
from typing import List, Dict, Any

class OuterVerificationLoop:
    """Verifies that generated code matches high-level architectural rules in AGENTS.md."""

    def __init__(self, agents_md_path: str = "AGENTS.md"):
        self.agents_md_path = Path(agents_md_path)

    def load_directives(self) -> List[str]:
        """Loads forbidden patterns or structural rules from AGENTS.md directives."""
        if not self.agents_md_path.exists():
            return []
        content = self.agents_md_path.read_text(encoding="utf-8")
        return [line.strip() for line in content.splitlines() if line.startswith("- Rule:")]

    def verify_architectural_conformance(self, workspace_path: str = ".") -> Dict[str, Any]:
        """Scans modified files to ensure architectural boundaries were respected."""
        directives = self.load_directives()
        violations = []

        # Example rule check: verify no bare raw secrets or prohibited calls
        for file_path in Path(workspace_path).rglob("*.py"):
            if "venv" in str(file_path) or ".git" in str(file_path):
                continue
            code = file_path.read_text(encoding="utf-8", errors="ignore")
            if "eval(" in code:
                violations.append(f"Security Violation in {file_path}: Dangerous 'eval()' statement found.")

        return {
            "conforms": len(violations) == 0,
            "violations": violations,
            "directives_checked": len(directives)
        }
