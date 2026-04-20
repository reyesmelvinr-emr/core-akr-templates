# capability-define-review

## Purpose

Assess completeness and implementation readiness for a `new` capability authored directly by PO/TL in:

- `index.md`
- `test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`

Write a structured `#### Capability Definition Review` block into `index.md`, including open gaps,
required actions, scoring, and routing recommendation.

## Status applicability

**New capabilities only.** Enforced by dispatcher pre-check in `SKILL.md`.

## Required input files

- `index.md` (required)
- `test-conditions.md` (recommended)
- `limitations.md` (recommended)
- `internal_dependencies.md` (recommended)
- `external_dependencies.md` (recommended)

`traceability.md` is not part of the `new` capability artifact set.

## Execution Steps

### Step 1: Validate authoring baseline

- Confirm capability folder exists under `docs/business-capabilities/new/<CapabilityName>/`.
- Confirm `index.md` exists. If missing, stop and return:
  "index.md is required for capability-define-review. Author index.md first using the canonical template."

### Step 2: Evaluate business definition quality

Assess PO-owned content (`index.md`, `test-conditions.md`) for:

- Business purpose clarity
- Actor/role identification
- At least three candidate `SCN-*` scenarios
- At least one testable acceptance condition per scenario
- Out-of-scope boundaries
- Edge cases/conditional rules
- Azure Boards work-item link presence (advisory gap if missing)

### Step 3: Evaluate technical definition quality

Assess TL-owned content (`limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, technical notes in `index.md`) for:

- Layer-level artifact intent (UI/API/Database)
- Internal integration points and registry alignment
- External integration points and type/contract intent
- Known constraints/workarounds
- Security/auth/data-handling considerations
- Testability of declared `TC-*` conditions
- Infrastructure/config implications
- TL technical decision statements in required POC format:
  - Decision ID
  - Decision
  - Rationale
  - Constraints/Implications

### Step 4: Compute readiness and complexity

- Compute Definition Readiness Score on the same 0-2 scale as enhancement-review.
- Compute Complexity Score on the same 0-2 scale as enhancement-review.
- Use the existing routing decision table unchanged.

### Step 5: Write/replace review block in index.md

Write one `#### Capability Definition Review` block to `index.md`.

If a prior block exists, replace it in place and include iteration delta:

- `✅ Resolved` items from prior run
- newly raised `❓` items

Include sections:

- Definition Readiness Score
- Complexity Score
- Routing Recommendation
- Open Gaps — Business
- Open Gaps — Technical
- Required Actions Before Definition Close
- Override Record (Optional)

### Step 6: Output summary in chat

Return:

- Review status (ready/not ready)
- Count of open gaps
- Required actions remaining
- Routing recommendation

If no open gaps remain and required actions are checked, instruct user to run:

`/akr-capability capability-define-close [CapabilityName]`

## Determinism rules

- Modify only `index.md` in this mode.
- Do not create `traceability.md` for `new` capability status.
- Mark inferred content as `🤖`.
- Mark unresolved gaps as `❓` with clear owner-oriented follow-up prompts.
