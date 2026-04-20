# enhancement-readiness-review

## Purpose

Assess the quality and completeness of business and technical requirements declared for each enhancement entry in an active capability's `enhancements.md`. Surface gaps the PO or TL may have missed, propose implementation guidance, and produce a per-enhancement routing recommendation that determines whether the coding task can be assigned to a Copilot coding agent or requires human developer involvement.

## Status applicability

**Active capabilities only.** Enforced by dispatcher pre-check in `SKILL.md`.

## Inputs

- `enhancements.md` (primary — the artifact being assessed)
- `index.md` (baseline behavior reference for impact and regression scope)
- `limitations.md` (known constraints that may affect feasibility)
- `internal_dependencies.md` (cross-capability change impact within the application)
- `external_dependencies.md` (cross-application interface impact)

## Required metadata checks

Validate metadata using `SKILL.md` section **Required Metadata and Governance**.
Do not write output if any metadata check fails; report failures with `❓`.

## Execution Steps

Execute these steps in order for each ENH-xxx entry found in `enhancements.md`.

### Step 1: Locate enhancement entries

- Read the Enhancement Activity table to identify all ENH-xxx IDs with non-placeholder values.
- Skip entries where Description, Business Value, and Status are all still `NEEDS` — report them as not yet started.
- For each active entry, proceed to the following steps.

### Step 2: Assess Business Requirements quality

For each enhancement, evaluate the Business Requirements section authored by the PO using these criteria.

| Criterion | Check | Severity if missing |
|---|---|---|
| Outcome clarity | Is the desired business outcome stated in measurable terms? | High |
| Acceptance criteria | Are acceptance conditions explicit enough for a tester to verify? | High |
| Scope boundary | Is out-of-scope behavior explicitly stated? | Medium |
| Edge case coverage | Are conditional, exceptional, or boundary scenarios addressed? | Medium |
| Stakeholder impact | Are affected roles, users, or downstream processes named? | Low |
| Traceability | Is an Azure Boards work item link present (optional but expected)? | Low — advisory only |

Mark each missing criterion with `❓ [criterion name]: [clarifying question for PO]`.

### Step 3: Assess Technical Requirements quality

For each enhancement, evaluate the Technical Requirements section authored by the TL using these criteria.

| Criterion | Check | Severity if missing |
|---|---|---|
| Implementation scope | Are the specific scripts, modules, or templates to update or add named? | High |
| Change rationale | Is there a clear link between each technical change and a specific business requirement? | High |
| Internal dependencies | Are all in-application capability dependencies declared? Cross-check against `internal_dependencies.md`. | High |
| External dependencies | Are all cross-application integration points declared? Cross-check against `external_dependencies.md`. | High |
| Known limitations | Are any known technical constraints or limitations that affect this enhancement declared? Cross-check against `limitations.md`. | Medium |
| New artifact identification | If new files or modules are required, are they named and their purpose described? | Medium |
| Security and data considerations | Are data handling, authentication, or authorization impacts noted if applicable? | Medium |
| Testability | Are the technical changes described in enough detail for the QA team to derive test conditions? | Medium |

Mark each missing criterion with `❓ [criterion name]: [clarifying question for TL]`.

### Step 4: Cross-check against capability baseline

- Read `index.md` to identify existing business rules, scenarios, and behaviors.
- Identify which baseline behaviors are directly touched by this enhancement.
- Identify which baseline behaviors are adjacent but should remain unchanged.
- Flag any baseline behavior that could regress without being covered by the declared technical scope.

Use `🤖` to mark inferred cross-check findings that the TL must confirm.

### Step 5: Propose implementation guidance

Based on the declared technical requirements and the baseline cross-check, produce a list of implementation suggestions.

For each suggestion:
- State the specific script, module, template, or integration point involved.
- Explain why it is likely to be affected.
- Mark as `confirmed by declared requirements` or `🤖 inferred — requires TL confirmation`.

Do not treat suggestions as requirements. They are advisory until the TL confirms them.

### Step 6: Compute readiness score

Score the enhancement against these five dimensions. Each dimension is rated 0–2 (0 = missing or inadequate, 1 = partial, 2 = complete and clear).

