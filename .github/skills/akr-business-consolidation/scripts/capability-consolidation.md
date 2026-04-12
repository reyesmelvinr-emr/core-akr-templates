# capability-consolidation

## Purpose

Generate or refresh the complete capability artifact set in a consolidation repository based on capability lifecycle status.

## Required output set

Write status-dependent files for `docs/business-capabilities/<status>/<CapabilityName>/`:

**Active capabilities (9 files):**
- `index.md`, `test-conditions.md`, `enhancement-test-conditions.md`, `enhancements.md`, `backlog.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md`

**New capabilities (6 files):**
- `index.md`, `test-conditions.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md` (excludes enhancement-test-conditions, enhancements, backlog)

**Archived capabilities (5 files):**
- `index.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md` (read-mostly historical context; excludes test and enhancement artifacts)

## Template contract

Use canonical templates from `core-akr-templates/.akr/templates/`:

- `business_capability_template.md` (all statuses)
- `capability_testing_template.md` (active, new only)
- `capability_enhancement_testing_template.md` (active only)
- `capability_enhancements_template.md` (active only)
- `capability_backlog_template.md` (active only)
- `capability_limitations_template.md` (all statuses)
- `capability_internal_dependencies_template.md` (all statuses)
- `capability_external_dependencies_template.md` (all statuses)
- `traceability-template.md` (all statuses)

## Required checks

- Validate `businessCapability` against registry before write.
- Validate metadata fields and front matter shape using `SKILL.md` section **Required Metadata and Governance**.
- Preserve existing repository-owned policy files.

## Output quality

- Business-facing language only.
- Include explicit traceability to source evidence.
- Mark inferred statements with `🤖` and unknowns with `❓`.

## Source access

Determine source-document location using `SKILL.md` section **Consolidation Mode**.
If `.akr-config.json` is absent or mode is not set, default to `source-evidence` and confirm evidence path before proceeding.

For `source-evidence` mode, read `sync-manifest.json` per `SKILL.md` section **Source Evidence Schema (sync-manifest.json)** and include source repo name, commit SHA, and sync timestamp in `traceability.md`.
