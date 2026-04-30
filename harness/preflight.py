from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

import yaml


SUPPORTED_MODELS = ("claude-sonnet-4-6", "gpt-5.4")
MAX_BATCH_MODULES = 5
LOCAL_ONLY_MODES = {"cache-status", "refresh-assets", "update-cache"}
MODULE_REQUIRED_MODES = {"generate", "resolve", "score"}


@dataclass(frozen=True)
class PreflightCheck:
    name: str
    passed: bool
    message: str
    credit_risk: str
    blocking: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PreflightResult:
    checks: list[PreflightCheck]

    def is_clear(self) -> bool:
        return all(check.passed for check in self.checks if check.blocking)

    def first_failure(self) -> Optional[PreflightCheck]:
        return next((check for check in self.checks if check.blocking and not check.passed), None)


def _load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle) or {}
    if not isinstance(manifest, dict):
        raise ValueError("modules.yaml must contain a mapping at top level")
    return manifest


def _modules_by_name(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modules = manifest.get("modules", [])
    if not isinstance(modules, list):
        return {}
    indexed: dict[str, dict[str, Any]] = {}
    for module in modules:
        if not isinstance(module, dict):
            continue
        name = module.get("name")
        if isinstance(name, str) and name.strip():
            indexed[name.strip()] = module
    return indexed


def _check_model_compatibility(active_model: Optional[str], supported_models: Sequence[str]) -> PreflightCheck:
    if not active_model:
        return PreflightCheck(
            name="model-compatibility",
            passed=False,
            message="Active model was not provided for preflight validation.",
            credit_risk="none",
        )

    if active_model in supported_models:
        return PreflightCheck(
            name="model-compatibility",
            passed=True,
            message=f"Model '{active_model}' is supported.",
            credit_risk="none",
            metadata={"active_model": active_model},
        )

    supported = ", ".join(supported_models)
    return PreflightCheck(
        name="model-compatibility",
        passed=False,
        message=f"Model '{active_model}' is not supported. Switch to one of: {supported}.",
        credit_risk="none",
    )


def _check_cache_directory(workspace_root: Path) -> PreflightCheck:
    cache_dir = workspace_root / ".akr" / "cache"
    if cache_dir.exists():
        return PreflightCheck(
            name="cache-readiness",
            passed=True,
            message="Local .akr/cache directory is available for template and charter reuse.",
            credit_risk="none",
            blocking=False,
            metadata={"cache_available": True},
        )

    return PreflightCheck(
        name="cache-readiness",
        passed=True,
        message="Local .akr/cache directory is not present; remote-backed runs may consume additional credits.",
        credit_risk="low",
        blocking=False,
        metadata={"cache_available": False},
    )


def _check_modules_yaml_exists(workspace_root: Path, mode: str) -> PreflightCheck:
    modules_path = workspace_root / "modules.yaml"
    required = mode in MODULE_REQUIRED_MODES
    if modules_path.exists():
        return PreflightCheck(
            name="modules-yaml",
            passed=True,
            message="modules.yaml found.",
            credit_risk="none",
            blocking=required,
            metadata={"path": str(modules_path)},
        )

    if required:
        return PreflightCheck(
            name="modules-yaml",
            passed=False,
            message="modules.yaml not found. Run '/akr-docs groupings' before this mode.",
            credit_risk="none",
        )

    return PreflightCheck(
        name="modules-yaml",
        passed=True,
        message="modules.yaml not required for this mode.",
        credit_risk="none",
        blocking=False,
    )


def _check_batch_targets(requested_modules: Sequence[str], manifest: dict[str, Any]) -> list[PreflightCheck]:
    checks: list[PreflightCheck] = []
    if not requested_modules:
        return checks

    if len(requested_modules) > MAX_BATCH_MODULES:
        checks.append(
            PreflightCheck(
                name="batch-size",
                passed=False,
                message=f"Batch size {len(requested_modules)} exceeds the maximum of {MAX_BATCH_MODULES} modules.",
                credit_risk="none",
            )
        )
        return checks

    indexed = _modules_by_name(manifest)
    missing = [module for module in requested_modules if module not in indexed]
    if missing:
        checks.append(
            PreflightCheck(
                name="batch-targets",
                passed=False,
                message=f"Requested modules not found in modules.yaml: {', '.join(missing)}.",
                credit_risk="none",
            )
        )
        return checks

    draft = [
        module_name
        for module_name in requested_modules
        if str(indexed[module_name].get("grouping_status", "")).strip().lower() == "draft"
    ]
    if draft:
        checks.append(
            PreflightCheck(
                name="grouping-status",
                passed=False,
                message=f"Requested modules still have grouping_status: draft: {', '.join(draft)}.",
                credit_risk="none",
            )
        )
        return checks

    checks.append(
        PreflightCheck(
            name="batch-targets",
            passed=True,
            message=f"Validated {len(requested_modules)} requested module target(s).",
            credit_risk="none",
            metadata={"requested_modules": list(requested_modules)},
        )
    )
    return checks


def _check_remote_prerequisites(mode: str, remote_required: bool, github_mcp_available: Optional[bool]) -> PreflightCheck:
    if mode in LOCAL_ONLY_MODES and not remote_required:
        return PreflightCheck(
            name="remote-prerequisites",
            passed=True,
            message="Remote GitHub MCP access is not required for this mode.",
            credit_risk="none",
            blocking=False,
        )

    if not remote_required:
        return PreflightCheck(
            name="remote-prerequisites",
            passed=True,
            message="Mode can proceed locally until a remote fetch is required.",
            credit_risk="low",
            blocking=False,
        )

    if github_mcp_available:
        return PreflightCheck(
            name="remote-prerequisites",
            passed=True,
            message="GitHub MCP availability confirmed for remote-backed execution.",
            credit_risk="low",
        )

    return PreflightCheck(
        name="remote-prerequisites",
        passed=False,
        message="Remote-backed execution requested, but GitHub MCP availability was not confirmed.",
        credit_risk="low",
    )


def run_preflight(
    mode: str,
    workspace_root: Path,
    *,
    active_model: Optional[str],
    requested_modules: Optional[Iterable[str]] = None,
    remote_required: bool = False,
    github_mcp_available: Optional[bool] = None,
    supported_models: Sequence[str] = SUPPORTED_MODELS,
) -> PreflightResult:
    requested = [module.strip() for module in (requested_modules or []) if module and module.strip()]
    checks: list[PreflightCheck] = [_check_model_compatibility(active_model, supported_models)]

    modules_yaml_check = _check_modules_yaml_exists(workspace_root, mode)
    checks.append(modules_yaml_check)

    manifest: dict[str, Any] = {}
    if modules_yaml_check.passed and mode in MODULE_REQUIRED_MODES.union({"groupings"}):
        manifest = _load_manifest(workspace_root / "modules.yaml")
        checks.extend(_check_batch_targets(requested, manifest))

    checks.append(_check_remote_prerequisites(mode, remote_required, github_mcp_available))
    checks.append(_check_cache_directory(workspace_root))
    return PreflightResult(checks)