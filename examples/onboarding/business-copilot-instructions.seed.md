# AKR Business Capability Consolidation Instructions

## Purpose

Generate and maintain business-facing capability documentation for PO/QA/TL audiences.

## Required rules

- Keep language business-facing and outcome-oriented.
- Use approved `businessCapability` values from the registry.
- Keep traceability explicit to source repo evidence.
- Mark inferred statements with `🤖` and unresolved items with `❓`.
- For `/akr-business-consolidation capability-consolidation`, use markdown source documents only; do not inspect code or schema files.
- For `/akr-business-consolidation capability-consolidation`, only update `index.md`, `test-conditions.md`, and `traceability.md`.
- Do not update PO/TL reference artifacts (`backlog.md`, `enhancements.md`, `enhancement-test-conditions.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`) in capability-consolidation mode.
- If required markdown source docs are missing, stop and return a blocking message; instruct PO/TL to have developers generate missing docs in application repos using repo-local documentation skills.

## Capability folder structure

Capabilities are organized by lifecycle status under `docs/business-capabilities/`:

- `docs/business-capabilities/active/<CapabilityName>/` — current production-used capabilities
- `docs/business-capabilities/new/<CapabilityName>/` — capabilities under construction, not yet in production
- `docs/business-capabilities/archived/<CapabilityName>/` — retained but no longer business-used

## Capability artifact contract

### Active capabilities (9 files)

- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`
- `enhancements.md`
- `backlog.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

### New capabilities (5 files)

- `index.md`
- `test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`

### Archived capabilities (5 files)

- `index.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

## Skills available

- `/akr-business-consolidation [mode] [CapabilityName]` — cross-repo consolidation skill (capability-consolidation, capability-promote, capability-promote-new, capability-coverage-review, capability-impact-analysis, capability-relationship-mapping, capability-test-maintenance)
- `/akr-capability [mode] [CapabilityName]` — enhancement assessment, new capability definition, and code review skill (enhancement-review, enhancement-review-close, enhancement-test-generation, enhancement-clarify, code-review, capability-define-review, capability-define-close, capability-define-clarify)

## Validation

Run `validation/run-validation.ps1` before merge.
