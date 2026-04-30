from __future__ import annotations

import json
from pathlib import Path

from _script_loader import load_script_module


def test_update_benchmark_writes_case_metrics(tmp_path: Path) -> None:
    module = load_script_module("update_benchmark", Path(".akr/scripts/update_benchmark.py"))
    benchmark_path = tmp_path / "benchmark.json"
    benchmark_path.write_text(json.dumps({"last-updated": "2026-03-31", "models": {}}), encoding="utf-8")

    result_path = tmp_path / "eval-results.json"
    result_path.write_text(
        json.dumps(
            {
                "case_id": "generate-coursedomain",
                "passed": True,
                "estimated_tokens": 3456,
                "token_budget": 12000,
                "cost_regression_threshold": 1.2,
            }
        ),
        encoding="utf-8",
    )

    updated = module.update_benchmark(benchmark_path, result_path, model="ci-contract")

    assert updated["models"]["ci-contract"]["generate-coursedomain"]["pass-rate"] == 1.0
    assert updated["models"]["ci-contract"]["generate-coursedomain"]["avg-tokens"] == 3456
    assert updated["models"]["ci-contract"]["generate-coursedomain"]["ai-credits"]["token-budget-per-run"] == 12000