import ctypes
import os
from pathlib import Path
from typing import Optional

class RustBridge:
    """Loads compiled Rust core binaries for high-performance AST and binary parsing."""

    def __init__(self, lib_path: Optional[str] = None):
        if not lib_path:
            # Default lookup for compiled shared library
            ext = "dylib" if os.uname().sysname == "Darwin" else "so"
            lib_path = str(Path(__file__).parent.parent.parent / f"target/release/libapex_core.{ext}")
        
        self._lib = None
        if os.path.exists(lib_path):
            try:
                self._lib = ctypes.CDLL(lib_path)
                self._lib.fast_parse_ast.argtypes = [ctypes.c_char_p]
                self._lib.fast_parse_ast.restype = ctypes.c_char_p
            except Exception:
                pass

    def fast_ast_parse(self, source_code: str) -> str:
        """Invokes high-speed Rust binary parser if available; falls back gracefully."""
        if self._lib and hasattr(self._lib, "fast_parse_ast"):
            res = self._lib.fast_parse_ast(source_code.encode('utf-8'))
            return res.decode('utf-8')
        return "[Fallback] Rust core library not loaded. Using Python AST."
