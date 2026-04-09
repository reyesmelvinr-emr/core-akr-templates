# capability-coverage-review

## Purpose

Assess whether a capability has complete source evidence for consolidation.

## Inputs

- Source module documentation from backend and UI repositories
- Required artifact contract from consolidation target-state definitions
- Capability registry values

## Required checks

- Coverage exists for core behavior, constraints, and test intent.
- Source metadata is valid (`businessCapability`, `feature`, `layer`, `project_type`).
- Unknowns are explicitly marked with `❓`.

## Outputs

- Coverage matrix by capability and layer
- Missing evidence list
- Readiness recommendation with blocker severity
