import os
from pathlib import Path

class TreeVisualizer:
    """Generates structured ASCII tree diagrams for repository documentation."""

    @staticmethod
    def generate_ascii_tree(dir_path: str, prefix: str = "", ignore_dirs: set = None) -> str:
        """Recursively builds an ASCII representation of the directory structure."""
        if ignore_dirs is None:
            ignore_dirs = {'.git', '__pycache__', 'venv', 'node_modules', '.apex'}
            
        path = Path(dir_path)
        if not path.exists():
            return ""

        tree_str = ""
        items = sorted([item for item in path.iterdir() if item.name not in ignore_dirs])
        
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            tree_str += f"{prefix}{connector}{item.name}\n"
            
            if item.is_dir():
                extension = "    " if is_last else "│   "
                tree_str += TreeVisualizer.generate_ascii_tree(str(item), prefix + extension, ignore_dirs)
                
        return tree_str

if __name__ == "__main__":
    # Example usage for automated README generation
    print("Project Structure:\n")
    print(TreeVisualizer.generate_ascii_tree("."))
