# capability-promote

## Purpose

Promote delivered enhancement outcomes into baseline capability and QA artifacts.

## Inputs

- `enhancements.md`
- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`

## Required metadata checks

- `businessCapability` must be an approved value from `core-akr-templates/.akr/tags/tag-registry.json`.
- `feature` must match `FN#####_US#####`.
- `layer` must be present and valid for each input source.
- Do not write output if any metadata check fails; report failures with `?`.

## Required checks

- Identify enhancement backlog rows that include a `Delivery Reference` value.
- Present candidate enhancement rows and request user confirmation for delivered/closed items.
- Skip non-confirmed items and include them in output notes.
- Preserve baseline scenario and test-condition continuity while promoting delivered changes.

## Execution steps

1. Read enhancement delivery candidates
   - Read `enhancements.md`.
   - Collect `Enhancement ID`, `Description`, `Status`, and `Delivery Reference` values.
   - Select rows with non-empty `Delivery Reference` as promotion candidates.

2. Confirm delivery state
   - Ask the user to confirm which candidates are delivered/closed.
   - Use only confirmed-delivered candidates for promotion.

3. Promote to baseline business behavior
   - Update `index.md` with delivered behavior, scenario updates, and business-rule updates.
   - Keep existing baseline scenarios and rules unless explicitly replaced by confirmed delivery outcomes.
   - Mark inferred updates with `?` when source certainty is partial.

4. Promote enhancement tests to baseline tests
   - Compare delivered scenario coverage in `enhancement-test-conditions.md`.
   - Merge covered enhancement conditions into `test-conditions.md` using next available `TC-*` IDs while preserving existing IDs.
   - If coverage is partial, add explicit gap placeholders in `test-conditions.md` for QA follow-up.
   - Remove promoted rows from `enhancement-test-conditions.md` after merge or reset to a minimal backlog shape.

5. Synchronize enhancement state
   - Update promoted rows in `enhancements.md` to delivered state.
   - Preserve non-promoted rows unchanged.

6. Report promotion summary
   - List promoted enhancement IDs.
   - List updated files and key ID mappings (`ETC-*` to `TC-*`).
   - List skipped items and unresolved QA gaps.

## Outputs

- Updated `index.md`
- Updated `enhancements.md`
- Updated `test-conditions.md`
- Updated `enhancement-test-conditions.md`
- Promotion summary notes

## Azure DevOps verification note

The current mode uses user-confirmed delivery status.

Future enhancement path:
- Use Azure DevOps REST API to verify work item state from `Delivery Reference` links.
- Validate that the work item state is closed/done before promotion writes are applied.
