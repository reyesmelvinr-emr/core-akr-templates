# AKR Business Consolidation Guidance

## Purpose

Use consolidation workflows to produce business-facing capability artifacts for PO/QA/TL audiences.

## Required practices

- Keep language business-facing and traceable to source evidence.
- Preserve unknowns with explicit `❓` markers.
- Use canonical templates and maintain artifact completeness per capability.
- Run repository validation scripts before PR or merge.

## Capability artifact contract

Each capability folder (organized by status: active/archived/new) includes a defined set of files:

**Active capabilities:**
- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`
- `enhancements.md` (in-development and delivery-tracked enhancements only)
- `backlog.md` (planned enhancements not yet queued)
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

**New capabilities:**
- `index.md` (may include Azure DevOps work-item references)
- `test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`
(excludes `enhancement-test-conditions.md`, `enhancements.md`, `backlog.md` until status changes to active)

**Archived capabilities:**
- `index.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`
(read-mostly historical baseline; excludes active test/enhancement artifacts)

## Ownership

Consolidation repository owners control editorial standards and final review decisions.