| Dimension | Weight | Score (0–2) |
|---|---|---|
| Business requirement clarity | 25% | |
| Technical specification completeness | 20% | |
| Dependency and limitation coverage | 20% | |
| Regression and impact certainty | 20% | |
| Traceability and evidence quality | 15% | |

Weighted score = sum of (score × weight) across all dimensions.
Maximum possible weighted score = 2.0.

Interpret result:

| Weighted Score | Readiness Band |
|---|---|
| 1.6 – 2.0 | Green — High readiness |
| 1.0 – 1.59 | Amber — Moderate readiness |
| 0 – 0.99 | Red — Low readiness |

### Step 7: Compute complexity score

Score the enhancement across these complexity dimensions. Each is rated 0–2 (0 = low, 1 = moderate, 2 = high).

| Dimension | Score (0–2) |
|---|---|
| Number of files or modules affected |  |
| Presence of external integration changes |  |
| Security, authentication, or data handling changes |  |
| Cross-capability impact (internal dependencies affected) |  |
| Degree of ambiguity remaining after Steps 2–3 |  |

Complexity score = average of all dimension scores.

Interpret result:

| Average Score | Complexity Band |
|---|---|
| 0 – 0.8 | Low |
| 0.81 – 1.4 | Moderate |
| 1.41 – 2.0 | High |

### Step 8: Produce routing recommendation

Apply this decision matrix using the Readiness Band and Complexity Band.

| Readiness | Complexity | Routing Decision |
|---|---|---|
| Green | Low | ✅ Copilot coding agent ready |
| Green | Moderate | ✅ Copilot coding agent ready with TL review checkpoint |
| Green | High | ⚠️ Copilot-assisted — developer supervision required |
| Amber | Low | ⚠️ Copilot-assisted — resolve amber gaps first |
| Amber | Moderate | ⚠️ Copilot-assisted — developer supervision required |
| Amber | High | 🚫 Human developer required |
| Red | Any | 🚫 Human developer required |

Routing decisions are advisory. PO and TL may override after reviewing the full assessment.

### Step 9: Write Review Outcome block into enhancements.md

Append the following block immediately after the **Dependencies and Limitations** subsection of the assessed ENH-xxx entry in `enhancements.md`. Do not overwrite any existing content.

```markdown
#### Enhancement Readiness Review

Assessed: [date]
Assessed by: akr-capability v1.0.0

**Readiness Score:** [weighted score] / 2.0 — [Green / Amber / Red]
**Complexity Score:** [average score] / 2.0 — [Low / Moderate / High]
**Routing Decision:** [✅ / ⚠️ / 🚫] [decision label]

##### Open Gaps — Business Requirements

<!-- One line per ❓ gap identified in Step 2. Remove when resolved. -->
- ❓ [criterion]: [clarifying question]

##### Open Gaps — Technical Requirements

<!-- One line per ❓ gap identified in Step 3. Remove when resolved. -->
- ❓ [criterion]: [clarifying question]

##### Implementation Suggestions

<!-- 🤖 marks inferred suggestions pending TL confirmation. -->
- 🤖 [suggestion]: [rationale]

##### Required Actions Before Coding Handoff

<!-- PO and TL must sign off on all items here before a coding agent is invoked. -->
- [ ] [action item for PO or TL]

##### Override Record (Optional)

If the routing decision is overridden, record the rationale and the name of the approver here.

- Override decision: N/A
- Rationale: N/A
- Approved by: N/A
```

If there are no open gaps in a category, write `None identified.` for that section rather than leaving it empty.

## Output Summary

At the end of the full assessment session, produce a summary table in chat:

| Enhancement ID | Readiness | Complexity | Routing Decision | Critical Gaps |
|---|---|---|---|---|
| ENH-xxx | Green / Amber / Red | Low / Moderate / High | [decision] | [count] |

Then state: "Review Outcome blocks have been written into `enhancements.md`. PO and TL must resolve all open gaps and confirm required actions before invoking a coding agent."

> This script is part of the `akr-capability` skill family. Additional mode scripts will be added to `.github/skills/akr-capability/scripts/` as new capabilities are introduced.
