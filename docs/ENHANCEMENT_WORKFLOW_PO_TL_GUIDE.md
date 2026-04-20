# Enhancement Workflow Guide for Product Owners and Technical Leads

Date: 2026-04-18
Audience: Product Owner (PO), Technical Lead (TL)
Scope: How to prepare `enhancements.md` for a business capability and how to use `akr-capability` plus `capability-promote` to review, close, generate enhancement test conditions, and promote delivered outcomes into the baseline capability artifacts.

---

## Overview

When an active capability has planned changes, those changes are tracked in the capability's `enhancements.md` file. Before any work is handed off to a coding agent or developer, the PO and TL must collaboratively document the intent and technical scope of each enhancement.

This guide is **active-capability only**. If capability status is `new`, use the new-capability definition workflow (`capability-define-review`, `capability-define-close`, `capability-define-clarify`, `capability-promote-new`) instead of the enhancement workflow in this guide.

The workflow uses three `akr-capability` commands plus a final `akr-business-consolidation` promotion command to complete the enhancement lifecycle.

```
Step 1:  /akr-capability enhancement-review [CapabilityName]        ← run as many times as needed
Step 2:  /akr-capability enhancement-review-close [CapabilityName]  ← run once when ready
Step 3:  /akr-capability enhancement-test-generation [CapabilityName]  ← run after close
Step 4:  /akr-business-consolidation capability-promote [CapabilityName]  ← run after delivery acceptance
```

This guide explains how to prepare `enhancements.md` correctly and how each command works so the PO and TL can complete an enhancement cycle from requirement definition through baseline promotion.

---

## Part 1: Preparing enhancements.md

### Where the file lives

For an active capability, the file is located at:

```
docs/business-capabilities/active/<CapabilityName>/enhancements.md
```

`enhancements.md` is only used for active capabilities. Capabilities with status `new` or `archived` do not use this file.

Decision rule before starting:

1. If capability status is `active`, follow this guide.
2. If capability status is `new`, follow the new-capability workflow recommendation and do not create `enhancements.md` until promotion to `active`.

### What the file contains

The file has two main sections:

1. **Enhancement Activity table** — a summary row for each enhancement with ID, brief description, business value, technical notes, status, target release, and a delivery reference.
2. **Enhancement Details** — one subsection per enhancement with the full Business Requirements and Technical Requirements.

---

### Enhancement ID format

Each enhancement is assigned a sequential ID using the prefix `ENH-`:

```
ENH-001, ENH-002, ENH-003 ...
```

IDs are never reused or reordered. When an enhancement is superseded, its entry is updated in place. IDs carry traceability across the enhancements file and the test conditions file.

---

### PO responsibility: Business Requirements

The Business Requirements section is **authored and owned by the Product Owner**. It describes *what* the change must accomplish from a business perspective.

A well-formed Business Requirements section answers:

| Question | Purpose |
|---|---|
| What business outcome does this change achieve? | Grounds the enhancement in a measurable result |
| What are the acceptance criteria a tester can verify? | Enables test derivation |
| What is explicitly out of scope? | Prevents scope creep |
| Are there edge cases, conditional rules, or boundary scenarios? | Catches gaps before coding begins |
| Which roles, users, or downstream processes are affected? | Defines impact and stakeholder review |

**Optional but recommended:** Include a link to the related Azure Boards User Story when one exists. This creates traceability from the enhancement back to the delivery backlog.

Example:

```markdown
#### Azure Boards User Story Link (Optional)
- Azure Boards Work Item: https://dev.azure.com/org/project/_workitems/edit/1234

#### Business Requirements

- When a manager exports a completion report, the file must include a column showing each employee's last training date.
- Acceptance: The exported CSV file must contain the column "Last Training Date" with a valid date value for all active employees.
- Out of scope: Historical reports generated before this release are not affected.
- Edge case: Employees with no recorded training should show "No training recorded" rather than a blank value.
```

---

### TL responsibility: Technical Requirements

The Technical Requirements section is **authored and owned by the Technical Lead**. It describes *how* the change will be implemented at a technical level.

The section has two subsections:

#### Implementation Scope

Document the specific changes to be made. Each item should name the artifact being changed and what is being done to it.

| Item | Example |
|---|---|
| Scripts or modules to update | `services/ReportService.cs` — add `LastTrainingDate` field to export model |
| New scripts, modules, or templates to add | `migrations/AddLastTrainingDateView.sql` |
| Other implementation notes | Azure Function trigger needs max concurrency adjustment |

#### Dependencies and Limitations

