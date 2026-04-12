# capability-test-generation

## Purpose

Generate enhancement-focused test scenarios and conditions for active capabilities while preserving baseline behavior coverage.

## Status applicability

**Active capabilities only.** This skill is not applicable to new or archived capabilities, which do not support active enhancement planning or test generation workflows.

## Inputs

- `enhancements.md` (active capabilities only)
- `index.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`

## Required metadata checks

Validate metadata using `SKILL.md` section **Required Metadata and Governance**.
Do not write output if any metadata check fails; report failures with `❓`.

## Required checks

- Compare enhancement scope against baseline behavior.
- Add regression-impact cases for impacted existing behavior.
- Keep generated cases business-readable and execution-ready for QA.

## Outputs

- Updated `enhancement-test-conditions.md`
- Enhancement impact mapping notes
- Regression addition summary
