# enhancement-review

## Purpose

Assess the quality and completeness of business and technical requirements declared for each enhancement entry in an active capability's `enhancements.md`. Surface gaps the PO or TL may have missed, propose implementation guidance, and produce a per-enhancement routing recommendation that determines whether the coding task can be assigned to a Copilot coding agent or requires human developer involvement.

The review is intended to make coding handoff clear without over-prescribing the internal design. Prefer stable implementation anchors such as UI surfaces, API contracts, data entities, integration points, batch jobs, or module areas. Exact file, class, or script names are helpful when already known, but they are not required unless a specific internal choice is mandated by an existing architectural, security, compliance, performance, or platform constraint.

This mode supports iterative execution. Each run re-evaluates only the gaps that remain open from a prior run, updates scores, and replaces the existing Review Outcome block in place. Resolved gaps are acknowledged. New gaps found in updated content are added. The iteration counter increments on every run.

When all gaps are resolved and the PO and TL are satisfied, run `enhancement-review-close` to confirm the review is complete and remove all review blocks for a clean `enhancements.md`.

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

### Step 1: Locate enhancement entries and detect run mode

- Read the Enhancement Activity table to identify all ENH-xxx IDs with non-placeholder values.
- Skip entries where Description, Business Value, and Status are all still `NEEDS` — report them as not yet started.
- For each active entry, check whether an `#### Enhancement Review` block already exists inside that entry.
  - If **no** block exists → this is a **fresh run** (Iteration 1). Proceed from Step 2.
  - If a block **exists** → this is an **iterative run**. Read the existing block to extract:
    - Current iteration number
    - Open gaps still listed under Business Requirements and Technical Requirements
    - Required Actions checklist state (checked vs unchecked)
    - Current routing decision
  - In iterative mode, Steps 2 and 3 assess **only the areas that changed** since the last run. Check whether the PO/TL updated content in the Business Requirements or Technical Requirements sections and re-evaluate accordingly. Do not re-raise gaps the PO/TL have already addressed in their content updates.

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

In iterative runs:
- For each criterion that was previously marked `❓`: check whether the updated content now satisfies it. If yes, mark it `✅ Resolved`.
- Only raise a new `❓` if the criterion is still unaddressed or if new content introduced a new gap.

### Step 3: Assess Technical Requirements quality

For each enhancement, evaluate the Technical Requirements section authored by the TL using these criteria.

| Criterion | Check | Severity if missing |
|---|---|---|
| Implementation scope | Are the affected implementation anchors named clearly enough to begin coding (for example UI surface, API contract, data entity, integration point, batch job, or module area)? Exact file or class names are optional when not yet stable. | High |
| Change rationale | Is there a clear link between each technical change and a specific business requirement or success condition? | High |
| Internal dependencies | Are all in-application capability dependencies declared? Cross-check against `internal_dependencies.md`. | High |
| External dependencies | Are all cross-application integration points declared? Cross-check against `external_dependencies.md`. | High |
| Known limitations | Are any known technical constraints or limitations that affect this enhancement declared? Cross-check against `limitations.md`. | Medium |
| New artifact identification | If new artifacts are required, is their purpose and boundary described clearly enough for implementation and testing? Exact names are recommended only when already decided. | Medium |
| Security and data considerations | Are data handling, authentication, or authorization impacts noted if applicable? | Medium |
| Testability | Are the technical changes described in enough detail for the QA team to derive test conditions from observable behavior, contracts, and data state even if internal design choices remain open? | Medium |
| Design freedom guardrail | Does the technical scope avoid mandating internal design choices without a stated architectural, security, compliance, performance, or platform reason? | Low — advisory |

Apply the same iterative resolution logic as Step 2.

Apply these review rules during Step 3:

- Prefer stable component anchors over exact file paths when the implementation can reasonably be completed in more than one internal location.
- Treat preferred implementation approaches as guidance unless the TL explicitly states why that choice is mandatory.
- Raise a gap only when the requirements leave the coding agent without a reliable implementation anchor or without enough behavioral clarity to prove success.
- If the Technical Requirements appear over-constrained, record that as an advisory note rather than a coding blocker unless the over-constraint would create delivery risk or contradict stated requirements.

### Step 4: Cross-check against capability baseline

- Read `index.md` to identify existing business rules, scenarios, and behaviors.
- Identify which baseline behaviors are directly touched by this enhancement.
- Identify which baseline behaviors are adjacent but should remain unchanged.
- Flag any baseline behavior that could regress without being covered by the declared technical scope, success criteria, or dependency handling.

In iterative runs, only re-run this step if the Technical Requirements section was updated since the last run.

