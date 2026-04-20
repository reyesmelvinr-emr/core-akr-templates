# New Capability Workflow — Design Recommendation

Date: 2026-04-18
Status: Recommendation — for review by PO, TL, and architecture owner
Scope: Defines an optimal workflow for `new` businessCapability 

## Fundamental Design Shift: PO/TL as Direct Authors

For `new` capabilities, the PO and TL **directly author** the canonical capability folder
artifacts using the same existing canonical templates. No staging file, no intermediate
transformation by a skill. The `new/<CapabilityName>/` folder and its artifact set are
populated by PO/TL before any skill runs:

| Artifact | Author | Content nature |
|---|---|---|
| `index.md` | PO | Forward-looking: what the capability *will* do, written in the same format as an active `index.md` — `SCN-*` scenarios, business rules, acceptance conditions, edge cases, out-of-scope boundaries. Also includes Azure Boards work item link(s) and key TL technical decision statements for traceability. |
| `test-conditions.md` | PO/TL jointly | Planned `TC-*` conditions — PO authors business-tier conditions, TL authors technical-tier conditions |
| `limitations.md` | TL | Anticipated business, technical constraints, infrastructure limits, known design boundaries |
| `internal_dependencies.md` | TL | Planned integration touchpoints with other capabilities in the application, cross-referenced against the capability registry |
| `external_dependencies.md` | TL | Planned integration touchpoints with external systems, APIs, or platforms |


### POC authoring sequence for joint `test-conditions.md`

To reduce PO/TL deadlocks during this proof of concept:

1. PO drafts business-tier `TC-*` conditions first.
2. TL appends technical-tier `TC-*` conditions second.
3. PO and TL run one reconciliation pass.
4. If wording conflicts remain:
  - PO decides acceptance/business wording.
  - TL decides technical feasibility wording.

Unresolved points must be captured as explicit assumptions before `capability-define-close`.

### POC format for TL technical decision statements in `index.md`

At least one TL technical decision statement is required before close. Use this minimum format:

```markdown
TD-001
- Decision: [what is being chosen]
- Rationale: [why this choice is being made]
- Constraints/Implications: [what this enables, limits, or defers]
```

This lightweight format is intentionally POC-oriented and can evolve after management/team feedback.


The `capability-define-review` and `capability-define-close` skills assess and validate the
content of these files as PO/TL author them — fulfilling the same governance role as
`enhancement-review` and `enhancement-review-close` in the `active` workflow.

---

## 1. Recommended Workflow: `capability-define` Skill Family

### Workflow Name

`capability-define` — added to the `akr-capability` skill family specifically for `new` capabilities.

### Invocation pattern (consistent with existing skills)

```
/akr-capability capability-define-review [CapabilityName]        ← PO/TL: iterate until gaps resolved
/akr-capability capability-define-close [CapabilityName]         ← PO/TL: validate and close
/akr-capability capability-define-clarify [CapabilityName]       ← Developer: pre-coding scope confirmation
```

Post-delivery:

```
/akr-business-consolidation capability-promote-new [CapabilityName]   ← PO/TL: promote new → active
```

Mapping to the existing `akr-capability` sequence:

| Existing (active) | New (new) | Key difference |
|---|---|---|
| `enhancement-review` | `capability-define-review` | Reads directly from canonical `new/` artifacts instead of `enhancements.md` |
| `enhancement-review-close` | `capability-define-close` | Closes review blocks in `index.md` rather than in `enhancements.md` |
| `enhancement-test-generation` | No equivalent | `test-conditions.md` is PO/TL-authored, not skill-generated |
| `enhancement-clarify` | `capability-define-clarify` | No baseline contrast — reads `new/` artifacts as the planned target state |

---

## 2. Phase Map — Where This Workflow Fits

`capability-consolidation` (Phase C) is **not in the path** for `new` capabilities. The PO/TL
author the canonical artifacts directly. Phase C runs for the first time against this capability
only after it is promoted to `active` and source-repo module docs have been created.

