# capability-consolidation

## Purpose

Generate or refresh the complete capability artifact set in a consolidation repository.

## Required output set

Write all files for `docs/business-capabilities/<CapabilityName>/`:

- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`
- `enhancements.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

## Template contract

Use canonical templates from `core-akr-templates/.akr/templates/`:

- `business_capability_template.md`
- `capability_testing_template.md`
- `capability_enhancement_testing_template.md`
- `capability_enhancements_template.md`
- `capability_limitations_template.md`
- `capability_internal_dependencies_template.md`
- `capability_external_dependencies_template.md`
- `traceability-template.md`

## Required checks

- Validate `businessCapability` against registry before write.
- Validate metadata fields and front matter shape.
- Preserve existing repository-owned policy files.

## Output quality

- Business-facing language only.
- Include explicit traceability to source evidence.
- Mark inferred statements with `🤖` and unknowns with `❓`.

## Source access

Read `consolidation.mode` from `.akr-config.json` in the consolidation repository root before locating source documentation.

| `consolidation.mode` | Where to read source docs |
|---|---|
| `local-workspace` | Read directly from the workspace folders listed in `consolidation.sourceRepos`. Each value corresponds to a folder name in the active VS Code multi-root workspace. |
| `source-evidence` | Read from `<consolidation.sourceEvidencePath>/<repo-name>/` inside the consolidation repository. Default path: `docs/references/source-evidence/`. |

If `.akr-config.json` is absent or `consolidation.mode` is not set, default to `source-evidence` and prompt the user to confirm the evidence path before proceeding.

For `source-evidence` mode, also read `sync-manifest.json` in each evidence folder to include source repo name, commit SHA, and sync timestamp in `traceability.md`.