Cross-reference the capability's dependency documents when completing these.

| Item | Example |
|---|---|
| Internal dependencies | UserManagement capability — queries the `Users` table |
| External dependencies | Azure Blob Storage — output file written to the shared reports container |
| Technical limitations or constraints | Export file size is capped at 10 MB by current infrastructure |

A well-formed Technical Requirements section gives the `enhancement-review` skill enough detail to:
- Score implementation completeness
- Suggest specific files and integration points that may be affected
- Recommend whether the work is suitable for a Copilot coding agent or requires human developer involvement

---

### Completed example: ENH-001 in enhancements.md

```markdown
### ENH-001: Add Last Training Date to Manager Completion Report Export

#### Azure Boards User Story Link (Optional)
- Azure Boards Work Item: https://dev.azure.com/org/project/_workitems/edit/1234

#### Business Requirements

- When a manager exports a completion report, the file must include a column showing each employee's last training date.
- Acceptance: The exported CSV file contains a "Last Training Date" column with a valid date or "No training recorded" for each active employee.
- Out of scope: Historical report formats and scheduled reports are not affected by this change.
- Edge case: Employees with no recorded training must show "No training recorded" rather than a blank cell.
- Affected roles: Managers with export permissions.

#### Technical Requirements

##### Implementation Scope

- Expected scripts, modules, or templates to update: `services/ReportService.cs` — add `LastTrainingDate` field to report DTO and query logic
- Expected new scripts, modules, or templates to add: `migrations/AddLastTrainingDateView.sql` — view to surface last training date per employee
- Other implementation notes: Export controller action must pass new field to existing CSV serializer

##### Dependencies and Limitations

- Internal dependencies: EnrollmentManagement capability — training completion data sourced from enrollment records
- External dependencies: None for this change
- Technical limitations or constraints: CSV export limit of 10 MB; large employee sets may require pagination in a follow-on enhancement
```

---

## Part 2: Using the akr-capability Skills

### Command 1 — enhancement-review (iterative)

```
/akr-capability enhancement-review [CapabilityName]
```

**When to run:** After the PO has filled in the Business Requirements and the TL has filled in the Technical Requirements for one or more enhancements.

**What it does:**

1. Reads `enhancements.md`, `index.md`, `limitations.md`, `internal_dependencies.md`, and `external_dependencies.md`.
2. Evaluates the Business Requirements against six criteria (outcome clarity, acceptance conditions, scope boundary, edge cases, stakeholder impact, traceability).
3. Evaluates the Technical Requirements against eight criteria (implementation scope, change rationale, internal dependencies, external dependencies, known limitations, new artifact identification, security/data considerations, testability).
4. Cross-checks declared scope against the capability baseline in `index.md` to identify regression risk.
5. Proposes implementation suggestions (advisory — TL may confirm or dismiss).
6. Computes a **Readiness Score** (0–2 scale) and a **Complexity Score** (0–2 scale).
7. Produces a **Routing Recommendation**:

| Readiness | Complexity | Routing Decision |
|---|---|---|
| Green (1.6–2.0) | Low | ✅ Copilot coding agent ready |
| Green | Moderate | ✅ Copilot coding agent ready with TL review checkpoint |
| Green | High | ⚠️ Copilot-assisted — developer supervision required |
| Amber (1.0–1.59) | Low | ⚠️ Copilot-assisted — resolve amber gaps first |
| Amber | Moderate | ⚠️ Copilot-assisted — developer supervision required |
| Amber | High | 🚫 Human developer required |
| Red (0–0.99) | Any | 🚫 Human developer required |

8. Writes a `#### Enhancement Review` block directly into `enhancements.md` for each assessed ENH-xxx entry, including all gaps, suggestions, a required actions checklist, and the routing recommendation.

**How to use iteratively:**

- After the first run, review the open gaps listed in the Review block.
- The PO updates the Business Requirements to address any business-side gaps.
- The TL updates the Technical Requirements to address any technical-side gaps.
- Run `/akr-capability enhancement-review [CapabilityName]` again.
- On each subsequent run, the skill detects previously raised gaps, marks resolved ones as `✅ Resolved`, and updates the iteration counter.
- Continue until no open gaps remain and all required actions are checked.

---

### Command 2 — enhancement-review-close

```
/akr-capability enhancement-review-close [CapabilityName]
```

**When to run:** After all open gaps are resolved, all required action checklist items are checked, and the PO and TL are satisfied with the requirements.

**What it does:**