| Phase | Name | Skill(s) | Status applicability |
|---|---|---|---|
| A | Define | Human-led registry setup + PO/TL direct artifact authoring | All |
| **A-1** | **New Capability Definition** | `capability-define-review` → `capability-define-close` → `capability-define-clarify` | **New only** |
| A-0 | Enhancement Assessment | `enhancement-review` → ... → `enhancement-clarify` | Active only |
| B | Assess | `capability-coverage-review`, `capability-impact-analysis` (reduced scope) | All |
| C | Consolidate | `capability-consolidation` | **Active and archived only — not new** |
| D | Promote delivered enhancements | `capability-promote` | Active only |
| **D-1** | **Promote New → Active** | `capability-promote-new` | **New only** |
| E | Maintain tests | `capability-test-maintenance` | Active only |
| F | Generate enhancement tests | `enhancement-test-generation` | Active only |
| G | Explain | `capability-relationship-mapping` | All |

**Phase B for `new` capabilities (reduced scope):**
- `capability-coverage-review` validates that the PO/TL-authored artifact set is sufficiently
  complete and internally consistent before development begins.
- `capability-impact-analysis` checks whether the planned new capability has impact on existing
  active capabilities through declared internal and external dependency records.
- `capability-consolidation` is **skipped** — no source-repo module docs exist to consolidate.

---



## 3. Skill Design: Each Step in Detail

---

### Step 1 — `capability-define-review` (PO/TL, iterative)

**Parallel to:** `enhancement-review`

**When to run:** After PO and TL have authored the initial versions of the `new` capability
artifacts directly in `docs/business-capabilities/new/[CapabilityName]/`. `index.md` must
exist before the skill will run.

**What it reads:**

All present artifacts in `new/[CapabilityName]/`:
- `index.md` (required to run)
- `test-conditions.md` (if present)
- `limitations.md` (if present)
- `internal_dependencies.md` (if present)
- `external_dependencies.md` (if present)

Note: `traceability.md` is **not part of the `new` capability artifact set**. Source-evidence
traceability cannot be written before code exists. Traceability anchors for `new` capabilities
are captured directly in `index.md` — Azure Boards work item links, PO acceptance conditions,
and TL technical decisions — and are evaluated as part of the `index.md` assessment below.

**What it evaluates:**

**Business content** (PO-owned — across `index.md` and `test-conditions.md`):
- Business purpose and user need clarity
- User roles and actor identification
- Key business scenarios — minimum three `SCN-*` candidate entries in `index.md`
- Acceptance conditions — at least one testable condition per scenario
- Out-of-scope boundary statements
- Edge cases and conditional rules
- Azure Boards Epic or User Story link — at least one work item link present in `index.md`
  for delivery traceability (flagged as a gap if absent, not a blocker)

**Technical content** (TL-owned — across `limitations.md`, `internal_dependencies.md`,
`external_dependencies.md`, and technical sections in `index.md`):
- New artifacts to be created — named at layer level (UI / API / Database)
- Integration points with existing capabilities — cross-referenced against capability registry
- Integration points with external systems — named and typed
- Known technical constraints — with workaround notes if applicable
- Authentication, authorization, and data-handling considerations
- Testability of the declared `test-conditions.md` scope
- New infrastructure or configuration requirements
- Key TL technical decisions documented in `index.md` — rationale for significant design
  choices that will ground post-promotion consolidation (flagged as a gap if absent)
- Routing assessment: is this scope suitable for a Copilot coding agent?


**Readiness and routing:** Computes a **Definition Readiness Score** (same 0–2 scale as
`enhancement-review`) and a **Complexity Score**. Produces a **Routing Recommendation**
using the identical decision table as `enhancement-review`. Reuse without modification.

**Output written to file:** Writes a `#### Capability Definition Review` block into `index.md`
(as the primary authored artifact — same pattern as `#### Enhancement Review` in
`enhancements.md`), including all gaps, suggestions, required actions checklist, and routing
recommendation.

**Iteration:** Supports multiple runs with delta tracking. On re-run, previously raised gaps
are checked for resolution and marked `✅ Resolved` or left open.

---

### Step 2 — `capability-define-close` (PO/TL, once per definition cycle)

**Parallel to:** `enhancement-review-close`

