import docker
import os

class REPLSandbox:
    """Isolated execution engine using Docker to prevent side effects on the host."""
    
    def __init__(self, image: str = "apexagent-sandbox:latest"):
        self.client = docker.from_env()
        self.image = image
        self.workspace_bind = os.path.abspath(".")

    def execute_code(self, code_payload: str, command: str = "python3") -> dict:
        """Executes generated AST/Code securely inside the container."""
        try:
            container = self.client.containers.run(
                self.image,
                command=f"{command} -c \"{code_payload}\"",
                volumes={self.workspace_bind: {'bind': '/workspace', 'mode': 'ro'}}, # Read-only for safety
                working_dir="/workspace",
                detach=False,
                stdout=True,
                stderr=True,
                remove=True
            )
            return {"status": "success", "output": container.decode('utf-8')}
        except docker.errors.ContainerError as e:
            return {"status": "error", "traceback": e.stderr.decode('utf-8')}
