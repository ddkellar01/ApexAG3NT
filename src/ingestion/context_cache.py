import os
import hashlib
from typing import List, Dict
from pathlib import Path

class ContextCacheEngine:
    """Manages massive multi-modal context windows and file hashing to prevent sliding window loss."""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.cache_manifest: Dict[str, str] = {}
        
    def _hash_file(self, filepath: Path) -> str:
        content = filepath.read_bytes()
        return hashlib.sha256(content).hexdigest()

    def ingest_workspace(self, ignore_dirs: List[str] = ['.git', 'node_modules', 'venv', '__pycache__']) -> str:
        """Walks repository and builds a unified context blob for Tier 1 ingestion."""
        context_blob = ["# APEXAGENT CONTEXT DUMP\n"]
        
        for root, dirs, files in os.walk(self.workspace):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                filepath = Path(root) / file
                file_hash = self._hash_file(filepath)
                
                # Only append if file changed or not in cache
                if self.cache_manifest.get(str(filepath)) != file_hash:
                    try:
                        content = filepath.read_text(encoding='utf-8')
                        context_blob.append(f"\n--- FILE: {filepath} ---\n{content}\n")
                        self.cache_manifest[str(filepath)] = file_hash
                    except UnicodeDecodeError:
                        context_blob.append(f"\n--- FILE: {filepath} (BINARY) ---\n")
                        
        return "".join(context_blob)