**When to run:** After all gaps in the Definition Review block are resolved, all required
action items are checked, and PO and TL are satisfied with the full artifact set.

**What it does:**

1. Validates that `index.md` contains no open `#### Capability Definition Review` blocks.
2. Validates that all required action items in the review checklist are checked.
3. Validates that the routing decision is not 🚫 (unless an explicit override was recorded).
4. Validates that `test-conditions.md` exists and has at least one `TC-*` entry.
5. Validates that `index.md` contains at least one Azure Boards work item link (warns if
   absent — not a hard blocker, but recorded as an unresolved traceability gap).
6. Validates that `index.md` contains at least one TL technical decision statement (warns
   if absent — flags that post-promotion consolidation will have insufficient anchors to
   assess alignment between the original design intent and the module docs).
7. Presents a close-readiness table in chat showing per-artifact status.
8. If not ready: lists what remains and stops without modifying any file.
9. If ready: asks for explicit PO and TL confirmation — **type "confirm" to proceed**.
10. On confirmation:
    - Strips all `#### Capability Definition Review` blocks from `index.md`
    - Adds a `Definition Closed` status marker to the `index.md` front matter

**Output written to file:**
- `index.md` — review blocks stripped, `Definition Closed` status marker added

**No test generation, no staging files, no traceability file.** `test-conditions.md` is
already authored by PO/TL and is validated but not modified. `traceability.md` is not part
of the `new` capability artifact set — source-evidence traceability is written only after
promotion to `active` on the first `capability-consolidation` run.

---

### Step 3 — `capability-define-clarify` (Developer, pre-coding)

**Parallel to:** `enhancement-clarify`

**Prerequisite:** `index.md` in `new/[CapabilityName]/` must carry the `Definition Closed`
status marker. If absent, or if any open `#### Capability Definition Review` blocks exist,
the skill stops and directs the developer to complete the PO/TL cycle first.

**What it reads:**

| File | Location | Purpose in clarification |
|---|---|---|
| `index.md` | `new/[CapabilityName]/` | Business scenarios, rules, acceptance conditions — treated as planned target state |
| `test-conditions.md` | `new/[CapabilityName]/` | `TC-*` conditions for success criteria mapping in mini-spec |
| `limitations.md` | `new/[CapabilityName]/` | Anticipated constraints affecting implementation choices |
| `internal_dependencies.md` | `new/[CapabilityName]/` | Adjacent active capabilities — checked one branch out |
| `external_dependencies.md` | `new/[CapabilityName]/` | External systems — checked one branch out |

**Key difference from `enhancement-clarify`:** All content is forward-looking. There is no
production baseline to contrast against. The skill reads `index.md` scenarios as the planned
target state. The one-branch-out dependency check still applies — adjacent `active` capability
module docs are read to verify that the integration points the TL declared in
`internal_dependencies.md` actually match what those capabilities expose.

**What it does:**

#### Load Phase

1. **Load capability intent** — reads `index.md` scenarios, rules, and acceptance conditions.
2. **Load test conditions** — reads `test-conditions.md` for `TC-*` success criteria mapping.
3. **Load anticipated constraints** — reads `limitations.md`.
4. **Adjacent capability verification (one branch out)** — for each entry in
  `internal_dependencies.md`, evaluates dependency status from the registry:
  - `active`: locates source-repo module docs and verifies that the declared integration point
    (data entity, endpoint, shared function) exists as described.
  - `new`: records as a conditional assumption requiring explicit developer confirmation.
  - any other status: raises blocker and stops clarification until corrected.
  Flags mismatches between what TL declared and what the adjacent capability actually exposes.
5. **External dependency specification check (one branch out)** — for each entry in
   `external_dependencies.md`, assesses whether the declared integration type and contract
   are sufficiently specified for implementation. Flags underspecified entries as blockers
   or assumptions.
6. **Net-new vs. reuse identification** — scans the codebase for any existing components that
   match artifact names or layers described in `index.md` technical sections. Flags apparent
   reuse candidates as assumptions requiring developer confirmation.

#### Clarification Output

