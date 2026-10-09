import git
from pathlib import Path

class GitSnapshotManager:
    """Handles automated file snapshotting and instant rewind (Claude-style safety)."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(self.repo_path)
        self.snapshot_ref = None

    def create_snapshot(self) -> str:
        """Stashes current uncommitted changes to create a reversible checkpoint."""
        if self.repo.is_dirty(untracked_files=True):
            self.repo.git.add(A=True)
            self.snapshot_ref = self.repo.git.stash('save', 'ApexAgent pre-execution snapshot')
            return "Snapshot created securely."
        return "Working tree clean, no snapshot needed."

    def rollback(self):
        """Instantly rewinds the workspace to the pre-execution state."""
        if self.snapshot_ref:
            self.repo.git.stash('pop')
            self.repo.git.reset('HEAD')
            self.snapshot_ref = None
            return "Rolled back to previous snapshot."
        else:
            self.repo.git.reset('--hard', 'HEAD')
            return "Hard reset applied."
