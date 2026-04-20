# capability-define-close

## Purpose

Close the PO/TL definition cycle for a `new` capability after review gaps are resolved.
This mode validates close-readiness, asks explicit confirmation, strips review blocks from
`index.md`, and marks the capability as `Definition Closed`.

## Status applicability

**New capabilities only.** Enforced by dispatcher pre-check in `SKILL.md`.

## Inputs

- `index.md` (required)
- `test-conditions.md` (required for close)

## Close-readiness checks

1. `index.md` contains no open `#### Capability Definition Review` gaps.
2. All required action items in review checklist are checked (`[x]`).
3. Routing decision is not 🚫 unless an explicit override exists.
4. `test-conditions.md` exists and has at least one `TC-*` entry.
5. `index.md` includes at least one Azure Boards work-item link (warning only if absent).
6. `index.md` includes at least one TL technical decision statement in POC format
   (Decision ID, Decision, Rationale, Constraints/Implications).

If any blocking check fails, return a readiness table and stop without file writes.

## Execution Steps

### Step 1: Validate close-readiness

Read required files and produce a close-readiness table:

| Check | Status | Note |
|---|---|---|
| Review gaps closed | ✅/❌ | ... |
| Required actions checked | ✅/❌ | ... |
| Routing eligible | ✅/❌ | ... |
| test-conditions present | ✅/❌ | ... |
| TC entries present | ✅/❌ | ... |
| Azure Boards link present | ✅/⚠️ | ... |
| TL technical decisions present | ✅/⚠️ | ... |

### Step 2: Confirmation gate

If blocking checks pass, ask:

"Definition close is ready. Type **confirm** to remove review blocks and mark Definition Closed."

If response is not `confirm`, stop without modifying files.

### Step 3: Apply close updates

On confirmation:

1. Remove all `#### Capability Definition Review` blocks from `index.md`.
2. Add `Definition Closed` marker to `index.md` front matter:
   - `definition_status: Definition Closed`

Do not modify `test-conditions.md` in this mode.

### Step 4: Completion output

Return summary in chat with:

- Definition Closed applied
- Remaining warnings (if any)
- Next command for developer handoff:
  - `/akr-capability capability-define-clarify [CapabilityName]`

## Determinism rules

- Modify only `index.md`.
- Do not create, update, or infer `traceability.md` for `new` status.
- Do not close if any blocking criteria remain unresolved.