```
## Pre-Coding Clarification: [CapabilityName] (New Capability)

### Capability Intent (from index.md)
[2–4 sentence summary of what this capability will do and who it serves]

### Scenarios in Scope
[One line per SCN-* entry: scenario ID and brief description]

### What Is Being Built
[One sentence per major component at each layer: UI, API, Database]

### Adjacent Capability Verification
[Table: Adjacent Capability | Status | Declared Interaction | Actual Interface Found | Assessment]

### External Dependency Specification Check
[Table: External System | Declared Type | Specification Completeness | Assessment]

### Blockers — Must resolve before coding
[Numbered list. If none: "No blockers identified."]

### Assumptions — Please confirm
[Numbered list. Each ends with "(confirm / correct)"]
[Includes reuse candidates and any mismatch between declared and actual adjacent interfaces]

### Nice-to-knows
[Numbered list. If none: "None."]
```

#### Clarification Loop and Mini-Spec

Identical loop behavior to `enhancement-clarify`:
- Resolves blockers iteratively
- Supports `skip clarification` with unresolved items recorded in the mini-spec
- Produces a confirmed **mini-spec** after developer types `confirmed`

**Mini-spec format for new capabilities:**

```
## Mini-Spec: [CapabilityName] — New Capability Build

**What is being built:**
[1–3 sentences describing the agreed implementation]

**New artifacts to create:**
[Bulleted list by layer: file/module/service name and its purpose]

**Existing artifacts to extend (if any):**
[Bulleted list, or "None — fully net-new"]

**Success criteria:**
[Numbered list mapped to TC-* IDs from test-conditions.md]

**Adjacent capability handling:**
[One line per entry: confirmed interface and agreed integration approach]

**External dependency handling:**
[One line per entry: confirmed contract and agreed integration approach]

**Anticipated constraints to respect:**
[One line per limitations.md entry relevant to this session]

**Out of scope for this session:**
[Explicitly excluded items, including any unresolved skip-clarification items]

**Routing note:**
[Routing recommendation from index.md Definition Review close. If Copilot-assisted or
Human required, supervision expectation is restated here.]
```

---

### Step 4 — `capability-promote-new` (PO/TL, post-delivery)

**Parallel to:** `capability-promote` (which handles active capabilities)

**When to run:** After the new capability has been built, deployed, and accepted by PO and TL.
This is the explicit, governed transition from `new` to `active` status.

**What it does:**

1. Reads the existing `new/[CapabilityName]/` artifact set as authored and validated by PO/TL.
2. Presents a promotion-readiness summary in chat and asks for explicit confirmation —
   **type "confirm" to proceed**.
3. On confirmation:
   - **Updates `index.md`**: removes the `Definition Closed` status marker, updates the
     capability status to `active`, formalises any scenario entries in draft notation into
     canonical `SCN-*` format consistent with `active` index.md conventions.
   - **Retains `test-conditions.md`** as-is — PO/TL-authored `TC-*` conditions become the
     baseline test conditions for the now-active capability. IDs are never renumbered.
   - **Retains `limitations.md`**, `internal_dependencies.md`, `external_dependencies.md`
     as-is — moved with the folder intact.
   - **Seeds `enhancements.md`** using `capability_enhancements_template.md` — empty but
     correctly structured, ready for the first enhancement cycle.
   - **Seeds `backlog.md`** using `capability_backlog_template.md` — empty but correctly
     structured.
   - **Seeds `enhancement-test-conditions.md`** using
     `capability_enhancement_testing_template.md` — empty but correctly structured.
   - **Moves** the capability folder from
     `docs/business-capabilities/new/[CapabilityName]/` to
     `docs/business-capabilities/active/[CapabilityName]/`.
   - **Updates** the capability registry (`tag-registry.json`) status field from `new`
     to `active`.

4. POC failure behavior for promotion:
  - Uses fail-fast execution.
  - Avoids partial writes where possible.
  - If a failure occurs mid-flow, the skill reports a recovery checklist in chat
    (which files changed, which steps remain, and what to rerun).
  - Full transactional rollback is deferred to a post-POC hardening phase.

5. `traceability.md` does not exist in the `new` artifact set and is not created by this
   skill. It is seeded for the first time by the first `capability-consolidation` run after
   promotion, once source-repo module docs have been authored by the developer. See Section 5
   for the constraints that govern that first consolidation run.

