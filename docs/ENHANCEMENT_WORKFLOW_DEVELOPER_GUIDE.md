# Enhancement Workflow Guide for Developers

Date: 2026-04-18
Audience: Developer, Copilot Coding Agent
Scope: How to receive a closed `enhancements.md` from the PO and Technical Lead, run the `enhancement-clarify` skill to resolve implementation ambiguities, and proceed to a confirmed coding session — including how to handle discoveries made during clarification that require back-documentation to the requirements.

---

## Overview

This guide covers the **developer side of the enhancement workflow**. By the time a developer receives an enhancement, the PO and Technical Lead have already completed the full review cycle in the consolidation repository:

This document applies to **active capabilities only**. For `new` capabilities, developers must use `capability-define-clarify` after PO/TL complete `Definition Closed` in `index.md`.

```
PO/TL Phase (already complete before developer begins):
  /akr-capability enhancement-review [CapabilityName]         ← iterated until no gaps
  /akr-capability enhancement-review-close [CapabilityName]   ← requirements approved
  /akr-capability enhancement-test-generation [CapabilityName] ← test conditions derived
```

The signal that handoff has occurred is `enhancements.md` having status `Review Closed` in the Enhancement Activity table. No development work begins before this signal is present.

The developer then runs a single pre-coding skill:

```
Step 1:  /akr-capability enhancement-clarify [CapabilityName]   ← run from the application codebase repo
```

This skill maps the approved requirements to the actual codebase, surfaces any blockers or assumptions before a single line of code is written, and produces a confirmed **mini-spec** the developer uses to brief the Copilot coding agent.

After implementation delivery and business/technical acceptance, ownership returns to the PO and TL to run the cycle-close step in the consolidation workflow:

```
/akr-business-consolidation capability-promote [CapabilityName]
```

This post-acceptance closeout step promotes delivered enhancement behavior into baseline capability artifacts.

**POC testing note:** Actual testing execution activities are out of scope for this proof-of-concept. There is currently no dedicated artifact that records completion of testing execution. `enhancement-test-conditions.md` documents planned test conditions, not executed test completion state.

---

## Part 1: Prerequisites Before Running enhancement-clarify

### What Must Be True Before You Proceed

| Prerequisite | Where to Verify |
|---|---|
| Capability status is `active` | `docs/business-capabilities/active/[CapabilityName]/index.md` — check the Status field |
| `enhancements.md` status is `Review Closed` | Enhancement Activity table in `enhancements.md` — all ENH-* rows must show `Review Closed` |
| No open `#### Enhancement Review` blocks exist in `enhancements.md` | Scan the file — any open review block means the PO/TL cycle is not yet complete |
| `enhancement-test-conditions.md` exists in the capability folder | Confirms `enhancement-test-generation` has been run; this file is required input for the skill |
| Your workspace has both the consolidation repo and the application codebase repo open | See Part 2 below |

If any prerequisite is not met, do **not** proceed. Contact the PO or Technical Lead and reference the `ENHANCEMENT_WORKFLOW_PO_TL_GUIDE.md` to identify which step is incomplete.

If the capability is `new`, stop this workflow and run the new-capability handoff path instead:

```
/akr-capability capability-define-clarify [CapabilityName]
```

New-capability clarify applies status-aware dependency handling:
- Internal dependencies with status `active` are verified directly.
- Internal dependencies with status `new` are captured as conditional assumptions and must be explicitly confirmed by the developer.

---

## Part 2: Workspace Setup — Two Repos Required

The `enhancement-clarify` skill reads from **two repositories simultaneously**:

