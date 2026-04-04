#!/usr/bin/env python3
"""
test_constants_sync.py

CI test: asserts that shared validation constants are identical between
akr_inline_validate.py (distributed, stdlib-only) and
validate_documentation.py (stays in core-akr-templates, CI-only).

Run this in the core-akr-templates CI pipeline on every push to main
and on every skill distribution release.

The test fails if:
  - CONSTANTS_VERSION strings differ between the two files
  - Any shared enum set differs in content (catches silent drift)
  - Either file is missing (catches accidental deletion)

Exit codes:
  0 = all constants in sync
  1 = sync failure (diff reported to stdout)
  2 = file not found
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, FrozenSet

# ---------------------------------------------------------------------------
# File paths — resolved from env vars when set (CI), otherwise __file__-relative
# ---------------------------------------------------------------------------
_repo_root = Path(__file__).resolve().parents[2]  # scripts/ → .akr/ → repo root

INLINE_VALIDATOR_PATH = Path(os.environ.get(
    "INLINE_VALIDATOR_PATH",
    str(_repo_root / ".github" / "skills" / "akr-docs" / "scripts" / "akr_inline_validate.py"),
))
FULL_VALIDATOR_PATH = Path(os.environ.get(
    "FULL_VALIDATOR_PATH",
    str(_repo_root / ".akr" / "scripts" / "validate_documentation.py"),
))


def _load_module(path: Path, module_name: str) -> Any:
    if not path.exists():
        print(f"❌ File not found: {path}", file=sys.stderr)
        sys.exit(2)

    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _assert_equal(name: str, a: FrozenSet, b: FrozenSet, source_a: str, source_b: str) -> bool:
    if a == b:
        print(f"  ✅ {name}: identical ({len(a)} values)")
        return True

    only_in_a = sorted(a - b)
    only_in_b = sorted(b - a)
    print(f"  ❌ {name}: MISMATCH")
    if only_in_a:
        print(f"     Only in {source_a}: {only_in_a}")
    if only_in_b:
        print(f"     Only in {source_b}: {only_in_b}")
    return False


def main() -> int:
    print(f"Loading inline validator from:  {INLINE_VALIDATOR_PATH}")
    print(f"Loading full CI validator from: {FULL_VALIDATOR_PATH}")
    print()

    inline = _load_module(INLINE_VALIDATOR_PATH, "akr_inline_validate")
    full = _load_module(FULL_VALIDATOR_PATH, "validate_documentation")

    all_pass = True

    # --- CONSTANTS_VERSION check ---
    inline_ver = getattr(inline, "CONSTANTS_VERSION", None)
    full_ver = getattr(full, "CONSTANTS_VERSION", None)

    if inline_ver is None:
        print("❌ CONSTANTS_VERSION not found in akr_inline_validate.py")
        print("   Add: CONSTANTS_VERSION = '1.0.0' to the shared constants block.")
        all_pass = False
    elif full_ver is None:
        print("❌ CONSTANTS_VERSION not found in validate_documentation.py")
        print("   Add: CONSTANTS_VERSION = '1.0.0' to the shared constants block.")
        all_pass = False
    elif inline_ver != full_ver:
        print(f"❌ CONSTANTS_VERSION mismatch: inline={inline_ver!r}, full={full_ver!r}")
        print("   When shared constants change, bump CONSTANTS_VERSION in both files.")
        all_pass = False
    else:
        print(f"✅ CONSTANTS_VERSION: '{inline_ver}' (matches)")

    print()
    print("Checking shared enum sets:")

    # --- VALID_LAYERS ---
    inline_layers = getattr(inline, "VALID_LAYERS", None)
    full_layers = getattr(full, "PROJECT_LAYER_ENUM", None)  # different name in full validator
    if inline_layers is None or full_layers is None:
        print("  ❌ VALID_LAYERS / PROJECT_LAYER_ENUM not found in one or both files")
        all_pass = False
    else:
        ok = _assert_equal(
            "VALID_LAYERS",
            frozenset(inline_layers),
            frozenset(full_layers),
            "inline (VALID_LAYERS)",
            "full CI (PROJECT_LAYER_ENUM)",
        )
        all_pass = all_pass and ok

    # --- VALID_PROJECT_TYPES ---
    inline_types = getattr(inline, "VALID_PROJECT_TYPES", None)
    full_types = getattr(full, "PROJECT_TYPE_ENUM", None)
    if inline_types is None or full_types is None:
        print("  ❌ VALID_PROJECT_TYPES / PROJECT_TYPE_ENUM not found in one or both files")
        all_pass = False
    else:
        ok = _assert_equal(
            "VALID_PROJECT_TYPES",
            frozenset(inline_types),
            frozenset(full_types),
            "inline (VALID_PROJECT_TYPES)",
            "full CI (PROJECT_TYPE_ENUM)",
        )
        all_pass = all_pass and ok

    # --- VALID_STATUSES ---
    inline_statuses = getattr(inline, "VALID_STATUSES", None)
    full_statuses = getattr(full, "MODULE_STATUS_ENUM", None)
    if inline_statuses is None or full_statuses is None:
        print("  ❌ VALID_STATUSES / MODULE_STATUS_ENUM not found in one or both files")
        all_pass = False
    else:
        ok = _assert_equal(
            "VALID_STATUSES",
            frozenset(inline_statuses),
            frozenset(full_statuses),
            "inline (VALID_STATUSES)",
            "full CI (MODULE_STATUS_ENUM)",
        )
        all_pass = all_pass and ok

    # --- VALID_COMPLIANCE_MODES ---
    inline_modes = getattr(inline, "VALID_COMPLIANCE_MODES", None)
    full_modes = getattr(full, "VALID_COMPLIANCE_MODES", frozenset({"pilot", "production"}))
    if inline_modes is None:
        print("  \u274c VALID_COMPLIANCE_MODES not found in akr_inline_validate.py")
        all_pass = False
    else:
        ok = _assert_equal(
            "VALID_COMPLIANCE_MODES",
            frozenset(inline_modes),
            frozenset(full_modes),
            "inline (VALID_COMPLIANCE_MODES)",
            "full CI (VALID_COMPLIANCE_MODES)",
        )
        all_pass = all_pass and ok

    print()
    if all_pass:
        print("✅ All constants in sync. No drift detected.")
        return 0
    else:
        print("❌ Constant sync failure. Update both files before merging.")
        print("   See CONSTANTS_VERSION in akr_inline_validate.py for sync protocol.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