---

## 4. Governance Rules for the New Workflow

| Rule | Detail |
|---|---|
| **New capability only** | All `capability-define-*` skills stop if capability status ≠ `new` |
| **Registry prerequisite** | `[CapabilityName]` must be in the capability registry with status `new` before PO/TL begin authoring or any skill in this family runs |
| **`index.md` is required before `capability-define-review`** | The skill reads `index.md` as its primary artifact. If it does not exist, the skill stops and instructs the PO to author it first using `business_capability_template.md` |
| **`capability-define-clarify` prerequisite** | Requires `Definition Closed` status marker in `index.md`. Stops if any open `#### Capability Definition Review` blocks exist. |
| **No file writes in clarify** | `capability-define-clarify` never modifies any file. Mini-spec is chat artifact only. |
| **Allowed internal dependency statuses in clarify** | `internal_dependencies.md` entries are valid only when target status is `active` or `new`. `active` is verified directly; `new` is captured as a conditional assumption requiring developer confirmation. |
| **One-branch-out rule** | Adjacent active capability module doc reading in `capability-define-clarify` is limited to directly listed integration points — no recursion into their dependency documents. |
| **Routing is preserved** | Routing note from `index.md` is always restated in the mini-spec. Never silently dropped. |
| **`capability-consolidation` does not run for new** | Bypassed entirely at `new` status — no source-repo module docs exist. First `capability-consolidation` run occurs after promotion to `active` once module docs have been authored. |
| **First post-promotion consolidation is non-destructive** | `capability-consolidation` in `first-run` mode (detected by absent `traceability.md` + empty `enhancements.md`) writes only `traceability.md`. All other baseline artifacts are read-only. Suggestions are surfaced as a chat report for PO/TL review only. |
| **`capability-promote-new` is irreversible** | Once promotion runs and status moves to `active`, `capability-define-*` skills refuse to run on that capability. |
| **Test ID continuity** | `TC-*` IDs in `test-conditions.md` authored by PO/TL are permanent. Never renumbered after promotion. Enhancement-generated IDs must use separate families (`BTC-*`, `TTC-*`, `RTC-*`) with independent counters so they never collide with baseline `TC-*`. |
| **PO/TL confirmation required for promotion** | `capability-promote-new` requires explicit "confirm" before any file is written. Same pattern as `enhancement-review-close`. |

---

## 5. First Post-Promotion `capability-consolidation` Run — Design Constraints

### The problem

When `capability-consolidation` runs for an `active` capability in normal operation, it
synthesizes source-repo module docs and **generates** the full artifact set from scratch,
treating the module docs as the authoritative source of truth. For a capability that has
just been promoted from `new`, this is unsafe:

- `index.md`, `test-conditions.md`, `limitations.md`, `internal_dependencies.md`, and
  `external_dependencies.md` already exist as PO/TL-authored baselines that were reviewed
  and closed through the `capability-define` workflow.
- Source-repo module docs authored by the developer post-delivery may not yet be perfectly
  aligned with the canonical artifact structure — they are written to document implementation,
  not to replace business definitions.
- Running a standard `capability-consolidation` that overwrites these files risks destroying
  the validated PO/TL baseline with unintended content.

### Recommendation: reuse `capability-consolidation` with a `first-run` mode flag

The same `capability-consolidation` skill should be reused — introducing a separate skill
for this purpose would fragment the consolidation skill surface and create a maintenance
burden. Instead, `capability-consolidation` should detect the first-run context and apply
a constrained operating mode.

**Detection:** The skill detects first-run context when:
- The capability status is `active`, AND
- `traceability.md` is absent from the capability folder (it was never present at `new` status
  and has not yet been seeded), AND
- `enhancements.md` is present but empty (seeded by `capability-promote-new`, never written to)

When all three conditions are true, the skill operates in **`first-run` mode** instead of
standard mode.

### `first-run` mode behaviour