| Repository | Role | What the Skill Reads |
|---|---|---|
| **Consolidation repo** (business definitions) | Source of requirements truth | `index.md`, `enhancements.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `enhancement-test-conditions.md` |
| **Application codebase repo** (implementation) | Source of code structure truth | Source-repository module docs tagged `businessCapability: [CapabilityName]` — typically `docs/services/*.md`, `docs/modules/*.md` |

The skill cannot map business requirements to actual code without access to both. **A single VS Code window with a multi-root workspace is the required setup.**

### Recommended: Multi-Root Workspace

Open both repos as separate folders in one VS Code workspace using a `.code-workspace` file. The `akr-consolidation.code-workspace.seed` template in the onboarding folder provides a starting point.

```json
{
  "folders": [
    {
      "path": "../core-akr-templates",
      "name": "Consolidation (Business Definitions)"
    },
    {
      "path": ".",
      "name": "Application Codebase (Implementation)"
    }
  ]
}
```

**Why multi-root:**
- Both folder hierarchies are visible in the Explorer simultaneously
- File search and Copilot context span both repos naturally
- The developer can navigate between business docs and source code without switching windows
- The clarification loop in the skill benefits from the developer being able to cross-reference docs and code in the same session

**Do not open two separate VS Code windows.** This breaks the unified search context the skill relies on and forces manual context switching during the clarification loop.

---

## Part 3: Running enhancement-clarify

### Invocation

From the application codebase repo, run:

```
/akr-capability enhancement-clarify [CapabilityName]
```

### What the Skill Does

The skill executes eight steps in sequence:

#### Steps 1–2: Load Context

The skill reads all six input files from the capability folder in the consolidation repo and builds an internal summary of the **current capability baseline** (business rules, scenario IDs, known limitations) and a **code component map** by layer (UI, API, Database) from source-repository module docs tagged with `businessCapability: [CapabilityName]`.

If source-repository module docs are not accessible or not tagged, the skill continues but surfaces a blocker: the developer must manually confirm the affected files.

#### Step 3: Load Enhancement Context

The skill reads every ENH-* entry with status `Review Closed` and:
- Extracts Business Requirements (outcomes, acceptance criteria, out-of-scope statements, edge cases, affected roles)
- Extracts Technical Requirements (specific artifacts listed in Implementation Scope, declared dependencies, known limitations)
- Cross-references enhancement scope against the scenario baseline in `index.md` to identify which existing `SCN-*` scenarios are affected
- Cross-references against `enhancement-test-conditions.md` to confirm test condition coverage matches declared scope

#### Step 4: Dependency Impact Check (One Branch Out Only)

The skill assesses every listed internal and external dependency of the target capability:

- **Internal:** Checks `internal_dependencies.md` — flags each dependent capability as **Impact Possible**, **Impact Unlikely**, or **Needs Confirmation**
- **External:** Checks `external_dependencies.md` — assesses whether the enhancement changes any data contract, authentication flow, or integration behavior

The skill does **not** recurse into the dependency documents of those dependencies. One branch out only.

#### Steps 5–6: Clarification Output

The skill presents the following in chat:

```
## Pre-Coding Clarification: [CapabilityName]

### Business Baseline (from index.md)
[2–4 sentence summary of the current capability and its key rules]

### Enhancement Scope Summary
[One sentence per ENH-* entry: what it changes and which SCN-* scenarios it affects]

### Code Components in Scope
[Bulleted list by layer: component/module name and what is changing]

### Dependency Impact
[Table: Dependency | Type | Assessment | Rationale]

### Blockers — Must resolve before coding
[Numbered list. If none: "No blockers identified."]

### Assumptions — Please confirm
[Numbered list of inferences. Each ends with "(confirm / correct)"]

### Nice-to-knows
[Numbered list. If none: "None."]
```

#### Step 7: Clarification Loop

The developer responds to the clarification output. The skill processes each response:

- Blockers that are resolved are marked `✅ Resolved` with a one-line summary
- Confirmed assumptions are marked `✅ Confirmed`
- Corrected assumptions are marked `✏️ Corrected: [correction]`
- New blockers emerging from responses are marked `🆕 New Blocker`

The loop continues until all blockers are resolved and all assumptions are confirmed or corrected, **or** the developer types `skip clarification` (see below).

**Typing `skip clarification`:** All outstanding blockers and unconfirmed assumptions are recorded in the mini-spec under "Out of scope / Unresolved" and the skill proceeds. Use this only when the outstanding items are genuinely non-blocking for the current session.

#### Step 8: Mini-Spec Confirmation

The skill produces the **mini-spec** — a concise, agreed statement of what the coding session will deliver:

```
## Mini-Spec: [CapabilityName] — [ENH-* scope]

**What is being built:**
[1–3 sentences describing the agreed implementation]

**Files / components to change:**
[Bulleted list of specific artifacts, corrected by any developer clarifications]

**Success criteria:**
[Numbered list — each item is a verifiable condition, mapped to BTC-/TTC-/RTC- IDs where available]

**Dependency handling:**
[One line per flagged dependency: what was agreed, or "No change required"]

**Out of scope for this session:**
[Items explicitly excluded, including any unresolved blockers if skip clarification was used]

**Routing note:**
[Routing recommendation from enhancements.md. If Copilot-assisted or Human required, supervision expectation is restated here]
```

The developer types `confirmed` to finalize. On correction, the mini-spec is updated and re-presented until confirmed.

---

## Part 4: Using the Mini-Spec in the Coding Session

The mini-spec is a **chat artifact only** — it is never written to any file by the skill. To use it in the coding session:

1. Copy the mini-spec from the clarification chat
2. Open the coding session (new Copilot chat or continuation)
3. Attach the following as context:
   - `enhancements.md` from the consolidation repo (the clean, Review Closed version)
   - The mini-spec (pasted or attached)
   - Any source-repository module docs relevant to the components being changed
4. Brief the Copilot coding agent using the mini-spec scope as the authoritative boundary

The coding agent now has:
- Business intent and acceptance criteria (from `enhancements.md`)
- Agreed implementation scope with corrected file names and component details (from mini-spec)
- Verifiable success criteria mapped to BTC-/TTC-/RTC- test condition IDs
- Confirmed dependency handling decisions
- Clear routing note if developer supervision is required

---

## Part 5: Handling Discoveries During Clarification — Back-Documentation Protocol

### When This Protocol Applies

During the clarification loop (Step 7), the developer may uncover factual information not known at the time the TL and PO wrote the requirements. This is different from a simple clarification or correction:

| Discovery Type | Definition | Action |
|---|---|---|
| **Informational** | A new detail that confirms or clarifies existing scope without changing it (e.g., the actual file path differs slightly from the TL's reference) | Capture in mini-spec only — no back-documentation needed. Developer proceeds normally. |
| **Additive** | A new detail that adds something previously unknown but remains within the declared scope (e.g., an undocumented DB index constraint that affects the TL's migration plan, a hidden configuration dependency) | Back-document to the appropriate requirements section. Developer proceeds after TL confirms the addition in writing. |
| **Scope-changing** | A discovery that changes what the PO accepted or what the TL committed to building (e.g., a missing integration contract, an undocumented authorization rule that alters the acceptance criteria, a fundamental limitation that voids a declared implementation path) | Suspend coding. Full `enhancement-review` re-run required after requirements are updated. |

The developer classifies the discovery and presents it to the PO and TL for agreement. The PO and TL make the final determination on classification when there is any doubt.

---

### Additive Discovery: Proceed Path

**Who does what:**

| Role | Responsibility |
|---|---|
| Developer | Documents the discovery in chat with a clear description of what was found and why it is relevant |
| Technical Lead | Authors the addition to the **Technical Requirements** section of `enhancements.md` (TL owns this section) |
| Product Owner | Authors any addition to the **Business Requirements** section if the discovery has a business-facing impact (PO owns this section) |
| Developer | Adds corresponding test condition(s) to `enhancement-test-conditions.md` following existing ID sequencing (BTC-/TTC-/RTC-) |

**Steps:**

```
1. Developer surfaces discovery in clarification chat
2. Tri-party agreement (PO + TL + Developer) classifies as Additive
3. TL amends Technical Requirements in enhancements.md
   (PO amends Business Requirements if business-facing)
4. Developer adds new test condition(s) to enhancement-test-conditions.md
   — follow existing ID sequencing; IDs are never reused or skipped
5. TL confirms the amendments in writing (chat acknowledgment is sufficient)
6. Developer proceeds to mini-spec confirmation
7. Mini-spec reflects the updated scope
```

**Important:** The `enhancements.md` Status column remains `Review Closed` for an Additive discovery. The addition is a factual supplement within approved scope, not a new review cycle.

---

### Scope-Changing Discovery: Suspend Path

**Steps:**

```
1. Developer surfaces discovery in clarification chat
2. Tri-party agreement classifies as Scope-changing
3. Coding is suspended — developer does not proceed to mini-spec confirmation
4. TL and/or PO update the relevant requirements section(s) in enhancements.md
5. ENH-* status in the Enhancement Activity table is reset from "Review Closed"
   back to "Under Review" — this is required for the skill to detect that
   the review cycle is not yet complete
6. PO/TL re-run the full review cycle:
     /akr-capability enhancement-review [CapabilityName]
     /akr-capability enhancement-review-close [CapabilityName]
     /akr-capability enhancement-test-generation [CapabilityName]
7. Once status returns to "Review Closed", developer re-runs:
     /akr-capability enhancement-clarify [CapabilityName]
```

**Why a full re-run is required:** A scope-changing discovery invalidates the test conditions that were derived from the original requirements. Re-running `enhancement-test-generation` ensures test coverage reflects the updated scope. Skipping this step leaves test condition IDs in `enhancement-test-conditions.md` that reference acceptance criteria the team has since changed.

---

### Discovery Classification Reference

Use this decision guide when classifying a discovery:

```
Does the discovery change any acceptance criterion the PO wrote?
  Yes → Scope-changing → Suspend

Does the discovery void or contradict any specific artifact or
implementation path the TL declared?
  Yes → Scope-changing → Suspend

Does the discovery add a previously unknown technical detail
(constraint, dependency, configuration) that the TL's plan
must account for but does not change the overall approach?
  Yes → Additive → Proceed after TL amends

Does the discovery simply clarify or correct a naming, path,
or minor detail that does not change what is being built?
  Yes → Informational → Capture in mini-spec only
```

When in doubt, classify upward (treat as Scope-changing rather than Additive).

---

## Part 6: Governance Rules Summary

| Rule | Detail |
|---|---|
| **Active capability only** | `enhancement-clarify` stops if capability status ≠ `active` |
| **Review Closed prerequisite** | `enhancement-clarify` stops if `enhancements.md` has open `#### Enhancement Review` blocks or any ENH-* not at `Review Closed` |
| **No file writes by the skill** | The skill never modifies any file. The mini-spec is a chat artifact only. All back-documentation is done manually by the appropriate role. |
| **One-branch-out dependency rule** | The skill only checks directly listed dependencies — it does not recurse into those dependencies' own dependency documents |
| **Module docs must be tagged** | Source-repo module docs must carry `businessCapability: [CapabilityName]` metadata for the skill to locate them. Missing tags result in a blocker in the clarification output. |
| **Routing is preserved** | If `enhancements.md` routing recommendation is ⚠️ Copilot-assisted or 🚫 Human required, this is prominently restated in the mini-spec. Developer supervision expectations are never silently dropped. |
| **Test condition IDs are permanent** | BTC-/TTC-/RTC- IDs in `enhancement-test-conditions.md` are never renumbered or reused, including after back-documentation updates. New conditions added during the Additive path use the next available sequential ID. |
| **POC testing execution artifact does not exist** | In this proof-of-concept, actual testing execution is out of scope. No artifact currently denotes completion of testing execution activities. `enhancement-test-conditions.md` remains a design/planning artifact for conditions, not a completion ledger. `capability-promote` therefore relies on explicit human confirmation when PO/TL decide whether baseline test merge should run. |
| **Additive status remains Review Closed** | An Additive discovery does not restart the PO/TL review cycle. Status is not changed. |
| **Scope-changing requires status reset** | The ENH-* status must be manually reset to `Under Review` before the PO/TL re-run the review cycle. This prevents `enhancement-clarify` from re-running prematurely. |

---

## Part 7: End-to-End Developer Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│ PO/TL Phase (complete — enhancements.md status: Review Closed)     │
│                                                                     │
│   enhancement-review → enhancement-review-close                    │
│   → enhancement-test-generation                                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ Handoff signal:
                               │ enhancements.md Status = "Review Closed"
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Developer opens multi-root workspace                               │
│   Folder 1: Consolidation repo (business definitions)             │
│   Folder 2: Application codebase repo (implementation)            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ /akr-capability enhancement-clarify [CapabilityName]                  │
│                                                                     │
│  → Loads capability baseline, code component map,                 │
│    enhancement scope, dependency impact                            │
│  → Outputs: Blockers, Assumptions, Nice-to-knows                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
             blockers found?        no blockers
                    │                    │
                    ▼                    │
         Developer resolves             │
         blockers in loop               │
                    │                    │
                    └──────────┬─────────┘
                               │
              discovery made during loop?
         ┌─────────────────────┼──────────────────────┐
    Informational           Additive             Scope-changing
         │                    │                       │
    Capture in            TL amends             Suspend coding
    mini-spec only        enhancements.md        Reset status to
    Proceed               Dev adds test          "Under Review"
                          conditions             PO/TL re-run:
                          Proceed after          enhancement-review
                          TL confirms            → review-close
                                                 → test-generation
                                                 → Re-run clarify
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Mini-Spec Confirmation                                             │
│                                                                     │
│  → Developer reviews mini-spec                                    │
│  → Types "confirmed"                                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Coding Session                                                     │
│                                                                     │
│  Developer attaches to Copilot:                                   │
│  → enhancements.md (from consolidation repo)                      │
│  → Mini-spec (from clarification chat)                            │
│  → Source-repo module docs for components in scope                │
│                                                                     │
│  Copilot coding agent proceeds within the confirmed scope         │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PO/TL Post-Acceptance Closeout                                     │
│                                                                     │
│  /akr-business-consolidation capability-promote [CapabilityName]   │
│                                                                     │
│  → Promotes delivered enhancement outcomes to baseline artifacts   │
│  → Uses explicit human confirmation for testing completion         │
│  → In this POC, may proceed without a testing-completion artifact  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 8: Tips for Developers

- **Read `enhancements.md` before running the skill.** Understanding the declared scope in advance reduces the number of clarification rounds and helps you identify potential blockers before the skill surfaces them.
- **Tag your module docs.** If source-repository module docs are not tagged with `businessCapability: [CapabilityName]`, the code component map will be incomplete. The skill will surface this as a blocker and the developer will need to manually confirm affected files. Keeping module docs current and tagged prevents this.
- **Do not estimate — verify.** When the skill flags a dependency as Needs Confirmation, resist the urge to mark it resolved without checking. Open the actual codebase, confirm the integration behavior, and respond with specific evidence.
- **The mini-spec is your scope contract.** Once you type `confirmed`, the mini-spec is the authoritative scope boundary for the coding session. If the coding agent tries to expand scope beyond what is in the mini-spec, the developer should redirect it back.
- **Classify discoveries conservatively.** When in doubt between Additive and Scope-changing, treat it as Scope-changing. It is faster to re-run a clean review cycle than to discover mid-coding that the requirements were materially wrong.
- **Routing note is not optional.** If the mini-spec routing note says ⚠️ Copilot-assisted or 🚫 Human required, that supervision expectation is real. Do not let a "confirmed" mini-spec become a signal to step away from the coding session.
- **Call out the closeout handoff.** Once delivery is accepted by business and technical owners, explicitly hand off to PO/TL to run `/akr-business-consolidation capability-promote [CapabilityName]` as the cycle-closing step.
- **Do not infer testing completion from artifacts.** In this POC, no artifact confirms completed test execution; treat `enhancement-test-conditions.md` as planned coverage only. During closeout, PO/TL may still ask for manual confirmation of whether testing is complete before `capability-promote` decides whether to merge baseline tests.
