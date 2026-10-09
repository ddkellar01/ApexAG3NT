import sys
import subprocess
import asyncio
from typing import Optional

class CLIHarness:
    """Handles Unix stdout/stdin stream piping and interactive shell tool calls."""

    @staticmethod
    def read_stdin() -> Optional[str]:
        """Reads piped input from standard input if present (e.g., `cat log.txt | apex run`)."""
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        return None

    @staticmethod
    async def execute_shell_cmd(cmd: str, timeout: int = 30) -> dict:
        """Runs a subshell command safely with streaming stdout/stderr capturing."""
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return {
                "exit_code": proc.returncode,
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace')
            }
        except asyncio.TimeoutError:
            proc.kill()
            return {"exit_code": -1, "stdout": "", "stderr": "Command timed out."}
