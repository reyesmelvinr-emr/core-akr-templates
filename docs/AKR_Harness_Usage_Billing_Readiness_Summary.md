# AKR Harness Readiness Summary for Copilot Usage-Based Billing

Date: 2026-04-30

## Why this matters now
Starting June 1, 2026, Copilot cost is directly tied to token consumption. In this model, repeated context loads, failed runs, and avoidable regeneration are no longer just quality issues. They become measurable spend.

The harness work recently implemented in core-akr-templates is strategically important because it introduces cost-control guardrails before expensive model operations are triggered.

## What was implemented and why it is financially relevant
1. Preflight harness
- File: harness/preflight.py
- Value: blocks unsupported model usage, invalid module targets, and batch issues before high-token generation steps begin.
- Billing impact: reduces token burn from runs that should never proceed.

2. Cache integrity harness
- File: harness/cache_guard.py
- Value: detects stale and corrupt cache states; prevents silent bad-cache reuse patterns that often trigger expensive retries.
- Billing impact: lowers unnecessary repeated fetch/generation cycles.

3. Write guard harness
- File: harness/write_guard.py
- Value: validates candidate output before persistence; blocks invalid writes that would require a second full generation pass.
- Billing impact: reduces regeneration cost.

4. Iteration guard
- File: harness/iteration_guard.py
- Value: prevents review-loop regressions and hard-stops runaway iteration counts.
- Billing impact: constrains repeated full-context iterations.

5. Checkpoint harness
- File: harness/checkpoint.py
- Value: supports resumability from last completed state instead of restarting long flows.
- Billing impact: avoids re-paying token cost for already completed passes.

6. Eval budget wiring
- Files: evals/cases/*.yaml, .akr/scripts/run_eval.py, .akr/scripts/update_benchmark.py, .github/workflows/run-evals.yml
- Value: introduces per-case token budgets and CI budget checks.
- Billing impact: detects cost regression early.

## Current efficiency baseline from the repository
From the recent contract eval output:
- generate-coursedomain estimated tokens: 8,262
- token budget configured: 12,000
- budget status: pass

This gives a practical baseline for comparison scenarios below.

## Token efficiency comparison: with harness vs without harness
The table below is a practical estimation model for a single module generation run using the 8,262-token baseline. These are planning estimates for POC decision-making, not final billing telemetry.

| Category | Without harness (expected waste) | With harness (expected waste) | Estimated reduction |
|---|---:|---:|---:|
| Preflight failures discovered late | 1,652 tokens per run (20%) | 330 tokens per run (4%) | 1,322 |
| Regeneration due to invalid writes | 1,239 tokens per run (15%) | 248 tokens per run (3%) | 991 |
| Redundant cache-related rework | 992 tokens per run (12%) | 331 tokens per run (4%) | 661 |
| Loop or resume inefficiency | 1,157 tokens per run (14%) | 413 tokens per run (5%) | 744 |
| Total avoidable overhead | 5,040 | 1,322 | 3,718 |

Projected per-run impact:
- Without harness: 8,262 + 5,040 = 13,302 tokens
- With harness: 8,262 + 1,322 = 9,584 tokens
- Estimated savings: 3,718 tokens per run, about 28%

## Cost perspective (illustrative)
Using 1 credit = 0.01 USD and proportional token billing:
- If a team runs 100 comparable generation flows per week, estimated token reduction is about 371,800 tokens per week.
- Relative spend reduction is about 28% versus an ungated process under the same workload.

## Sensitivity range for POC planning
To avoid overconfidence, use a three-band estimate:

| Scenario | Estimated savings per run |
|---|---:|
| Conservative | 15% to 20% |
| Expected | 25% to 30% |
| Aggressive | 35% to 45% |

The implemented harness set is most likely to land in the Expected band once fully enforced in all execution paths.

## POC readiness statement
For POC scope, the harness implementation is meaningful and directionally strong because:
- the right cost-protective controls exist in code,
- budget-aware eval mechanics are wired into CI,
- and baseline token budgeting is now explicit.

For production-level confidence before billing cutover, prioritize:
1. Executing harness gates from runtime paths (not only as documented contract guidance),
2. Capturing non-placeholder telemetry for session ledger fields,
3. Aggregating matrix eval outputs into one benchmark snapshot per workflow run.

## Practical next metric targets
For the next sprint, track these KPIs per run:
- Preflight abort rate
- Cache hit rate
- Regeneration rate after write validation
- Average tokens per successful run
- Budget exceedance rate in eval CI

If these five KPIs trend down after harness enforcement, the AKR solution is demonstrably prepared for usage-based billing economics.