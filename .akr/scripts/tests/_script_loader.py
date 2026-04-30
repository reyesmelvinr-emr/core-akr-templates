from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def load_script_module(module_name: str, relative_path: Path):
    repo_root = Path(__file__).resolve().parents[3]
    script_path = repo_root / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module