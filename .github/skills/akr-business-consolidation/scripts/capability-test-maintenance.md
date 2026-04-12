# capability-test-maintenance

## Purpose

Update baseline test conditions after capability behavior changes without introducing new enhancement scope.

## Inputs

- `index.md`
- `test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`

## Required metadata checks

Validate metadata using `SKILL.md` section **Required Metadata and Governance**.
Do not write output if any metadata check fails; report failures with `❓`.

## Required checks

- Keep `test-conditions.md` aligned with current baseline behavior in `index.md`.
- Reflect dependency and limitation impacts in test scope.
- Preserve existing IDs and update only impacted cases when possible.

## Outputs

- Updated `test-conditions.md`
- Baseline regression scope update notes
