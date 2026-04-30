#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
from typing import Callable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
INLINE_VALIDATOR_PATH = REPO_ROOT / ".github" / "skills" / "akr-docs" / "scripts" / "akr_inline_validate.py"
GENERATE_SCRIPT_PATH = REPO_ROOT / ".github" / "skills" / "akr-docs" / "scripts" / "akr-generate.md"
SKILL_PATH = REPO_ROOT / ".github" / "skills" / "akr-docs" / "SKILL.md"
TRAINING_TRACKER_FIXTURE = REPO_ROOT / "examples" / "modules.trainingtracker.api.yaml"
PYTHON_WEB_FIXTURE = REPO_ROOT / "examples" / "modules.python-web-api.yaml"
CUSTOMER_VISIBILITY_FIXTURE = REPO_ROOT / "examples" / "modules.customer-visibility.yaml"


@dataclass(frozen=True)
class AssertionResult:
    name: str
    passed: bool
    details: str


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_inline_validator_module():
    spec = importlib.util.spec_from_file_location("akr_inline_validate", INLINE_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load inline validator from {INLINE_VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _estimate_tokens(text_blobs: list[str]) -> int:
    total_words = sum(len(blob.split()) for blob in text_blobs)
    return max(1, int(total_words * 1.3))


def _assert_modules_yaml_exists() -> AssertionResult:
    exists = PYTHON_WEB_FIXTURE.exists()
    return AssertionResult("modules_yaml_exists", exists, f"Fixture exists: {PYTHON_WEB_FIXTURE}")


def _assert_modules_have_status_draft() -> AssertionResult:
    fixture = _load_yaml(PYTHON_WEB_FIXTURE)
    modules = fixture.get("modules", [])
    passed = bool(modules) and all(module.get("grouping_status") == "draft" for module in modules if isinstance(module, dict))
    return AssertionResult("modules_have_status_draft", passed, "All example grouping outputs remain in draft review state.")


def _assert_modules_max_files_le_8() -> AssertionResult:
    fixture = _load_yaml(PYTHON_WEB_FIXTURE)
    modules = fixture.get("modules", [])
    counts = [len(module.get("files", [])) for module in modules if isinstance(module, dict)]
    passed = bool(counts) and all(count <= 8 for count in counts)
    return AssertionResult("modules_max_files_le_8", passed, f"Observed file counts: {counts}")


def _assert_unassigned_has_reason() -> AssertionResult:
    fixture = _load_yaml(PYTHON_WEB_FIXTURE)
    unassigned = fixture.get("unassigned", [])
    passed = bool(unassigned) and all(item.get("reason") for item in unassigned if isinstance(item, dict))
    return AssertionResult("unassigned_has_reason", passed, "All unassigned entries include explicit reason text.")


def _assert_business_capability_pascal_case() -> AssertionResult:
    fixture = _load_yaml(CUSTOMER_VISIBILITY_FIXTURE)
    identifiers = [item.get("id", "") for item in fixture.get("businessCapabilities", []) if isinstance(item, dict)]
    passed = bool(identifiers) and all(identifier[:1].isupper() and "_" not in identifier for identifier in identifiers)
    return AssertionResult("business_capability_pascal_case", passed, f"Capability identifiers: {identifiers}")


def _assert_required_sections_present() -> AssertionResult:
    validator = _load_inline_validator_module()
    required_sections = list(getattr(validator, "BASELINE_REQUIRED_SECTIONS", []))
    expected = [
        "Quick Reference",
        "Module Files",
        "API Operations",
        "Integration Context",
        "Business Rules",
        "Data Operations",
        "Questions & Gaps",
    ]
    passed = required_sections == expected
    return AssertionResult("required_sections_present", passed, f"Required sections: {required_sections}")


def _assert_module_files_complete() -> AssertionResult:
    content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "## Step 4: Read Source Files" in content and "Module Files" in content
    return AssertionResult("module_files_complete", passed, "Generate script captures module-files extraction and section coverage.")


def _assert_operations_map_complete() -> AssertionResult:
    content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "Operations Map" in content and "2A" in content and "2B" in content
    return AssertionResult("operations_map_complete", passed, "Operations-map generation and split-pass sequencing are documented.")


def _assert_business_rules_columns_present() -> AssertionResult:
    passed = "Business Rules" in _read_text(GENERATE_SCRIPT_PATH)
    return AssertionResult("business_rules_columns_present", passed, "Business rules section remains part of the generation contract.")


def _assert_data_operations_complete() -> AssertionResult:
    passed = "Data Operations" in _read_text(GENERATE_SCRIPT_PATH)
    return AssertionResult("data_operations_complete", passed, "Data operations section remains part of the generation contract.")


def _assert_metadata_header_present() -> AssertionResult:
    content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "<!-- akr-generated -->" in content and "pass-timings-seconds" in content and "total-generation-seconds" in content
    return AssertionResult("metadata_header_present", passed, "Generate script still requires canonical metadata header fields.")


def _assert_no_truncation_markers() -> AssertionResult:
    content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "output truncating mid-section" in content
    return AssertionResult("no_truncation_markers", passed, "Generate script documents truncation handling through SSG fallback guidance.")


def _assert_passes_completed_recorded() -> AssertionResult:
    passed = "passes-completed" in _read_text(GENERATE_SCRIPT_PATH)
    return AssertionResult("passes_completed_recorded", passed, "Draft metadata records passes-completed.")


def _assert_pass_split_allowed_when_needed() -> AssertionResult:
    content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "Pass 2A" in content and "Pass 2B" in content
    return AssertionResult("pass_split_allowed_when_needed", passed, "Section-scoped generation allows split pass 2A/2B.")


def _assert_generation_strategy_section_scoped() -> AssertionResult:
    passed = "section-scoped" in _read_text(GENERATE_SCRIPT_PATH)
    return AssertionResult("generation_strategy_section_scoped", passed, "Section-scoped generation strategy is explicitly documented.")


def _assert_passes_completed_contains_1_to_7_or_split() -> AssertionResult:
    content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "1, 2A, 2B, 3, 4, 5, 6, 7" in content or "1, 2, 3, 4, 5, 6, 7" in content
    return AssertionResult("passes_completed_contains_1_to_7_or_split", passed, "Pass metadata includes the full single-pass or split-pass sequence.")


def _assert_pass_timings_present_or_unavailable() -> AssertionResult:
    passed = "pass-timings-seconds" in _read_text(GENERATE_SCRIPT_PATH)
    return AssertionResult("pass_timings_present_or_unavailable", passed, "Pass timing metadata is included in the draft contract.")


def _assert_total_generation_seconds_present_or_unavailable() -> AssertionResult:
    passed = "total-generation-seconds" in _read_text(GENERATE_SCRIPT_PATH)
    return AssertionResult("total_generation_seconds_present_or_unavailable", passed, "Total generation timing metadata is included in the draft contract.")


def _assert_forward_payload_discipline() -> AssertionResult:
    skill_content = _read_text(SKILL_PATH)
    generate_content = _read_text(GENERATE_SCRIPT_PATH)
    passed = "Forward payload between SSG passes must be structured facts only" in skill_content and "never re-read source files or charter after Pass 1" in generate_content
    return AssertionResult("forward_payload_discipline", passed, "Forward-payload discipline is documented in dispatcher and generate mode script.")


ASSERTIONS: dict[str, Callable[[], AssertionResult]] = {
    "modules_yaml_exists": _assert_modules_yaml_exists,
    "modules_have_status_draft": _assert_modules_have_status_draft,
    "modules_max_files_le_8": _assert_modules_max_files_le_8,
    "unassigned_has_reason": _assert_unassigned_has_reason,
    "business_capability_pascal_case": _assert_business_capability_pascal_case,
    "required_sections_present": _assert_required_sections_present,
    "module_files_complete": _assert_module_files_complete,
    "operations_map_complete": _assert_operations_map_complete,
    "business_rules_columns_present": _assert_business_rules_columns_present,
    "data_operations_complete": _assert_data_operations_complete,
    "metadata_header_present": _assert_metadata_header_present,
    "no_truncation_markers": _assert_no_truncation_markers,
    "passes_completed_recorded": _assert_passes_completed_recorded,
    "pass_split_allowed_when_needed": _assert_pass_split_allowed_when_needed,
    "generation_strategy_section_scoped": _assert_generation_strategy_section_scoped,
    "passes_completed_contains_1_to_7_or_split": _assert_passes_completed_contains_1_to_7_or_split,
    "pass_timings_present_or_unavailable": _assert_pass_timings_present_or_unavailable,
    "total_generation_seconds_present_or_unavailable": _assert_total_generation_seconds_present_or_unavailable,
    "forward_payload_discipline": _assert_forward_payload_discipline,
}


def evaluate_case(case_path: Path) -> dict:
    case = _load_yaml(case_path)
    assertion_results: list[AssertionResult] = []
    for assertion_name in case.get("assertions", []):
        if assertion_name not in ASSERTIONS:
            raise ValueError(f"Unsupported eval assertion: {assertion_name}")
        assertion_results.append(ASSERTIONS[assertion_name]())

    evidence_paths = [case_path]
    if case["id"] in {"generate-coursedomain", "generate-large-module", "ssg-pass-sequence"}:
        evidence_paths.extend([GENERATE_SCRIPT_PATH, INLINE_VALIDATOR_PATH, TRAINING_TRACKER_FIXTURE])
    if case["id"] == "groupings-standard":
        evidence_paths.extend([PYTHON_WEB_FIXTURE, CUSTOMER_VISIBILITY_FIXTURE])

    estimated_tokens = _estimate_tokens([_read_text(path) for path in evidence_paths])
    token_budget = case.get("token_budget")
    threshold = case.get("cost_regression_threshold", 1.0)
    budget_ok = token_budget is None or estimated_tokens <= int(token_budget * threshold)

    if token_budget is not None:
        assertion_results.append(
            AssertionResult(
                name="token_budget",
                passed=budget_ok,
                details=f"Estimated tokens {estimated_tokens} vs budget {token_budget} (threshold {threshold}).",
            )
        )

    passed = all(result.passed for result in assertion_results)
    return {
        "case_id": case["id"],
        "description": case.get("description", ""),
        "command": case.get("inputs", {}).get("command"),
        "mode": "contract-eval",
        "estimated_tokens": estimated_tokens,
        "token_budget": token_budget,
        "cost_regression_threshold": threshold,
        "passed": passed,
        "assertions": [result.__dict__ for result in assertion_results],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AKR contract eval cases against repository fixtures and prompt contracts.")
    parser.add_argument("case_path", help="Path to an eval case YAML file")
    parser.add_argument("--output", default="eval-results.json", help="Path to write JSON results")
    args = parser.parse_args()

    result = evaluate_case(Path(args.case_path))
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())