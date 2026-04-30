import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
GROUPINGS_PATH = REPO_ROOT / ".github" / "skills" / "akr-docs" / "scripts" / "akr-groupings.md"
MANIFEST_PATH = REPO_ROOT / ".akr" / "TEMPLATE_MANIFEST.json"
HOOK_CONFIG_PATH = REPO_ROOT / ".github" / "hooks" / "agentStop.json"
HOOK_SCRIPT_PATH = REPO_ROOT / ".github" / "hooks" / "scripts" / "validate-docs.sh"


def _extract_h2_sections(template_path: Path) -> set[str]:
    headings: set[str] = set()
    for line in template_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            headings.add(match.group(1).strip())
    return headings


def test_python_grouping_guidance_covers_advanced_patterns() -> None:
    text = GROUPINGS_PATH.read_text(encoding="utf-8")

    required_markers = [
        "signals.py",
        "management/commands/*.py",
        "admin.py",
        "tasks.py",
        "celery*.py",
        "middleware.py",
        "middlewares.py",
        "decorators.py",
    ]

    for marker in required_markers:
        assert marker in text


def test_manifest_governance_templates_have_meaningful_metadata() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    templates = {entry["id"]: entry for entry in manifest["templates"]}

    governance_ids = [
        "business-capability-template",
        "capability-backlog-template",
        "capability-enhancement-testing-template",
        "capability-enhancements-template",
        "capability-external-dependencies-template",
        "capability-internal-dependencies-template",
        "capability-limitations-template",
        "capability-testing-template",
        "feature-consolidated",
        "feature-testing-consolidated",
        "lean-baseline-service-template-module",
        "module-draft-template",
        "project-review-template",
        "traceability-template",
        "ui-component-template-module",
    ]

    for template_id in governance_ids:
        entry = templates[template_id]
        assert entry["estimated_time_minutes"] > 0
        assert entry["mandatory_sections"]

        template_path = REPO_ROOT / entry["file"]
        headings = _extract_h2_sections(template_path)

        for section in entry["mandatory_sections"]:
            assert section in headings


def test_agent_stop_hook_points_to_script_and_script_exists() -> None:
    hook = json.loads(HOOK_CONFIG_PATH.read_text(encoding="utf-8"))
    command = hook["hooks"]["agentStop"][0]["bash"]

    assert command == "bash .github/hooks/scripts/validate-docs.sh"
    assert HOOK_SCRIPT_PATH.exists()