1. Validates that every reviewed ENH-xxx has:
   - No open Business Requirements gaps
   - No open Technical Requirements gaps
   - All required action items checked (`[x]`)
   - A routing decision that is not 🚫 (unless an explicit override was recorded)
2. Presents a close-readiness table in chat showing each enhancement's status.
3. If any enhancement is not ready, lists what remains to be resolved and stops without modifying the file.
4. If all enhancements are ready, asks for explicit confirmation: **type "confirm" to proceed**.
5. On confirmation, removes all `#### Enhancement Review` blocks from `enhancements.md`, leaving only the clean business and technical requirements the PO and TL wrote.
6. Updates the Status column in the Enhancement Activity table to `Review Closed`.

**Important:** This command only runs once per review cycle. The resulting `enhancements.md` is the clean source of truth for coding handoff. Running `enhancement-review` again after close starts a new review cycle.

---

### Command 3 — enhancement-test-generation

```
/akr-capability enhancement-test-generation [CapabilityName]
```

**When to run:** After `enhancement-review-close` has completed successfully.

**What it does:**

1. Reads the closed `enhancements.md` and derives three tiers of test conditions for each ENH-xxx:

   - **Business Test Conditions (BTC-\*):** Derived from the Business Requirements. Written in plain language. Executable by a business user or non-technical QA tester. Covers business rules, observable outcomes, and acceptance criteria.
   - **Technical Test Conditions (TTC-\*):** Derived from the Technical Requirements. Executable by a QA tester with technical expertise. Includes a Technical Method column specifying the API endpoint, database query, log key, or integration assertion to use.
   - **Regression Test Conditions (RTC-\*):** Identifies baseline behaviors that are adjacent to or potentially affected by the enhancement. Confirms existing behavior remains unchanged after the change is delivered.

2. Fills in a Capability Impact Analysis section per ENH-xxx block identifying affected business rules and workflows.

3. Creates or updates `enhancement-test-conditions.md` in the capability folder.

**POC note:** For this proof-of-concept, execution testing activities may be deferred. If test execution is deferred, retain generated enhancement test conditions for later execution and complete promotion after business/technical acceptance using Command 4.

**Test ID format:**

| Prefix | Tier | Example |
|---|---|---|
| `BTC-` | Business Test Condition | BTC-001 |
| `TTC-` | Technical Test Condition | TTC-001 |
| `RTC-` | Regression Test Condition | RTC-001 |

IDs are sequential and never reused. If a test condition is superseded, it is commented out rather than deleted so the ID remains reserved.

---

### Command 4 — capability-promote

```
/akr-business-consolidation capability-promote [CapabilityName]
```

**When to run:** After code changes are delivered and accepted by both business and technical owners. In the full workflow, run after enhancement testing is complete. In this POC, if testing execution is out of scope, promotion may proceed with deferred test-merge notes.

**What it does:**

1. Reads promotion candidates from `enhancements.md` (and optionally `backlog.md`) using `Delivery Reference` values.
2. May also transition confirmed backlog items from `backlog.md` into the active enhancement queue before promotion proceeds.
3. Requests explicit confirmation of delivered/closed items, PO/TL acceptance, and whether testing is complete for each accepted item.
4. Promotes delivered enhancement behavior into `index.md` as the new baseline capability behavior.
5. Updates `limitations.md`, `internal_dependencies.md`, and `external_dependencies.md` when delivered enhancements changed constraints or dependencies.
6. If testing is complete, merges promoted enhancement tests from `enhancement-test-conditions.md` (`BTC-*`, `TTC-*`, `RTC-*`) into baseline `test-conditions.md` with next available `TC-*` IDs.
7. If testing is not complete or is out of scope for the proof-of-concept, records deferred test-merge notes and still synchronizes the delivered business baseline.
8. Synchronizes promoted rows in `enhancements.md` and reports promotion summary notes, including skipped or deferred items.

**Important:** This command is the cycle-closing step for delivered enhancements. Testing completion is confirmed manually during the prompt flow; it is not inferred from repository artifacts in the current proof-of-concept. Once promotion is complete, `index.md` and companion baseline artifacts are the source of truth for current capability behavior.

---

