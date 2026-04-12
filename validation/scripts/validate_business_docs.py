#!/usr/bin/env python3
"""Status-aware validator for consolidation capability artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import yaml

ACTIVE_REQUIRED_FILES = [
    "index.md",
    "test-conditions.md",
    "enhancement-test-conditions.md",
    "enhancements.md",
    "backlog.md",
    "limitations.md",
    "internal_dependencies.md",
    "external_dependencies.md",
    "traceability.md",
]

NEW_REQUIRED_FILES = [
    "index.md",
    "test-conditions.md",
    "limitations.md",
    "internal_dependencies.md",
    "external_dependencies.md",
    "traceability.md",
]

ARCHIVED_REQUIRED_FILES = [
    "index.md",
    "limitations.md",
    "internal_dependencies.md",
    "external_dependencies.md",
    "traceability.md",
]

FORBIDDEN_BY_STATUS = {
    "new": [
        "enhancement-test-conditions.md",
        "enhancements.md",
        "backlog.md",
    ],
    "archived": [
        "enhancement-test-conditions.md",
        "enhancements.md",
        "backlog.md",
        "test-conditions.md",
    ],
}

FRONT_MATTER_REQUIRED_KEYS = [
    "businessCapability",
    "feature",
    "layer",
    "project_type",
    "status",
    "compliance_mode",
]

FEATURE_PATTERN = re.compile(r"^FN\d{5}_US\d{3,}$")
STATUS_VALUES = {"draft", "review", "approved", "deprecated", "in-progress"}
COMPLIANCE_VALUES = {"pilot", "production"}
LIFECYCLE_STATUS = {"active", "new", "archived"}


@dataclass
class Finding:
    severity: str
    rule: str
    message: str
    path: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "severity": self.severity,
            "rule": self.rule,
            "message": self.message,
            "path": self.path,
        }


def _required_for(status: str) -> List[str]:
    if status == "active":
        return ACTIVE_REQUIRED_FILES
    if status == "new":
        return NEW_REQUIRED_FILES
    return ARCHIVED_REQUIRED_FILES


def _severity_for_status(status: str, default: str = "error") -> str:
    if status == "active":
        return default
    return "warning"


def _read_front_matter(md_file: Path) -> Dict[str, str]:
    text = md_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    out: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def _discover_capabilities(workspace_root: Path, capability_path: Optional[Path]) -> List[Tuple[str, Path]]:
    if capability_path is not None:
        cap = capability_path.resolve()
        status = cap.parent.name
        if status not in LIFECYCLE_STATUS:
            raise ValueError("capability-path must be under docs/business-capabilities/<active|new|archived>/")
        return [(status, cap)]

    base = workspace_root / "docs" / "business-capabilities"
    discovered: List[Tuple[str, Path]] = []
    for status in sorted(LIFECYCLE_STATUS):
        status_dir = base / status
        if not status_dir.exists():
            continue
        for item in sorted(status_dir.iterdir()):
            if item.is_dir():
                discovered.append((status, item))
    return discovered


def _load_approved_capabilities(workspace_root: Path) -> Optional[set[str]]:
    registry_path = workspace_root / ".akr" / "tags" / "tag-registry.json"
    if not registry_path.exists():
        return None

    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    registry = raw.get("registry", {})
    capabilities = registry.get("businessCapabilities")
    if isinstance(capabilities, dict):
        return set(capabilities.keys())
    if isinstance(capabilities, list):
        return {str(item) for item in capabilities}
    return None


def _validate_capability(status: str, capability_dir: Path, approved_caps: Optional[set[str]]) -> List[Finding]:
    findings: List[Finding] = []
    required = _required_for(status)
    forbidden = FORBIDDEN_BY_STATUS.get(status, [])

    for name in required:
        if not (capability_dir / name).exists():
            findings.append(
                Finding(
                    severity=_severity_for_status(status),
                    rule="status-aware-required-files",
                    message=f"Missing required file for {status}: {name}",
                    path=capability_dir.as_posix(),
                )
            )

    for name in forbidden:
        if (capability_dir / name).exists():
            findings.append(
                Finding(
                    severity=_severity_for_status(status),
                    rule="status-aware-forbidden-files",
                    message=f"File must not exist for {status}: {name}",
                    path=capability_dir.as_posix(),
                )
            )

    index_file = capability_dir / "index.md"
    if not index_file.exists():
        return findings

    front_matter = _read_front_matter(index_file)
    if not front_matter:
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="front-matter",
                message="Missing YAML front matter in index.md",
                path=index_file.as_posix(),
            )
        )
        return findings

    for key in FRONT_MATTER_REQUIRED_KEYS:
        if not front_matter.get(key):
            findings.append(
                Finding(
                    severity=_severity_for_status(status),
                    rule="front-matter",
                    message=f"Missing required front matter key: {key}",
                    path=index_file.as_posix(),
                )
            )

    feature = front_matter.get("feature", "")
    if feature and not FEATURE_PATTERN.match(feature):
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="front-matter",
                message=f"Invalid feature format: {feature}",
                path=index_file.as_posix(),
            )
        )

    status_value = front_matter.get("status", "")
    if status_value and status_value not in STATUS_VALUES:
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="front-matter",
                message=f"Invalid status value: {status_value}",
                path=index_file.as_posix(),
            )
        )

    compliance_mode = front_matter.get("compliance_mode", "")
    if compliance_mode and compliance_mode not in COMPLIANCE_VALUES:
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="front-matter",
                message=f"Invalid compliance_mode value: {compliance_mode}",
                path=index_file.as_posix(),
            )
        )

    layer = front_matter.get("layer", "")
    if layer and layer != "Business":
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="front-matter",
                message=f"Expected layer: Business, got: {layer}",
                path=index_file.as_posix(),
            )
        )

    project_type = front_matter.get("project_type", "")
    if project_type and project_type != "business-consolidation":
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="front-matter",
                message=f"Expected project_type: business-consolidation, got: {project_type}",
                path=index_file.as_posix(),
            )
        )

    business_capability = front_matter.get("businessCapability", "")
    if approved_caps is not None and business_capability and business_capability not in approved_caps:
        findings.append(
            Finding(
                severity=_severity_for_status(status),
                rule="registry-alignment",
                message=f"businessCapability not in approved registry: {business_capability}",
                path=index_file.as_posix(),
            )
        )

    return findings


def _should_fail(findings: Iterable[Finding], fail_on: str) -> bool:
    if fail_on == "never":
        return False

    has_error = any(f.severity == "error" for f in findings)
    has_warning = any(f.severity == "warning" for f in findings)

    if fail_on == "pilot":
        return has_error
    return has_error or has_warning


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate status-aware consolidation capability docs")
    parser.add_argument("--workspace-root", default=".", help="Repository root path")
    parser.add_argument("--capability-path", help="Validate one capability folder path")
    parser.add_argument("--status-aware", action="store_true", help="Enable status-aware rules (required)")
    parser.add_argument("--fail-on", choices=["never", "pilot", "production"], default="pilot")
    parser.add_argument("--report-format", choices=["text", "json"], default="text")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not args.status_aware:
        print("--status-aware is required", file=sys.stderr)
        return 2

    workspace_root = Path(args.workspace_root).resolve()
    capability_path = Path(args.capability_path).resolve() if args.capability_path else None

    try:
        capabilities = _discover_capabilities(workspace_root, capability_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    approved_caps = _load_approved_capabilities(workspace_root)
    findings: List[Finding] = []

    for status, capability_dir in capabilities:
        findings.extend(_validate_capability(status, capability_dir, approved_caps))

    summary = {
        "validated_capabilities": len(capabilities),
        "errors": sum(1 for f in findings if f.severity == "error"),
        "warnings": sum(1 for f in findings if f.severity == "warning"),
        "fail_on": args.fail_on,
    }

    if args.report_format == "json":
        print(
            json.dumps(
                {
                    "summary": summary,
                    "findings": [f.to_dict() for f in findings],
                },
                indent=2,
            )
        )
    else:
        print("Status-aware consolidation validation")
        print(f"Validated capabilities: {summary['validated_capabilities']}")
        print(f"Errors: {summary['errors']}")
        print(f"Warnings: {summary['warnings']}")
        if args.verbose:
            for finding in findings:
                print(f"[{finding.severity}] {finding.rule}: {finding.message} ({finding.path})")

    return 1 if _should_fail(findings, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
