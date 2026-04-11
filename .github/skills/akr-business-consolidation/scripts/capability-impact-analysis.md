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

## Source access

Read `consolidation.mode` from `.akr-config.json` in the consolidation repository root before locating source documentation.

| `consolidation.mode` | Where to read source docs |
|---|---|
| `local-workspace` | Read directly from the workspace folders listed in `consolidation.sourceRepos`. Each value corresponds to a folder name in the active VS Code multi-root workspace. |
| `source-evidence` | Read from `<consolidation.sourceEvidencePath>/<repo-name>/` inside the consolidation repository. Default path: `docs/references/source-evidence/`. |

If `.akr-config.json` is absent or `consolidation.mode` is not set, default to `source-evidence` and prompt the user to confirm the evidence path before proceeding.

For `source-evidence` mode, use `sync-manifest.json` `commit_sha` and `triggering_pr` fields as the source change reference when constructing the impact analysis output.
