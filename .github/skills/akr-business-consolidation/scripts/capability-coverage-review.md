# capability-coverage-review

## Purpose

Assess whether a capability has complete source evidence for consolidation.

For `new` capabilities, assess completeness and internal consistency of PO/TL-authored
capability artifacts before development handoff (reduced-scope review).

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

For `new` capabilities, also output:

- Artifact completeness result for required new-capability files
- Internal consistency findings across index/test/dependency/limitations documents
- Explicit note that consolidation generation is skipped at `new` status

## Source access

Determine source-document location using `SKILL.md` section **Consolidation Mode**.
If `.akr-config.json` is absent or mode is not set, default to `source-evidence` and confirm evidence path before proceeding.

For `source-evidence` mode, read `sync-manifest.json` per `SKILL.md` section **Source Evidence Schema (sync-manifest.json)** and report `synced_at` for snapshot currency.
