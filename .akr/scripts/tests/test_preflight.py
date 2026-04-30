from __future__ import annotations

from pathlib import Path

from harness.preflight import run_preflight


def _write_manifest(path: Path) -> None:
    path.write_text(
        """project:
  name: TrainingTracker.Api
  layer: API
  standards_version: v1.1.0
  minimum_standards_version: v1.0.0
  compliance_mode: pilot
modules:
  - name: CourseDomain
    grouping_status: approved
    doc_output: docs/modules/CourseDomain_doc.md
  - name: EnrollmentDomain
    grouping_status: draft
    doc_output: docs/modules/EnrollmentDomain_doc.md
database_objects: []
unassigned: []
""",
        encoding="utf-8",
    )


def test_run_preflight_allows_approved_batch(tmp_path: Path) -> None:
    _write_manifest(tmp_path / "modules.yaml")
    result = run_preflight(
        "generate",
        tmp_path,
        active_model="gpt-5.4",
        requested_modules=["CourseDomain"],
    )

    assert result.is_clear()
    assert result.first_failure() is None


def test_run_preflight_blocks_draft_module(tmp_path: Path) -> None:
    _write_manifest(tmp_path / "modules.yaml")
    result = run_preflight(
        "generate",
        tmp_path,
        active_model="gpt-5.4",
        requested_modules=["EnrollmentDomain"],
    )

    assert not result.is_clear()
    failure = result.first_failure()
    assert failure is not None
    assert failure.name == "grouping-status"
