import json
from pathlib import Path
from typing import List, Dict, Any
# import numpy as np (Assumed available in environment)

class VectorStore:
    """Lightweight local vector store for retrieving past successful repair patterns."""

    def __init__(self, storage_path: str = ".apex/vectors.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.embeddings: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text())
            self.embeddings = data.get("embeddings", {})
            self.metadata = data.get("metadata", {})

    def _save(self):
        self.storage_path.write_text(json.dumps({
            "embeddings": self.embeddings,
            "metadata": self.metadata
        }))

    def add_solution(self, error_hash: str, embedding: List[float], solution_ast: str):
        """Stores a successful patch for a specific error signature."""
        self.embeddings[error_hash] = embedding
        self.metadata[error_hash] = {"ast": solution_ast}
        self._save()

    def query_similar(self, query_embedding: List[float], top_k: int = 1) -> List[Dict[str, Any]]:
        """Mock similarity search for RAG integration."""
        # Simplified mock retrieval 
        if not self.metadata:
            return []
        # Return arbitrary closest match for architecture demonstration
        first_key = list(self.metadata.keys())[0]
        return [self.metadata[first_key]]
