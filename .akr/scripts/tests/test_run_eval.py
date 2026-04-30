from __future__ import annotations

from pathlib import Path

from _script_loader import load_script_module


def test_evaluate_generate_case_passes_contract_checks() -> None:
    module = load_script_module("run_eval", Path(".akr/scripts/run_eval.py"))
    result = module.evaluate_case(Path("evals/cases/generate-coursedomain.yaml"))

    assert result["case_id"] == "generate-coursedomain"
    assert result["passed"] is True
    assert result["estimated_tokens"] > 0


def test_evaluate_groupings_case_includes_budget_assertion() -> None:
    module = load_script_module("run_eval_groupings", Path(".akr/scripts/run_eval.py"))
    result = module.evaluate_case(Path("evals/cases/groupings-standard.yaml"))

    assertion_names = {item["name"] for item in result["assertions"]}
    assert "token_budget" in assertion_names