# Evaluation Artifacts

This directory and the root `eval-results.json` serve different purposes.

## File Purpose Matrix

### Root eval-results.json

- Purpose: single run output for one contract-eval execution.
- Scope: one case execution, including assertions and pass/fail state.
- Typical producer: manual/local run of a specific eval command.
- Typical consumer: quick validation checks and ad hoc debugging.

### evals/benchmark.json

- Purpose: benchmark schema and longitudinal metrics container.
- Scope: many models and cases over time, including quality and cost/billing fields.
- Typical producer: benchmark pipeline or periodic benchmark aggregation process.
- Typical consumer: trend analysis, management reporting, and budget/performance review.

### evals/cases/*.yaml

- Purpose: declarative test case definitions.
- Scope: prompt/command contracts and assertion expectations used by eval runs.
- Typical producer: standards maintainers.
- Typical consumer: local contract runs and benchmark automation.

## Expected Flow

1. Define or update case contracts in `evals/cases/*.yaml`.
2. Run a case locally and inspect root `eval-results.json` for immediate pass/fail signal.
3. Aggregate repeated runs into `evals/benchmark.json` for cross-model and over-time comparisons.

## Governance Note

Treat `eval-results.json` as run output (ephemeral snapshot) and `evals/benchmark.json` as reporting structure (durable benchmark record).
