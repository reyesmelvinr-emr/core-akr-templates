# capability-impact-analysis

## Purpose

Identify which business capabilities are affected by source documentation or code changes.

## Inputs

- Changed source document paths
- `modules.yaml` metadata from participating source repositories
- Capability registry entries from `core-akr-templates/.akr/tags/tag-registry.json`

## Required checks

- `businessCapability` values must be approved registry values.
- `feature` must match `FN#####_US#####`.
- `layer` must be present and valid for each input source.

## Outputs

- Impacted capability list
- Source-path to capability mapping
- Re-consolidation recommendation (`required` or `not-required`)

## Notes

When source metadata is incomplete, mark findings with `❓` and include a concrete follow-up owner/action.
