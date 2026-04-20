# capability-promote

## Purpose

Promote delivered enhancement outcomes into baseline capability and QA artifacts.

## Inputs

- `backlog.md` (source for items moving into development queue)
- `enhancements.md` (source for in-development items with delivery status)
- `index.md` (baseline business behavior document to update)
- `limitations.md` (baseline operational constraints to update when enhancement introduces or changes limits)
- `internal_dependencies.md` (baseline internal dependency map to update when enhancement changes capability interactions)
- `external_dependencies.md` (baseline external integration dependency map to update when enhancement changes interfaces/contracts)
- `test-conditions.md` (baseline QA condition set to extend)
- `enhancement-test-conditions.md` (enhancement candidate condition source)

## Required metadata checks

- `businessCapability` must be an approved value from `core-akr-templates/.akr/tags/tag-registry.json`.
- `feature` must match `FN#####_US#####`.
- `layer` must be present and valid for each input source.
- Do not write output if any metadata check fails; report failures with `?`.

## Required checks

- Identify enhancement backlog rows that include a `Delivery Reference` value.
- Present candidate enhancement rows and request user confirmation for delivered/closed items.
- Request explicit PO/TL confirmation that promoted items are accepted by both business and technical owners.
- Ask whether enhancement testing is complete for confirmed items.
- Skip non-confirmed items and include them in output notes.
- Preserve baseline scenario and test-condition continuity while promoting delivered changes.
- When testing is not complete or explicitly out of scope (for example, POC mode), continue with business baseline promotion and dependency/limitation synchronization, and record deferred test-promotion notes.

## Execution steps

1. Read enhancement delivery candidates
   - **From backlog (optional):** Read `backlog.md` to identify planned items ready to move into the active enhancement queue. Ask user to confirm which backlog entries should transition to `enhancements.md` for development.
   - **From enhancements:** Read `enhancements.md`.
   - Collect `Enhancement ID`, `Description`, `Status`, and `Delivery Reference` values.
   - Select rows with non-empty `Delivery Reference` as promotion candidates.

2. Confirm delivery state
   - Ask the user to confirm which candidates are delivered/closed.
   - Ask the user to confirm PO/TL acceptance for each delivered candidate.
   - Ask the user whether testing is complete for each accepted candidate.
   - Use only confirmed-delivered and PO/TL-accepted candidates for promotion.

3. Promote to baseline business behavior
   - Update `index.md` with delivered behavior, scenario updates, and business-rule updates.
   - Keep existing baseline scenarios and rules unless explicitly replaced by confirmed delivery outcomes.
   - Mark inferred updates with `🤖` when source certainty is partial.

4. Promote dependency and limitation updates
   - Update `limitations.md` when delivered enhancements introduce new constraints, modify existing constraints, or remove obsolete workarounds.
   - Update `internal_dependencies.md` when delivered enhancements change in-application capability interactions or dependency expectations.
   - Update `external_dependencies.md` when delivered enhancements change integration contracts, authentication assumptions, or external touchpoints.
   - Preserve existing IDs and references; append or amend entries rather than rewriting entire sections.

5. Promote enhancement tests to baseline tests (when testing complete)
   - If testing is confirmed complete, compare delivered scenario coverage in `enhancement-test-conditions.md`.
   - Merge covered enhancement conditions (`BTC-*`, `TTC-*`, `RTC-*`) into `test-conditions.md` using next available `TC-*` IDs while preserving existing IDs.
   - If coverage is partial, add explicit gap placeholders in `test-conditions.md` for QA follow-up.
   - Remove promoted rows from `enhancement-test-conditions.md` after merge.
   - If testing is not complete or out of scope, skip this step and record deferred test merge actions in output notes.

6. Synchronize enhancement state
   - Update promoted rows in `enhancements.md` to delivered state.
   - Preserve non-promoted rows unchanged.

7. Report promotion summary
   - List promoted enhancement IDs.
   - List updated files and key ID mappings (`BTC-*`/`TTC-*`/`RTC-*` to `TC-*`) when test promotion ran.
   - List dependency/limitation updates applied.
   - List skipped items, unresolved QA gaps, and deferred test-promotion actions.
   - If backlog-to-enhancement transitions were made, include transition summary.

## Outputs

- Updated `index.md`
- Updated `limitations.md` (as needed)
- Updated `internal_dependencies.md` (as needed)
- Updated `external_dependencies.md` (as needed)
- Updated `enhancements.md`
- Updated `test-conditions.md` (when testing complete)
- Updated `enhancement-test-conditions.md` (when testing complete)
- Promotion summary notes

## Azure DevOps verification note

The current mode uses user-confirmed delivery status.

Future enhancement path:
- Use Azure DevOps REST API to verify work item state from `Delivery Reference` links.
- Validate that the work item state is closed/done before promotion writes are applied.
