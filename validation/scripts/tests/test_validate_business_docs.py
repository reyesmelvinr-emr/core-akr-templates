import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "validate_business_docs.py"


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT_PATH), "--workspace-root", str(root)] + args
    return subprocess.run(command, text=True, capture_output=True, check=False)


def _write_index(path: Path, business_capability: str = "CourseManagement") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                f"businessCapability: {business_capability}",
                "feature: FN12345_US678",
                "layer: Business",
                "project_type: business-consolidation",
                "status: approved",
                "compliance_mode: pilot",
                "---",
                "",
                "# Index",
            ]
        ),
        encoding="utf-8",
    )


def _touch_files(base: Path, names: list[str]) -> None:
    for name in names:
        target = base / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if name == "index.md":
            _write_index(target)
        else:
            target.write_text("placeholder", encoding="utf-8")


def test_requires_status_aware_flag() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = _run(root, [])
        assert result.returncode == 2
        assert "--status-aware is required" in result.stderr


def test_active_missing_required_files_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        cap = root / "docs" / "business-capabilities" / "active" / "CourseManagement"
        _touch_files(cap, ["index.md"])

        result = _run(root, ["--status-aware", "--fail-on", "pilot", "--report-format", "json"])
        payload = json.loads(result.stdout)

        assert result.returncode == 1
        assert payload["summary"]["errors"] > 0
        assert any("Missing required file for active" in f["message"] for f in payload["findings"])


def test_new_forbidden_files_warn_and_can_pass_in_pilot() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        cap = root / "docs" / "business-capabilities" / "new" / "UserManagement"
        required = [
            "index.md",
            "test-conditions.md",
            "limitations.md",
            "internal_dependencies.md",
            "external_dependencies.md",
            "traceability.md",
            "enhancements.md",
        ]
        _touch_files(cap, required)

        result = _run(root, ["--status-aware", "--fail-on", "pilot", "--report-format", "json"])
        payload = json.loads(result.stdout)

        assert result.returncode == 0
        assert payload["summary"]["warnings"] > 0
        assert any("must not exist for new" in f["message"] for f in payload["findings"])


def test_registry_alignment_warns_when_registry_present() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        registry = root / ".akr" / "tags"
        registry.mkdir(parents=True, exist_ok=True)
        (registry / "tag-registry.json").write_text(
            json.dumps(
                {
                    "registry": {
                        "businessCapabilities": {
                            "CourseManagement": {"approved": True}
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        cap = root / "docs" / "business-capabilities" / "new" / "SomethingElse"
        _touch_files(
            cap,
            [
                "index.md",
                "test-conditions.md",
                "limitations.md",
                "internal_dependencies.md",
                "external_dependencies.md",
                "traceability.md",
            ],
        )
        _write_index(cap / "index.md", business_capability="NotInRegistry")

        result = _run(root, ["--status-aware", "--fail-on", "pilot", "--report-format", "json"])
        payload = json.loads(result.stdout)

        assert result.returncode == 0
        assert any(f["rule"] == "registry-alignment" for f in payload["findings"])


def test_capability_path_validation_errors_for_bad_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bad = root / "docs" / "business-capabilities" / "invalid" / "X"
        bad.mkdir(parents=True, exist_ok=True)

        result = _run(
            root,
            [
                "--status-aware",
                "--capability-path",
                str(bad),
            ],
        )

        assert result.returncode == 2
        assert "capability-path must be under" in result.stderr
