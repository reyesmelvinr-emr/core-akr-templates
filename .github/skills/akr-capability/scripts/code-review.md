# code-review

## Purpose

Provide a post-coding review workflow for application repositories after implementation is complete.
This mode evaluates generated code against the approved enhancement baseline and reports:

- Alignment with `enhancements.md`
- Alignment with the confirmed mini-spec (if provided in chat/attachments)
- Improvement items and technical risks
- Gaps that should have been captured earlier in `enhancement-clarify`, mini-spec, or `enhancements.md`
- A recommended developer action plan

**This mode is read-only and does not write to any file.**

## Status applicability

**Active capabilities only.** Enforced by dispatcher pre-check in `SKILL.md`.

## Prerequisites

- `enhancements.md` exists for the capability
- At least one ENH-xxx entry has status `Review Closed`

If no closed enhancement exists, stop and return:

"No Review Closed enhancements found for <CapabilityName>. Complete enhancement review/close before code-review."

## Inputs

- `enhancements.md` (required baseline)
- `enhancement-test-conditions.md` (if available)
- `index.md`, `limitations.md`, dependency maps (if available)
- Source code and module docs in the application repo
- Mini-spec text (optional, from chat or attachment)

## Review scope

Review only the implementation surface that maps to the closed enhancement scope.
Do not expand into unrelated architecture cleanup unless it directly impacts requirement fidelity.

## Execution steps

### Step 1 - Baseline extraction

From `enhancements.md`, extract for each closed ENH-xxx:

- Business requirements
- Technical requirements
- Implementation scope update/new artifacts
- Constraints and out-of-scope statements

If mini-spec is provided, extract:

- What is being built
- Files/components expected to change
- Success criteria
- Dependency handling assumptions

### Step 2 - Implementation inventory

Identify all changed/added code and tests relevant to the enhancement.
Prefer direct source reads and test files over generated summaries.

### Step 3 - Requirement alignment assessment

Assess each requirement as:

- **Aligned**
- **Partially aligned**
- **Not aligned**
- **Not assessable** (with reason)

### Step 4 - Findings review (code-review mindset)

Prioritize defects/risks over summary prose. Focus on:

- Functional mismatches against requirements
- Behavioral regressions
- Contract mismatches (request/response, validation, persistence)
- In-memory vs EF parity issues (if applicable)
- Missing/weak tests against declared conditions
- Runtime/deployment caveats that can hide correctness

### Step 5 - Process gap assessment

Identify gaps that should have been surfaced earlier in:

- `enhancement-clarify` (missing blocker/assumption/discovery classification)
- Mini-spec (missing acceptance criterion, missing implementation detail)
- `enhancements.md` (unclear rule, ambiguous requirement, absent constraint)

Classify each as:

- **Should have been a blocker**
- **Should have been an assumption**
- **Should have been a documentation amendment**

### Step 6 - Action plan

Produce a practical action sequence for developer/TL including:

- Immediate code fixes
- Test additions/updates
- Documentation updates (if required)
- Validation steps and rerun order

## Required output format

Return the following sections in this order:

1. **Alignment With Mini-Spec And enhancements.md**
2. **Code Improvement Items**
3. **Gaps That Should Have Been Called Out Earlier**
4. **Recommended Action Plan For Developer**
5. **Additional Recommendations**

Output rules:

- Findings must be ordered by severity (High, Medium, Low)
- Every finding references concrete files/locations
- If no findings, explicitly state: "No material misalignment findings detected"
- Keep summary concise; findings remain primary

## Determinism rules

- Never invent requirements not present in source artifacts.
- If mini-spec is not provided, state this explicitly and assess against `enhancements.md` only.
- Do not perform code edits in this mode.
- Do not claim test pass/fail unless directly verified in current workspace session.