Use `🤖` to mark inferred cross-check findings that the TL must confirm.

### Step 5: Propose implementation guidance

Based on the declared technical requirements and the baseline cross-check, produce a list of implementation suggestions.

For each suggestion:
- State the most reliable implementation anchor involved. Use exact file, class, or script names only when they are explicitly declared or clearly established by surrounding context.
- Explain why it is likely to be affected.
- Mark as `confirmed by declared requirements` or `🤖 inferred — requires TL confirmation`.

In iterative runs, carry forward previously listed suggestions that are still valid. Add new ones only if updated content reveals additional scope. Do not repeat suggestions already confirmed by the TL.

Do not treat suggestions as requirements. They are advisory until the TL confirms them.

If the TL has described a preferred internal implementation path without a stated mandatory reason, preserve that detail as guidance rather than converting it into a readiness gate.

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

### Step 9: Write or replace the Review Outcome block in enhancements.md

**Fresh run:** Append the Review Outcome block immediately after the **Dependencies and Limitations** subsection of the assessed ENH-xxx entry.

**Iterative run:** Replace the entire existing `#### Enhancement Review` block in place. Do not leave any remnant of the previous block. The replacement must include the incremented iteration number and a delta summary.

Use this block structure:

```markdown
#### Enhancement Review

<!-- akr-capability: review-in-progress -->
Iteration: [N]
Last assessed: [date]
Assessed by: akr-capability v1.0.0

**Readiness Score:** [weighted score] / 2.0 — [Green / Amber / Red]
**Complexity Score:** [average score] / 2.0 — [Low / Moderate / High]
**Routing Decision:** [✅ / ⚠️ / 🚫] [decision label]

##### Changes Since Last Iteration
<!-- Omit this section on Iteration 1 -->
- Resolved: [list of criteria marked ✅ Resolved this run, or "None"]
- Newly raised: [list of new ❓ gaps added this run, or "None"]

##### Open Gaps — Business Requirements

<!-- One line per unresolved ❓ gap. Remove the entire section if none remain. -->
- ❓ [criterion]: [clarifying question]

##### Open Gaps — Technical Requirements

<!-- One line per unresolved ❓ gap. Remove the entire section if none remain. -->
- ❓ [criterion]: [clarifying question]

##### Implementation Suggestions

<!-- 🤖 marks inferred suggestions pending TL confirmation. Remove confirmed items. -->
- 🤖 [suggestion]: [rationale]

##### Required Actions Before Coding Handoff

<!-- Check off items as they are completed. All must be checked before review-close. -->
- [ ] [action item for PO or TL]

##### Resolved Items Disposition

<!-- Populated as Q&G and D&R items are resolved during review iterations.
     Each resolved item must have a destination declared before review-close.
     enhancement-review-close uses this table to promote content into requirements and clean up source sections.
     Destination values: "Business Requirements" | "Technical Requirements > Other implementation notes" | "Technical Requirements > Dependencies and Limitations" | "Already incorporated — remove only" -->
| Source Section | Item Summary | Destination | Normalized Statement |
|---|---|---|---|
| Questions and Gaps | [brief label] | [destination] | [requirement-style statement to insert, or "N/A" if already incorporated] |

##### Override Record (Optional)

If the routing decision is overridden, record the rationale and the name of the approver here.

- Override decision: N/A
- Rationale: N/A
- Approved by: N/A
```

Rules:
- If there are no open gaps in a category, write `None identified.` for that section rather than leaving it empty.
- The `<!-- akr-capability: review-in-progress -->` marker is used by `enhancement-review-close` to locate and remove review blocks. Do not remove or alter it.

## Output Summary

At the end of the full assessment session, produce a summary table in chat:

| Enhancement ID | Iteration | Readiness | Complexity | Routing Decision | Open Gaps | All Actions Checked |
|---|---|---|---|---|---|---|
| ENH-xxx | N | Green / Amber / Red | Low / Moderate / High | [decision] | [count] | Yes / No |

Then state one of:
- If open gaps remain: "Review Outcome blocks updated in `enhancements.md` (Iteration N). [X] gaps remain open. PO and TL should address them and re-run `/akr-capability enhancement-review [CapabilityName]`."
- If no gaps remain and all actions are checked: "No open gaps detected. All required actions are checked. Run `/akr-capability enhancement-review-close [CapabilityName]` to confirm the review is complete and clean the enhancements file."

> Invoked via `/akr-capability enhancement-review [CapabilityName]`. This script is part of the `akr-capability` skill family. Additional mode scripts will be added to `.github/skills/akr-capability/scripts/` as new capabilities are introduced.
