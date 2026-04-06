import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "validate_documentation.py"


def _run_validator(workspace: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT_PATH), "--workspace-root", str(workspace)] + args
    return subprocess.run(command, text=True, capture_output=True, check=False)


def _write_module_doc(path: Path, extra_front_matter: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        textwrap.dedent(
            f"""\
            ---
            businessCapability: CourseCatalogManagement
            feature: FN00001_US100
            layer: API
            project_type: api-backend
            status: approved
            compliance_mode: pilot
            generation-strategy: section-scoped
            {extra_front_matter}---
            <!-- akr-generated
            skill: akr-docs
            -->

            ## Overview
            x

            ## Module Files
            x

            ## Operations Map
            x

            ## Architecture Overview
            x

            ## Business Rules
            x
            """
        ),
        encoding="utf-8",
    )


def test_review_status_is_accepted() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: review
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(root / "docs/modules/CourseDomain_doc.md")

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--output", "json"])
        payload = json.loads(result.stdout)
        schema_errors = [
            issue for issue in payload["preflight_issues"] if issue["rule"] == "modules-schema"
        ]
        assert all("status" not in issue["message"] for issue in schema_errors)


def test_standards_version_floor_is_enforced() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.0.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules: []
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        (root / "docs/modules/sample.md").parent.mkdir(parents=True, exist_ok=True)
        (root / "docs/modules/sample.md").write_text("## Overview\n", encoding="utf-8")

        result = _run_validator(root, ["--file", "docs/modules/sample.md", "--output", "json"])
        payload = json.loads(result.stdout)
        assert any(
            issue["message"]
            == "modules.yaml project.standards_version must be >= project.minimum_standards_version"
            for issue in payload["preflight_issues"]
        )


def test_preview_mode_prints_preview_block() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: approved
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(root / "docs/modules/CourseDomain_doc.md", "review-mode: full\n")

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--preview"])
        assert "GenerateDocumentation Preview: CourseDomain" in result.stdout
        assert "Review mode:" in result.stdout


def test_declared_artifacts_missing_warns() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: approved
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                    review_sheet: docs/modules/.akr/trainingtracker_review.md
                    draft_output: docs/modules/.akr/CourseDomain_draft.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(root / "docs/modules/CourseDomain_doc.md")

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--output", "json"])
        payload = json.loads(result.stdout)
        messages = [issue["message"] for issue in payload["preflight_issues"]]
        assert "Draft declared but not found. Run GenerateDocumentation." in messages
        assert "Review sheet declared but not found. Run ProposeGroupings." in messages


def test_final_doc_rejects_draft_only_front_matter() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: approved
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(
            root / "docs/modules/CourseDomain_doc.md",
            "preview-generated-at: 2026-03-20T12:00:00Z\nreview-mode: incremental\n",
        )

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--output", "json"])
        payload = json.loads(result.stdout)
        messages = [issue["message"] for issue in payload["results"][0]["issues"]]
        assert (
            "Final doc contains draft-only front matter fields. Re-run GenerateDocumentation Step 6a to strip before committing."
            in messages
        )


def test_semantic_score_present_surfaced_in_json() -> None:
    """When semantic-score is in front matter, JSON output must include it in the scores block."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: approved
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(root / "docs/modules/CourseDomain_doc.md", "semantic-score: 75\n")

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--output", "json"])
        payload = json.loads(result.stdout)
        scores = payload["results"][0]["scores"]
        assert scores["semantic"] == 75.0
        assert scores["combined"] is not None


def test_semantic_score_absent_combined_equals_structural() -> None:
    """When semantic-score is absent, combined_score must equal completeness_score."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: approved
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(root / "docs/modules/CourseDomain_doc.md")

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--output", "json"])
        payload = json.loads(result.stdout)
        scores = payload["results"][0]["scores"]
        assert scores["semantic"] is None
        assert scores["combined"] == scores["structural"]


def test_score_fields_not_flagged_as_draft_only() -> None:
    """Score front matter fields must NOT trigger the draft-only-fields validation error."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "modules.yaml").write_text(
            textwrap.dedent(
                """\
                project:
                  name: TrainingTracker.Api
                  layer: API
                  standards_version: v1.1.0
                  minimum_standards_version: v1.1.0
                  compliance_mode: pilot
                modules:
                  - name: CourseDomain
                    businessCapability: CourseCatalogManagement
                    feature: FN00001_US100
                    project_type: api-backend
                    status: approved
                    max_files: 3
                    files:
                      - src/Controllers/CoursesController.cs
                    doc_output: docs/modules/CourseDomain_doc.md
                database_objects: []
                unassigned: []
                """
            ),
            encoding="utf-8",
        )
        _write_module_doc(
            root / "docs/modules/CourseDomain_doc.md",
            "semantic-score: 80\nsemantic-scored-at: 2026-04-06T14:00:00Z\nsemantic-score-version: v1.0\n",
        )

        result = _run_validator(root, ["--file", "docs/modules/CourseDomain_doc.md", "--output", "json"])
        payload = json.loads(result.stdout)
        messages = [issue["message"] for issue in payload["results"][0]["issues"]]
        assert not any("draft-only front matter" in m for m in messages)
