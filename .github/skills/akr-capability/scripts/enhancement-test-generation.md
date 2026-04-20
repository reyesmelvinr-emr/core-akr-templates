# enhancement-test-generation

## Purpose

Generate recommended test conditions for each closed enhancement in an active capability's `enhancements.md`, populating or refreshing the capability's `enhancement-test-conditions.md`. Tests are derived directly from the Business Requirements and Technical Requirements declared in the enhancement, cross-checked against the capability baseline in `index.md`.

Test conditions are produced in two separate tiers:

- **Business Test Conditions (`BTC-`)** — executable by a business user or QA tester without technical tooling. Derived from Business Requirements. Covers UI flows, business rules, observable outcomes, and acceptance criteria.
- **Technical Test Conditions (`TTC-`)** — executable by a QA tester with technical expertise. Derived from Technical Requirements. Covers API calls, database record verification, integration assertions, and system-state checks.

Regression test conditions (`RTC-`) are also generated for both tiers to confirm that behavior outside the enhancement scope remains unchanged.

## Status applicability

**Active capabilities only.** Enforced by dispatcher pre-check in `SKILL.md`.

## Pre-condition

`enhancements.md` must not contain any active `<!-- akr-capability: review-in-progress -->` markers. All enhancements must have passed `enhancement-review-close` before test generation is run.

If active review markers are found, stop and return:
"Enhancement review is still in progress for <CapabilityName>. Run `/akr-capability enhancement-review-close [CapabilityName]` before generating tests."

## Inputs

- `enhancements.md` (source of Business Requirements and Technical Requirements per ENH-xxx)
- `index.md` (baseline behavior and scenario IDs for regression scope)
- `limitations.md` (constraints that affect test feasibility)
- `internal_dependencies.md` (cross-capability impact for regression scope)
- `external_dependencies.md` (integration impact for technical test scope)
- `enhancement-test-conditions.md` (existing file to update if present; created fresh if absent)

## Required metadata checks

Validate metadata using `SKILL.md` section **Required Metadata and Governance**.
Do not write output if any metadata check fails; report failures with `❓`.

## Execution Steps

Execute these steps in order for each ENH-xxx entry found in `enhancements.md`.

### Step 1: Locate enhancement entries

- Read the Enhancement Activity table to identify all ENH-xxx IDs.
- Skip entries where Status is `NEEDS`, still a placeholder, or not yet in development.
- For each qualifying entry, read the Business Requirements and Technical Requirements sections.

### Step 2: Derive Business Test Conditions

From the Business Requirements section of each ENH-xxx:

- Map each stated business outcome or acceptance criterion to one or more `BTC-` test conditions.
- Each `BTC-` must include: scenario description, preconditions (in plain business terms), step-by-step actions a business user or non-technical QA tester can execute, and expected result stated in business terms.
- Do not include implementation-level details (API routes, table names, query syntax) in `BTC-` conditions.
- Flag any business requirement that lacks enough detail for test derivation with `❓ [requirement ref]: [clarifying question]`.

### Step 3: Derive Technical Test Conditions

From the Technical Requirements section of each ENH-xxx:

- Map each implementation scope item, dependency, or system-state change to one or more `TTC-` test conditions.
- Each `TTC-` must include: scenario description, the technical method (e.g. API call — specify endpoint and verb, DB query — specify table and assertion, log check — specify log key), preconditions, steps, and expected result stated in technical terms.
- Cross-check declared internal and external dependencies against `internal_dependencies.md` and `external_dependencies.md` and add `TTC-` conditions for integration points affected by the enhancement.
- Flag any technical requirement that lacks enough detail to define a verifiable test condition with `❓ [requirement ref]: [clarifying question for TL]`.

### Step 4: Derive Regression Test Conditions

- Read `index.md` to identify baseline scenarios and business rules.
- Identify which baseline behaviors are adjacent to or potentially affected by the enhancement scope.
- For each at-risk baseline behavior, generate one `RTC-` condition.
  - Assign tier `Business` if the regression check is executable without technical tooling.
  - Assign tier `Technical` if the regression check requires API, database, or integration verification.
- Keep the Unchanged Behavior Assertions list current: for each baseline behavior confirmed as outside the enhancement scope, add an assertion.

### Step 5: Populate Capability Impact Analysis

For each ENH-xxx block in `enhancement-test-conditions.md`, fill in the Capability Impact Analysis section:

- Affected business rules or workflows: derived from Business Requirements.
- Affected technical components: derived from Implementation Scope in Technical Requirements.
- Components explicitly not touched: derived from the out-of-scope boundary in Business Requirements and from items in `index.md` not referenced by the enhancement.

### Step 6: Write or update enhancement-test-conditions.md

**If the file does not exist:** create it using the canonical `capability_enhancement_testing_template.md` structure, then populate all sections.

**If the file exists:** for each ENH-xxx block:
- If a block for that ENH-xxx already exists, update it in place. Preserve any existing test conditions that remain valid; add new ones; mark superseded ones with `<!-- superseded by [new TTC/BTC ID] -->` rather than deleting them.
- If no block exists for a new ENH-xxx, append a new block following the template structure.
- Update the Enhancement Test Summary table to include all new IDs.

ID assignment rules:
- `BTC-` IDs are sequential across the entire file (BTC-001, BTC-002, …).
- `TTC-` IDs are sequential across the entire file (TTC-001, TTC-002, …).
- `RTC-` IDs are sequential across the entire file (RTC-001, RTC-002, …).
- Never reuse an ID. If an existing ID is superseded, keep it commented out rather than renumbering.

### Step 7: Update the Enhancement Test Summary table

Ensure every generated `BTC-`, `TTC-`, and `RTC-` ID appears in the top-level Enhancement Test Summary table with:
- Test ID
- Enhancement Ref (ENH-xxx)
- Tier (Business / Technical)
- Test Scope (brief description)
- Status (`draft`)
- Evidence (blank — to be filled by QA)

## Output Summary

At the end of the session, produce a summary table in chat:

| Enhancement ID | BTC Generated | TTC Generated | RTC Generated | ❓ Gaps Found |
|---|---|---|---|---|
| ENH-xxx | [count] | [count] | [count] | [count] |

Then state:
- If no gaps: "`enhancement-test-conditions.md` has been updated for <CapabilityName>. Hand off to QA for execution."
- If gaps exist: "`enhancement-test-conditions.md` has been updated with [N] open gaps. PO and TL should resolve flagged items before QA execution begins."

> Invoked via `/akr-capability enhancement-test-generation [CapabilityName]`. This script is part of the `akr-capability` skill family.
