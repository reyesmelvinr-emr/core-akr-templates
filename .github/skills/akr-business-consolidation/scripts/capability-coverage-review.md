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

## Source access

Read `consolidation.mode` from `.akr-config.json` in the consolidation repository root before locating source documentation.

| `consolidation.mode` | Where to read source docs |
|---|---|
| `local-workspace` | Read directly from the workspace folders listed in `consolidation.sourceRepos`. Each value corresponds to a folder name in the active VS Code multi-root workspace. |
| `source-evidence` | Read from `<consolidation.sourceEvidencePath>/<repo-name>/` inside the consolidation repository. Default path: `docs/references/source-evidence/`. |

If `.akr-config.json` is absent or `consolidation.mode` is not set, default to `source-evidence` and prompt the user to confirm the evidence path before proceeding.

For `source-evidence` mode, check `sync-manifest.json` in each evidence folder and report the `synced_at` timestamp in the coverage output so reviewers can assess snapshot currency.
