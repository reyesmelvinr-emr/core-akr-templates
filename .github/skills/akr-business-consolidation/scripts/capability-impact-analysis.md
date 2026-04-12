# capability-impact-analysis

## Purpose

Identify which business capabilities are affected by source documentation or code changes.

## Inputs

- Changed source document paths
- `modules.yaml` metadata from participating source repositories
- Capability registry entries from `core-akr-templates/.akr/tags/tag-registry.json`

## Required checks

- Validate metadata using `SKILL.md` section **Required Metadata and Governance**.

## Outputs

- Impacted capability list
- Source-path to capability mapping
- Re-consolidation recommendation (`required` or `not-required`)

## Notes

When source metadata is incomplete, mark findings with `❓` and include a concrete follow-up owner/action.

## Source access

Determine source-document location using `SKILL.md` section **Consolidation Mode**.
If `.akr-config.json` is absent or mode is not set, default to `source-evidence` and confirm evidence path before proceeding.

For `source-evidence` mode, use `sync-manifest.json` fields per `SKILL.md` section **Source Evidence Schema (sync-manifest.json)**. At minimum include `commit_sha` and `triggering_pr` in impact analysis output.
