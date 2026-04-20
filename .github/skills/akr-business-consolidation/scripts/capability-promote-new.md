# capability-promote-new

## Purpose

Promote a completed `new` capability to `active` status after PO/TL acceptance.

This mode moves the capability folder from `new` to `active`, retains validated baseline
artifacts, seeds active-only enhancement artifacts, and updates capability lifecycle status.

## Status applicability

**New capabilities only.** Must stop if capability status is not `new`.

## Inputs

- `docs/business-capabilities/new/<CapabilityName>/index.md`
- `docs/business-capabilities/new/<CapabilityName>/test-conditions.md`
- `docs/business-capabilities/new/<CapabilityName>/limitations.md`
- `docs/business-capabilities/new/<CapabilityName>/internal_dependencies.md`
- `docs/business-capabilities/new/<CapabilityName>/external_dependencies.md`
- capability registry entry for `<CapabilityName>`

## Preconditions

1. `index.md` contains `definition_status: Definition Closed`.
2. No open `#### Capability Definition Review` blocks exist.
3. PO/TL explicitly confirm promotion in-chat by typing `confirm`.

## Execution Steps

### Step 1: Validate readiness

Confirm required files exist and preconditions are satisfied.
If not ready, report missing/invalid items and stop without writing files.

### Step 2: Confirmation gate

Present promotion summary and ask for explicit confirmation:

"Promotion is ready for <CapabilityName>. Type **confirm** to promote new -> active."

If response is not `confirm`, stop without writing files.

### Step 3: Promote artifacts

On confirmation:

1. Update `index.md`:
   - remove `definition_status: Definition Closed`
   - set capability lifecycle status to active conventions
2. Retain and move unchanged:
   - `test-conditions.md`
   - `limitations.md`
   - `internal_dependencies.md`
   - `external_dependencies.md`
3. Seed active-only artifacts in target folder:
   - `enhancements.md` from `capability_enhancements_template.md`
   - `backlog.md` from `capability_backlog_template.md`
   - `enhancement-test-conditions.md` from `capability_enhancement_testing_template.md`
4. Move folder:
   - `docs/business-capabilities/new/<CapabilityName>/` -> `docs/business-capabilities/active/<CapabilityName>/`
5. Update capability registry lifecycle status:
   - `new` -> `active`

Do not create `traceability.md` in this mode.

### Step 4: POC failure behavior

Use fail-fast behavior and avoid partial writes where possible.
If failure occurs mid-sequence, output a recovery checklist including:

- completed steps
- pending steps
- files touched
- rerun guidance

Full transactional rollback is deferred post-POC.

## Output summary

Return:

- promotion result
- moved path
- seeded files
- registry status update confirmation
- next step reminder:
  - first `capability-consolidation` run should use first-run mode and seed `traceability.md`

## Determinism rules

- Never promote without explicit `confirm`.
- Never generate `traceability.md` in this mode.
- Preserve existing `TC-*` IDs unchanged.