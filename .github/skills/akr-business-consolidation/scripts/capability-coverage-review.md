# capability-coverage-review

## Purpose

Assess whether a capability has complete source evidence for consolidation.

## Inputs

- Source module documentation from backend and UI repositories
- Required artifact contract from consolidation target-state definitions
- Capability registry values

## Required checks

- Coverage exists for core behavior, constraints, and test intent.
- Source metadata is valid per `SKILL.md` section **Required Metadata and Governance**.
- Unknowns are explicitly marked with `❓`.

## Outputs

- Coverage matrix by capability and layer
- Missing evidence list
- Readiness recommendation with blocker severity

## Source access

Determine source-document location using `SKILL.md` section **Consolidation Mode**.
If `.akr-config.json` is absent or mode is not set, default to `source-evidence` and confirm evidence path before proceeding.

For `source-evidence` mode, read `sync-manifest.json` per `SKILL.md` section **Source Evidence Schema (sync-manifest.json)** and report `synced_at` for snapshot currency.
