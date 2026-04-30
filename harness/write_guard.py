from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import tempfile


INLINE_VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "skills"
    / "akr-docs"
    / "scripts"
    / "akr_inline_validate.py"
)


@dataclass(frozen=True)
class WriteResult:
    path: Path
    validation_passed: bool
    errors: list[dict]
    warnings: list[dict]
    estimated_tokens_written: int
    compliance_mode: str | None


class HarnessValidationError(RuntimeError):
    def __init__(self, errors: list[dict]):
        self.errors = errors
        super().__init__(f"Write guard blocked: {len(errors)} validation error(s).")


def _load_inline_validator():
    spec = importlib.util.spec_from_file_location("akr_inline_validate", INLINE_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load inline validator from {INLINE_VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _estimate_tokens(content: str) -> int:
    return max(1, int(len(content.split()) * 1.3))


def guarded_write(
    path: Path,
    content: str,
    *,
    compliance_mode: str | None = None,
    is_final: bool = True,
) -> WriteResult:
    validator = _load_inline_validator()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / (path.name or "generated.md")
        temp_path.write_text(content, encoding="utf-8")
        validation = validator.validate_file(temp_path, compliance_mode=compliance_mode, is_final=is_final)

    errors = [issue for issue in validation["issues"] if issue["severity"] == "error"]
    warnings = [issue for issue in validation["issues"] if issue["severity"] == "warning"]
    if errors:
        raise HarnessValidationError(errors)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return WriteResult(
        path=path,
        validation_passed=True,
        errors=[],
        warnings=warnings,
        estimated_tokens_written=_estimate_tokens(content),
        compliance_mode=validation.get("compliance_mode"),
    )