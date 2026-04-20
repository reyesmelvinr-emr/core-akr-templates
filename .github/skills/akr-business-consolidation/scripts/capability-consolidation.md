# capability-consolidation

## Purpose

Generate or refresh capability artifacts in a consolidation repository for statuses that are
eligible for consolidation.

For capabilities recently promoted from `new` to `active`, this mode uses a constrained
first-run behavior to protect PO/TL-authored baselines.

## Required output set

Write status-dependent files for `docs/business-capabilities/<status>/<CapabilityName>/`:

**Active capabilities (9 files):**
- `index.md`, `test-conditions.md`, `enhancement-test-conditions.md`, `enhancements.md`, `backlog.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md`

**New capabilities (not consolidated):**
- `capability-consolidation` does not run at status `new`.
- Source module docs are not treated as authoritative replacement for PO/TL-authored new
	capability artifacts.

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
- `traceability-template.md` (active, archived only)

## Required checks

- Validate `businessCapability` against registry before write.
- Validate metadata fields and front matter shape using `SKILL.md` section **Required Metadata and Governance**.
- Preserve existing repository-owned policy files.

## Status gating

- If capability status is `new`, stop and return:
	"capability-consolidation does not run for new capabilities. Promote to active first using capability-promote-new."

- If capability status is `archived`, run in read-mostly mode and preserve historical context.

## First-run mode (post-promotion active)

Detect first-run mode when all are true:

1. Capability status is `active`
2. `traceability.md` is absent
3. `enhancements.md` exists and is empty/seeded

When first-run mode is active:

- **Write scope:** create `traceability.md` only.
- **Read-only:** `index.md`, `test-conditions.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`.
- Produce a chat-only Suggested Additions Report covering advisory additions/refinements for
	read-only baseline artifacts.

Suggested Additions governance actions (POC):

1. Accept all
2. Reject all
3. Manual selective update

## Output quality

- Business-facing language only.
- Include explicit traceability to source evidence.
- Mark inferred statements with `🤖` and unknowns with `❓`.

## Source access

Determine source-document location using `SKILL.md` section **Consolidation Mode**.
If `.akr-config.json` is absent or mode is not set, default to `source-evidence` and confirm evidence path before proceeding.

For `source-evidence` mode, read `sync-manifest.json` per `SKILL.md` section **Source Evidence Schema (sync-manifest.json)** and include source repo name, commit SHA, and sync timestamp in `traceability.md`.