| Artifact | Standard `capability-consolidation` behaviour | `first-run` mode behaviour |
|---|---|---|
| `index.md` | Generated from module docs — overwrites existing content | **Read-only.** Skill reads it as the authoritative baseline. May produce a **suggested additions report** in chat identifying gaps or enhancements based on module docs, but writes nothing to the file. PO/TL decide whether to incorporate suggestions. |
| `test-conditions.md` | Generated from module docs | **Read-only.** Same pattern — suggestions surfaced in chat only. |
| `limitations.md` | Generated from module docs | **Read-only.** Suggestions only. |
| `internal_dependencies.md` | Generated from module docs | **Read-only.** Suggestions only. |
| `external_dependencies.md` | Generated from module docs | **Read-only.** Suggestions only. |
| `traceability.md` | Refreshed from module docs | **Created for the first time.** Seeded with source-evidence entries mapping `index.md` claims to source-repo module doc paths. This is the one write operation in `first-run` mode. |

### Suggested additions report

The chat artifact produced by `first-run` mode consolidation is a **Suggested Additions
Report** presented to PO/TL for review. Its structure:

```
## First-Run Consolidation Report: [CapabilityName]

### Traceability seeded
[Confirmation that traceability.md has been created with source-evidence entries]

### Suggested additions to index.md
[Numbered list of specific additions the module docs support — each framed as a suggestion,
not a replacement. Example: "SCN-004 candidate: Module docs describe a bulk-import path
not covered in current scenarios. Suggested addition: [draft scenario text]"]

### Suggested additions to test-conditions.md
[Numbered list of additional TC-* candidates derived from implementation detail in module docs]

### Suggested refinements to limitations.md / internal_dependencies.md / external_dependencies.md
[Any implementation-discovered constraints or integration details not yet in the baseline artifacts]

### Alignment gaps (advisory)
[Any areas where module doc content appears to diverge from the PO/TL-authored baseline —
flagged for PO/TL review, not automatically resolved]
```

PO/TL must choose one governance action for the report:
- **Accept all** suggestions
- **Reject all** suggestions
- **Manual selective update** of chosen suggestions

PO/TL review the report and apply any accepted suggestions manually to the baseline artifacts.
After their review, a standard `capability-consolidation` run can be executed to confirm
full alignment going forward.

---

## 6. What Stays the Same — Continuity With the Existing Solution

| Existing contract | Status |
|---|---|
| `businessCapability` as single grouping key | ✅ Unchanged |
| `akr-capability` skill family naming and invocation pattern | ✅ Extended, not replaced |
| Role ownership (PO/Business, TL/Technical, Developer/Implementation) | ✅ Unchanged |
| Canonical artifact templates | ✅ Reused — PO/TL author directly from existing templates |
| `new/<CapabilityName>/` folder shape | ✅ Reduced to 5 artifacts — `traceability.md` removed for `new` status; code does not exist yet so source-evidence traceability cannot be written. Azure Boards links, PO acceptance conditions, and TL technical decisions are captured in `index.md` directly. |
| One-branch-out dependency rule | ✅ Applied identically in `capability-define-clarify` |
| Mini-spec as chat artifact only | ✅ Unchanged |
| `confirmed` / `skip clarification` interaction pattern | ✅ Unchanged |
| Routing recommendation table and scoring scale | ✅ Reused verbatim |
| Phase A-0 for active capabilities | ✅ Untouched |
| `enhancement-clarify` for active capabilities | ✅ Untouched — runs on `active` only after promotion |
| `capability-consolidation` for active and archived capabilities | ✅ Untouched — not invoked at `new` status. Reused post-promotion in `first-run` mode (non-destructive). |

---

