#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def update_benchmark(benchmark_path: Path, result_path: Path, *, model: str) -> dict:
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))

    benchmark["last-updated"] = "2026-04-30"
    models = benchmark.setdefault("models", {})
    model_bucket = models.setdefault(model, {})

    case_id = result["case_id"]
    case_bucket = model_bucket.setdefault(case_id, {})
    if not isinstance(case_bucket, dict):
        case_bucket = {}
        model_bucket[case_id] = case_bucket

    case_bucket["pass-rate"] = 1.0 if result.get("passed") else 0.0
    case_bucket["avg-tokens"] = result.get("estimated_tokens")

    if result.get("token_budget") is not None:
        ai_credits = case_bucket.setdefault("ai-credits", {})
        ai_credits["avg-total-tokens"] = result.get("estimated_tokens")
        ai_credits["token-budget-per-run"] = result.get("token_budget")
        ai_credits["token-budget-exceeded-threshold"] = result.get("cost_regression_threshold", 1.0)

    benchmark_path.write_text(json.dumps(benchmark, indent=2), encoding="utf-8")
    return benchmark


def main() -> int:
    parser = argparse.ArgumentParser(description="Update benchmark.json with a contract-eval result.")
    parser.add_argument("--benchmark", default="evals/benchmark.json", help="Path to benchmark JSON")
    parser.add_argument("--result", required=True, help="Path to eval result JSON")
    parser.add_argument("--model", default="ci-contract", help="Benchmark model bucket to update")
    args = parser.parse_args()

    update_benchmark(Path(args.benchmark), Path(args.result), model=args.model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())