## Part 3: End-to-End Workflow Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│ PO authors Business Requirements in enhancements.md               │
│ TL authors Technical Requirements in enhancements.md              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ /akr-capability enhancement-review [CapabilityName]                   │
│                                                                     │
│  → Evaluates Business and Technical Requirements                   │
│  → Surfaces gaps with clarifying questions                         │
│  → Scores readiness and complexity                                 │
│  → Writes routing recommendation into enhancements.md             │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                         gaps found?
                      ┌────────┴───────┐
                     yes              no
                      │               │
                      ▼               │
               PO/TL address          │
               gaps and               │
               update file            │
                      │               │
                      └───────┬───────┘
                              │
                    run enhancement-review
                    again until no gaps
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ /akr-capability enhancement-review-close [CapabilityName]             │
│                                                                     │
│  → Validates all gaps resolved, all actions checked                │
│  → Asks for explicit "confirm"                                     │
│  → Strips review blocks → clean enhancements.md                   │
│  → Status updated to "Review Closed"                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ /akr-capability enhancement-test-generation [CapabilityName]          │
│                                                                     │
│  → Derives BTC- (business) test conditions                        │
│  → Derives TTC- (technical) test conditions                       │
│  → Derives RTC- (regression) test conditions                      │
│  → Produces enhancement-test-conditions.md for QA handoff         │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
   Code delivered + accepted by business and technical teams?
            ┌──────────┴───────────┐
           no                     yes
            │                      │
            ▼                      │
       continue delivery/acceptance      │
       activities                        │
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│ /akr-business-consolidation capability-promote [CapabilityName]    │
│                                                                     │
│  → Promotes delivered enhancement behavior into index.md           │
│  → Updates limitations and dependency baselines as needed          │
│  → Merges enhancement tests into baseline tests when complete      │
│  → Synchronizes enhancement delivery state                         │
└──────────────────────────────┬──────────────────────────────────────┘
                │
                ▼
      Enhancement cycle closed and baseline artifacts refreshed
```

---

## Part 4: Tips for the PO

- Fill in the Business Requirements before asking the TL to start the Technical Requirements. Requirements drive technical scope, not the other way around.
- Write acceptance criteria as testable statements: "The system must..." or "When X happens, the result must be Y."
- Include edge cases proactively. The `enhancement-review` skill will flag missing edge cases as gaps, so addressing them in advance reduces review iterations.
- The Azure Boards work item link is optional but strongly recommended. It creates a direct audit trail from the enhancement back to the delivery backlog.
- You may run `enhancement-review` as many times as needed before closing. There is no cost to extra iterations.
- Before running `capability-promote`, confirm in writing that business acceptance is complete for each delivered ENH-* candidate.
- Be prepared to answer whether testing is complete for each accepted enhancement. In the current proof-of-concept this confirmation is manual and can result in deferred baseline test merge notes.

---

## Part 5: Tips for the TL

- Cross-reference `internal_dependencies.md` and `external_dependencies.md` when filling in the Dependencies and Limitations subsection. The `enhancement-review` skill compares your declared dependencies against those documents and flags uncovered integration points.
- Name specific artifacts in the Implementation Scope. Vague entries like "update the service" will score lower than "update `services/ReportService.cs` to include the new export field."
- Security, authentication, and data handling changes score as High complexity. If the enhancement touches access control, data classification, or external API authentication, declare it explicitly so the routing recommendation reflects the true risk.
- If the routing recommendation comes back as 🚫 Human developer required and you believe a Copilot coding agent can handle it with supervision, you may fill in the Override Record section in the Review block to record your rationale and approver name before running `enhancement-review-close`.
- Before running `capability-promote`, confirm technical acceptance and validate whether dependency or limitation baselines must be amended.
- If backlog items are ready to move into active delivery tracking, use the promotion workflow prompt to transition them from `backlog.md` into `enhancements.md` before the next coding cycle starts.

---

## Part 6: Governance Reminders

- `enhancements.md` belongs to active capabilities only. If a capability's status is `new` or `archived`, this workflow does not apply.
- The `enhancement-review-close` step is required before any enhancement work is handed off to a coding agent. A clean `enhancements.md` (no open review blocks) is the signal that requirements are approved.
- `enhancement-test-conditions.md` is separate from `test-conditions.md`. Baseline test conditions live in `test-conditions.md`. Enhancement-specific test conditions live in `enhancement-test-conditions.md`. After delivery, the `capability-promote` skill merges enhancement tests into the baseline only when testing completion is confirmed.
- Test condition IDs (BTC-, TTC-, RTC-) are permanent. Once assigned, they are never renumbered, even if an enhancement is later superseded.
- `capability-promote` is the cycle-closing step after delivery acceptance; it promotes delivered outcomes into `index.md` and updates baseline dependency/limitation artifacts as needed.
- For this POC, testing execution may be out of scope. If so, promotion may proceed with explicit deferred test-merge notes and a follow-up action to complete baseline test merge later. The prompt flow relies on human confirmation rather than a dedicated testing-completion artifact.