## 7. Summary: Full New Capability Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│ Phase A: Define                                                      │
│                                                                     │
│ PO registers [CapabilityName] in capability registry (status: new)  │
│ PO/TL create docs/business-capabilities/new/[CapabilityName]/      │
│                                                                     │
│ PO authors (using existing canonical templates):                    │
│   → index.md (SCN-* scenarios, rules, acceptance conditions,       │
│               edge cases, out-of-scope — same format as active;    │
│               also includes Azure Boards work item link(s) and     │
│               TL technical decision statements)                    │
│   → test-conditions.md (TC-* business-tier conditions)             │
│                                                                     │
│ TL authors (using existing canonical templates):                    │
│   → test-conditions.md (TC-* technical-tier conditions — jointly)  │
│   → limitations.md (anticipated constraints)                       │
│   → internal_dependencies.md (planned in-app integration points)  │
│   → external_dependencies.md (planned external integration points) │
│                                                                     │
│ NOTE: traceability.md is NOT authored at new status — code does    │
│ not exist yet. It is seeded on first capability-consolidation run  │
│ after promotion to active.                                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Phase A-1: New Capability Definition Review (NEW)                   │
│                                                                     │
│ /akr-capability capability-define-review [CapabilityName]             │
│   → Reads all present artifacts in new/[CapabilityName]/           │
│   → Evaluates PO business content (index.md, test-conditions.md)  │
│   → Evaluates TL technical content (limitations, dependencies)     │
│   → Writes Capability Definition Review block into index.md        │
│   → Gaps found → PO/TL update artifacts → re-run until clear      │
│                                                                     │
│ /akr-capability capability-define-close [CapabilityName]              │
│   → Validates all artifacts complete and review block clear        │
│   → Strips review block from index.md                              │
│   → Adds "Definition Closed" status marker to index.md front matter│
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Phase B: Assess (reduced scope for new)                             │
│                                                                     │
│ capability-coverage-review: validates artifact set completeness     │
│ capability-impact-analysis: checks impact on existing active        │
│   capabilities via declared dependency records                      │
│                                                                     │
│ NOTE: capability-consolidation is NOT run — no source-repo docs    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Developer Handoff                                                    │
│                                                                     │
│ Developer opens multi-root workspace                                │
│ /akr-capability capability-define-clarify [CapabilityName]            │
│   → Reads all artifacts from new/[CapabilityName]/                 │
│   → Verifies adjacent active capability interfaces (one branch out)│
│   → Checks external dependency specification completeness          │
│   → Identifies net-new vs. reuse candidates                        │
│   → Clarification loop: Blockers → Assumptions → Nice-to-knows    │
│   → Mini-spec confirmed                                             │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Coding Session                                                       │
│                                                                     │
│ Developer attaches as Copilot context:                              │
│   → index.md (Definition Closed)                                    │
│   → test-conditions.md                                              │
│   → limitations.md, internal_dependencies.md,                      │
│     external_dependencies.md (as needed)                           │
│   → Mini-spec                                                        │
│   → Adjacent active capability module docs (integration points)    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Post-Coding: Developer creates source-repo module documentation     │
│                                                                     │
│ Developer authors module docs in the source repository tagged:     │
│   businessCapability: [CapabilityName]                             │
│ (Required before capability-consolidation can run post-promotion)  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Phase D-1: Promote New → Active                                     │
│                                                                     │
│ /akr-business-consolidation capability-promote-new [CapabilityName] │
│   → Formalises index.md to active conventions; removes             │
│     "Definition Closed" marker; updates status to active           │
│   → Retains test-conditions.md, limitations.md,                    │
│     internal/external dependencies as-is                           │
│   → Seeds enhancements.md, backlog.md,                             │
│     enhancement-test-conditions.md (empty, ready for first cycle)  │
│   → Moves folder: new/[CapabilityName]/ → active/[CapabilityName]/ │
│   → Updates registry: status new → active                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ First post-promotion capability-consolidation run (Phase C)         │
│ — first-run mode (non-destructive)                                  │
│                                                                     │
│ /akr-business-consolidation capability-consolidation [CapabilityName]│
│   → Detected as first-run: traceability.md absent +                │
│     enhancements.md empty                                           │
│   → WRITES: traceability.md — seeded with source-evidence entries  │
│   → READ-ONLY: all other baseline artifacts unchanged              │
│   → PRODUCES: Suggested Additions Report in chat for PO/TL review  │
│     (index.md, test-conditions.md, limitations, dependencies)      │
│   → PO/TL review and manually apply accepted suggestions           │
│   → Subsequent standard consolidation runs proceed normally        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
         Capability is now fully ACTIVE — full Phase A-0 through G
         workflow available for all future enhancements
```
