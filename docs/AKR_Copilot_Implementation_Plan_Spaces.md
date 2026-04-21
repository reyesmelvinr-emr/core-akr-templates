# AKR Copilot Scoped Retrieval — Implementation Plan (Copilot Spaces)

**Project:** AKR Copilot Context Retrieval POC  
**Date:** 2026-04-19  
**Status:** POC Implementation Planning  
**Interface:** GitHub Copilot Spaces (web)  
**Purpose:** Define the full implementation plan for deploying AKR-guided scoped retrieval
using GitHub Copilot Spaces as the retrieval infrastructure and instruction carrier,
replacing the VSCode IDE-based approach.

## Implementation Kickoff Status (2026-04-21)

The following starter artifacts are now created in this repository to begin Sprint execution:

- `docs/AKR_SPACE_BOOTSTRAP.md`
- `docs/AKR_SPACE_INSTRUCTION.md`
- `docs/AKR_COPILOT_QUICKSTART.md`
- `docs/references/AKR_EVAL_CASES.md`

These files provide immediately usable templates, but are not yet environment-specific.
The Space owner must populate repository names, Space URL, and scenario data before pilot use.

POC expectation reminder:

- Spaces improves scope control and instruction persistence for this POC.
- Spaces does not provide deterministic file-level retrieval guarantees.
- Instruction policy is high-leverage but not programmatically enforced.

---

## Context and Approach

Default Copilot performs unscoped retrieval — it works from ambient context and has no
awareness of business capability boundaries, evidence quality, or documentation hierarchy.
The AKR layer addresses this by defining what Copilot should retrieve, in what order,
and how it should qualify its answers.

**Why Copilot Spaces instead of VSCode**

The VSCode approach required a scope manifest, a workspace bootstrap process, per-repository
`copilot-instructions.md` files carrying policy blocks, and explicit skill file invocation
by each developer. It was fragile because scope depended on which folders were open and
policies were only active when developers remembered to invoke the skill.

Copilot Spaces solves the two most fragile parts of the VSCode approach directly:

- **Scope boundary** — The Space is configured with exactly three repositories. That
  boundary is real, stable, and set once by the Space owner. It does not depend on open
  folders or developer discipline.
- **Persistent instruction** — The Space instruction field injects a policy block into
  every question asked within the Space automatically. Developers do not need to reference
  any file or invoke any skill. The policy is always active.

The approach in this plan does not replace Copilot's retrieval engine. It configures a
bounded, instruction-governed Space around it so that AKR behavioral policies apply
consistently to every capability-scoped question asked through that Space.

**What this plan delivers**

An AKR-configured Copilot Space with a three-repository scope, a persistent instruction
block encoding all retrieval and output behavior policies, a precomputed capability map
attached as a Space resource, CI gates enforcing metadata quality at the source, a
developer quickstart, and a structured evaluation framework that produces the management
evidence needed for a go/no-go decision on production investment.

**What this plan does not deliver**

A custom retrieval engine. Behavioral policies are instruction-enforced, not
programmatically guaranteed. The plan includes a tuning sprint specifically because
instruction wording affects consistency and will require iteration against real test cases.

---

## Implementation Items

---

### Item 1 — Copilot Space Configuration

**What it is**  
The initial creation and configuration of the GitHub Copilot Space that will serve as
the AKR retrieval environment for the POC. This is a one-time setup performed by the
Space owner on the GitHub website.

**Why it matters**  
The Space configuration is the foundation of everything else in this plan. The repository
selection defines the retrieval boundary. If the wrong repositories are attached, or if
the consolidation repository is missing, the Space cannot provide business context
regardless of how well the instruction is written.

**What to implement**  
- Navigate to GitHub Copilot Spaces and create a new Space named:  
  `AKR Scoped Retrieval — POC`
- Attach exactly three repositories in the Space repository configuration:
  - `<backend-repo-name>` — provides technical context: service code and source module docs
  - `<ui-repo-name>` — provides technical context: UI component code and module docs
  - `<business-docs-repo-name>` — provides business context: consolidated capability artifacts
- Set the Space visibility to the appropriate team access level for the POC participants.
- Do not attach additional repositories. The three-repository boundary is the scope
  boundary for the entire POC. Adding more repositories without updating the Space
  instruction and capability map invalidates the scoping model.
- Confirm that GitHub has indexed all three repositories before proceeding to Item 2.
  Indexing can take several minutes after the Space is created.

**Acceptance criteria**  
- Space exists with the correct name and all three repositories attached.
- All three repositories are confirmed as indexed by GitHub (search returns results
  from all three when tested with a known term).
- Space visibility is set correctly for POC participants.
- No additional repositories are attached beyond the defined three.

**Effort:** Low  
**Sprint:** 1

---

### Item 2 — Precomputed Capability Map

**What it is**  
A machine-readable JSON file generated from `modules.yaml` and documentation front
matter across all in-scope repositories that maps every module to its `businessCapability`,
documentation paths, layer, feature reference, and status. This file is attached to the
Space as a resource so Copilot has the full module-to-capability lookup available without
performing runtime discovery across multiple files.

**Why it matters**  
Copilot cannot reliably piece together module-to-capability mappings at runtime by reading
`modules.yaml` and scanning documentation front matter across three repositories
simultaneously. The precomputed map makes the mapping explicit, complete, and reviewable.
It also surfaces metadata gaps visibly — a missing entry in the map means missing coverage,
not a silent failure. Attaching it to the Space makes it part of every question's context
without requiring developers to reference it manually.

**What to implement**  
- Create a generation script (PowerShell or Python) that reads `modules.yaml` from each
  in-scope application repository and all documentation front matter under the configured
  doc paths, then outputs `akr-capability-map.json`.
- Output structure per entry:

```json
{
  "module": "<module-name>",
  "businessCapability": "<capability-name>",
  "layer": "API | UI | Database",
  "feature": "FN#####_US#####",
  "status": "active | new | archived",
  "sourceDocPaths": [
    "<repo>/docs/services/<module>.md"
  ],
  "consolidationDocPath": "<business-repo>/docs/business-capabilities/<status>/<capability>/index.md",
  "moduleCodePaths": [
    "<repo>/src/<module-folder>/"
  ]
}
```

- Store the generation script in the AKR skill bundle or as a standalone workspace
  utility so it can be rerun whenever `modules.yaml` or documentation metadata changes.
- Attach the generated `akr-capability-map.json` to the Copilot Space as a file resource.
- Add a CI check (see Item 6) that warns when `akr-capability-map.json` is stale relative
  to the most recently modified `modules.yaml` or documentation file, and prompts
  regeneration and re-upload to the Space.

**Note on updates:** When the capability map is regenerated after metadata changes, the
updated file must be manually re-attached to the Space. Document this as a Space
maintenance step in `workspace-bootstrap.md` (Item 3).

**Acceptance criteria**  
- Generation script produces a valid `akr-capability-map.json` from current repository state.
- Map covers all modules declared in all in-scope `modules.yaml` files.
- File is attached to the Copilot Space and visible to Copilot when queried.
- CI stale-map check is operational and produces a visible warning in PRs when the map
  is out of date.
- At least one test query against the Space confirms Copilot references the map correctly.

**Effort:** Medium  
**Sprint:** 1

---

### Item 3 — Space Bootstrap and Maintenance Checklist

**What it is**  
A short reference document that defines what must be confirmed before the Space is used
for a POC session, and what maintenance steps are required when repositories or metadata
change. This replaces the complex per-developer VSCode bootstrap process with a single
Space-owner responsibility.

**Why it matters**  
The Space configuration is set once but must stay current with the repositories.
A stale capability map, a newly added capability with no consolidation artifact, or
a repository that has fallen out of sync with the Space index will all degrade answer
quality silently. A maintenance checklist prevents this from going unnoticed.

**What to implement**  
- Create `AKR_SPACE_BOOTSTRAP.md` in the `<business-docs-repo-name>` repository
  with the following sections:

```markdown
# AKR Copilot Space — Bootstrap and Maintenance Checklist

## Space URL
<insert Space URL after creation>

## Pre-session checks (Space owner, per sprint or after repository changes)
- [ ] All three repositories are attached and indexed in the Space.
- [ ] akr-capability-map.json is attached to the Space and reflects current modules.yaml state.
- [ ] Space instruction has not been accidentally cleared or truncated (see AKR_SPACE_INSTRUCTION.md).
- [ ] At least one active businessCapability artifact exists in the consolidation repository.

## After metadata changes (triggered by merged PRs to modules.yaml or doc front matter)
- [ ] Regenerate akr-capability-map.json using the generation script.
- [ ] Remove the old akr-capability-map.json from the Space file attachments.
- [ ] Attach the new akr-capability-map.json to the Space.
- [ ] Run one test query against the Space to confirm the updated map is read correctly.

## After new capability onboarding
- [ ] Confirm new capability name is present in akr-capability-map.json.
- [ ] Confirm at least index.md exists in the consolidation repository for the new capability.
- [ ] Reattach updated akr-capability-map.json to the Space.

## After Space instruction changes
- [ ] Save the updated instruction text to AKR_SPACE_INSTRUCTION.md before applying it.
- [ ] Apply the updated instruction in the Space instruction field.
- [ ] Run the evaluation smoke test (5 representative questions) to confirm behavior is correct.
```

- Also create `AKR_SPACE_INSTRUCTION.md` in the same repository as the version-controlled
  source of truth for the Space instruction text (see Item 4). The Space instruction field
  itself does not have version history — this file provides it.

**Acceptance criteria**  
- `AKR_SPACE_BOOTSTRAP.md` exists and is accurate against the current Space configuration.
- `AKR_SPACE_INSTRUCTION.md` exists and contains the current Space instruction text.
- Space owner has reviewed and signed off on both documents before POC sessions begin.

**Effort:** Low  
**Sprint:** 1

---

### Item 4 — Space Instruction Block

**What it is**  
The persistent instruction text entered into the Copilot Space instruction field. This
is the single most important artifact in the entire plan. It encodes all AKR behavioral
policies — capability resolution, retrieval order, evidence sufficiency, conflict
detection, and response modes — in a concise, plain-language format that Copilot
receives with every question asked in the Space.

**Why it matters**  
The Space instruction is always active. Every developer who asks a question in the Space
receives Copilot's response under this instruction without needing to invoke anything,
reference any file, or follow any per-session setup. This is the key advantage of Spaces
over the VSCode approach. The quality and precision of this instruction directly determines
the quality and consistency of every answer produced in the Space.

**Important constraint:** The Space instruction field has a token limit. The instruction
below is deliberately concise. If any section needs to be expanded, the lowest-priority
content to trim is the background context paragraph. The behavioral policy sections
(capability resolution through conflict handling) must be kept intact.

**What to implement**  
- Enter the following instruction into the Space instruction field.
- Save the same text to `AKR_SPACE_INSTRUCTION.md` in the consolidation repository
  as the version-controlled source of truth.

---

```
You are an AKR-guided Copilot assistant for a multi-repository application workspace.
Your job is to answer developer questions about application behavior and business
capabilities by retrieving scoped evidence from the three attached repositories and
the akr-capability-map.json file, rather than performing a broad unscoped search.

CAPABILITY RESOLUTION
Before retrieving evidence for any question about application behavior, modules,
or business context:
1. State which businessCapability this question is about.
2. State the evidence you used to reach that conclusion (active file, module name,
   or explicit mention in the question).
3. If you cannot identify a single businessCapability with confidence, state:
   "I could not determine a single businessCapability for this question. Please
   clarify which capability or module you are asking about."
4. Do not retrieve evidence until the capability is identified or clarified.

RETRIEVAL ORDER
When retrieving evidence, always follow this sequence:
1. The file or code the developer explicitly referenced in the question — highest priority.
2. Code files linked to the identified module in modules.yaml — primary technical corpus.
3. Source module documentation with matching businessCapability metadata — technical context.
4. Consolidation repository capability documents with matching businessCapability — business context.
5. General repository instructions and AKR reference documents — background context only.
If a step produces no results, state that explicitly before continuing.

EVIDENCE SUFFICIENCY
Before answering, verify you have minimum evidence:
- Minimum technical evidence (at least one): an explicitly referenced file related to
  the function, module-linked code from modules.yaml, or source module documentation
  for the same module.
- Minimum business evidence (for a full answer): at least one capability-aligned
  document from the consolidation repository or source documentation with explicit
  businessCapability metadata.
If minimum technical evidence is missing: do not provide a confident answer. State:
"I do not have sufficient technical evidence. Please reference the relevant module
files explicitly."
If business evidence is missing but technical evidence exists: proceed in
TECHNICAL ONLY mode and state that business context was not found.

CONFLICT DETECTION
Before synthesising an answer from multiple sources:
- If the same module maps to different businessCapability values across repositories:
  do not merge both paths. State the conflict and which source you are using.
- If source documentation and consolidation documentation disagree on behavior:
  prefer source module evidence for function behavior and report the discrepancy.
- If multiple capabilities match with no clear module anchor: do not select one
  arbitrarily. Declare the result ambiguous and ask for clarification.

RESPONSE MODES
Every answer must begin with one of the following declared modes:

[MODE: BUSINESS + TECHNICAL]
Full evidence available. Covers both technical behavior and business context.
Confidence: High. Sources: [list evidence used].

[MODE: TECHNICAL ONLY]
Technical evidence available. Business context was not found.
Confidence: Medium for technical behavior. Business impact not covered.
Sources: [list technical evidence used].

[MODE: AMBIGUOUS]
Capability could not be determined, or multiple capabilities matched.
This answer may not be scoped correctly. Please clarify before relying on it.
Confidence: Low.

[MODE: INSUFFICIENT EVIDENCE]
Required technical evidence was not found.
A confident scoped answer cannot be provided.
Action: Reference the relevant module files explicitly and ask again.

SCOPE BOUNDARY
Only treat content from the three attached repositories as authoritative.
Use akr-capability-map.json as the primary lookup for module-to-capability mapping.
Do not use knowledge outside these sources for function behavior or business rules.
```

---

**Tuning note:** The instruction above is a starting draft. Sprint 2 is dedicated to
iterating on the instruction wording based on real test results. Do not treat this text
as final until Sprint 2 evaluation confirms the response modes and conflict detection
are triggering correctly.

**Acceptance criteria**  
- Instruction is entered into the Space instruction field without truncation.
- Identical text is saved to `AKR_SPACE_INSTRUCTION.md` in the consolidation repository.
- A smoke test of five representative questions confirms Copilot declares a response
  mode for each answer.
- Copilot states the inferred capability before answering in all five smoke test questions.

**Effort:** Medium  
**Sprint:** 1

---

### Item 5 — Space Instruction Tuning

**What it is**  
A structured iteration process that tests the Space instruction from Item 4 against
the full set of evaluation scenarios and refines the wording until behavioral policies
are triggered correctly and consistently.

**Why it matters**  
The Space instruction is interpreted by a language model, not executed as code. The
wording, ordering, and phrasing of instruction sections affect how reliably Copilot
follows them. An instruction that looks correct on paper may still produce inconsistent
response mode selection, missed conflict detection, or skipped evidence checks until
the wording is tuned against real cases. This sprint exists specifically to surface
and fix those gaps before the POC evaluation.

**What to implement**  
- Run the following five scenario types against the Space using the current instruction:

| Scenario | Setup | Expected result |
|---|---|---|
| Full evidence | All metadata present, consolidation doc exists for the capability | `[MODE: BUSINESS + TECHNICAL]` |
| Technical only | No consolidation doc for the capability, source docs present | `[MODE: TECHNICAL ONLY]` with explicit business context note |
| Ambiguous | Question with no module anchor, no active file referenced | `[MODE: AMBIGUOUS]` with clarification request |
| Insufficient evidence | No relevant files referenced, question is vague | `[MODE: INSUFFICIENT EVIDENCE]` with action prompt |
| Conflict | Same module tagged with two different capabilities across repos | Conflict warning surfaced before answer |

- For each scenario where the expected result is not produced, identify the instruction
  section responsible and revise the wording.
- Re-run the affected scenario after each revision until the expected result is produced
  on at least three consecutive attempts.
- Record each instruction revision in `AKR_SPACE_INSTRUCTION.md` with a short note on
  what changed and why.
- Do not proceed to Sprint 3 until all five scenario types produce correct results
  consistently.

**Acceptance criteria**  
- All five scenario types produce the correct response mode on at least three consecutive
  attempts each.
- Conflict warning is surfaced in 100% of conflict scenario tests.
- Capability is stated before the answer in 100% of full-evidence and technical-only tests.
- Final tuned instruction text is saved to `AKR_SPACE_INSTRUCTION.md` and matches what
  is currently in the Space instruction field exactly.

**Effort:** Medium  
**Sprint:** 2

---

### Item 6 — CI Validation Gates

**What it is**  
Automated checks added to the pull request validation workflow in each application
repository that block merges when required AKR metadata is missing or inconsistent.
These gates enforce the documentation quality that the Space depends on to produce
accurate, well-scoped answers.

**Why it matters**  
The Space can only retrieve what exists and is correctly tagged. If developers can merge
documentation without `businessCapability` front matter, or without a valid `modules.yaml`
entry, the Space retrieval degrades silently. A developer asking about a capability whose
documentation lacks proper metadata will receive an `[MODE: INSUFFICIENT EVIDENCE]`
response through no fault of the Space configuration. CI gates enforce quality at the
point where it is cheapest to fix — the pull request.

**What to implement**  
- Extend the existing `validate-documentation.yml` workflow in each application
  repository with the following checks:
  - **Fail** if any new or modified documentation file under `docs/services/` or
    `docs/modules/` is missing `businessCapability` front matter.
  - **Fail** if the `businessCapability` value in any documentation file does not
    match an entry in `akr-capability-map.json`.
  - **Fail** if `modules.yaml` is absent from the repository root.
  - **Warn** (do not fail) if `akr-capability-map.json` is older than the most recently
    modified `modules.yaml` or documentation file. Include a message prompting the
    Space owner to regenerate and re-attach the map.

- Add a separate check in the consolidation repository workflow:
  - **Fail** if a capability folder under `docs/business-capabilities/active/` is
    missing `index.md` or `test-conditions.md`.
  - **Warn** if a capability folder under `docs/business-capabilities/new/` is
    missing `index.md`.

**Acceptance criteria**  
- PR is blocked when a documentation file missing `businessCapability` is submitted.
- PR is blocked when `modules.yaml` is absent from an application repository.
- PR is blocked when an active capability folder is missing `index.md`.
- Stale `akr-capability-map.json` produces a visible warning in the PR with a prompt
  to regenerate and re-attach to the Space.
- All checks complete in under three minutes.

**Effort:** Medium  
**Sprint:** 3

---

### Item 7 — Developer Onboarding Quickstart

**What it is**  
A short, practical guide that tells developers what the AKR Copilot Space is, how to
access it, how to ask capability-scoped questions effectively, and how to interpret
the response modes they will see. This is significantly simpler than the VSCode
equivalent because there is no skill invocation, no file referencing requirement, and
no bootstrap process for individual developers.

**Why it matters**  
The Space instruction handles all the behavioral policy automatically, but developers
still need to know how to phrase questions that anchor to a capability or module. An
unscoped question — "how does enrollment work?" — will still produce an `[MODE: AMBIGUOUS]`
response because Copilot cannot infer a capability target from vague phrasing. The
quickstart teaches developers the one habit that makes the Space work well: anchoring
questions to a specific capability, module, or file.

**What to implement**  
- Create `AKR_COPILOT_QUICKSTART.md` in the consolidation repository under `docs/` with
  the following content:

```markdown
# AKR Copilot Space — Developer Quickstart

## What is this Space?
The AKR Copilot Space is a GitHub Copilot environment configured to answer
questions about the application's business capabilities using evidence from
three repositories: the backend codebase, the UI codebase, and the business
documentation repository.

Copilot in this Space follows AKR retrieval policies automatically — you do not
need to reference any files or invoke any skills. Just ask your question and
Copilot will declare what kind of answer it was able to produce.

## How to access the Space
<insert Space URL>

## How to ask good capability-scoped questions

Good — capability anchor present:
"How does the EnrollmentManagement capability handle duplicate enrollments?"

Good — module anchor present:
"What does the enrollment-service module do when a user is already enrolled?"

Good — explicit file reference:
"Based on the enrollment-service source module docs, what are the known limitations?"

Avoid — no anchor:
"How does enrollment work?"
This will produce [MODE: AMBIGUOUS] because Copilot cannot infer which capability
or module you mean.

## How to read response modes

**[MODE: BUSINESS + TECHNICAL]**
Full answer. Both technical behavior and business context were found.
High confidence. Sources are listed.

**[MODE: TECHNICAL ONLY]**
Technical answer only. No business documentation was found for this capability.
Check that the consolidation repository has an index.md for this capability.

**[MODE: AMBIGUOUS]**
Copilot could not determine which capability your question is about.
Add a capability name, module name, or file reference and ask again.

**[MODE: INSUFFICIENT EVIDENCE]**
Copilot could not find enough technical evidence to answer confidently.
Reference the specific module files explicitly and ask again.

## When to escalate
If you consistently see AMBIGUOUS or INSUFFICIENT EVIDENCE for a capability that
should be covered, report it to the Space owner. The cause is usually one of:
- Missing businessCapability metadata in source module documentation.
- modules.yaml not updated after a module was added or renamed.
- akr-capability-map.json is stale and needs to be regenerated and re-attached.
```

**Acceptance criteria**  
- `AKR_COPILOT_QUICKSTART.md` exists in the consolidation repository.
- Space URL is filled in before the document is distributed to developers.
- A developer new to the Space can read the guide and ask a correctly scoped question
  in under five minutes.
- Response mode descriptions match the modes implemented in the Space instruction.

**Effort:** Low  
**Sprint:** 4

---

### Item 8 — Telemetry and Evaluation Framework

**What it is**  
A structured evaluation that measures whether the AKR-configured Space produces
meaningfully better answers than baseline Copilot, using a defined set of test cases
run against both configurations with results recorded for the management report.

**Why it matters**  
The POC must demonstrate measurable improvement, not just a better-configured system.
Management's decision to invest in production implementation depends on evidence
that scoped retrieval produces more accurate, more appropriately qualified answers
than unguided Copilot. Without a structured evaluation, the POC produces documentation
but no proof.

**What to implement**  
- Create `AKR_EVAL_CASES.md` in the consolidation repository under `docs/references/`
  with a minimum of 10 test cases covering all five scenario types:
  - 2 full evidence scenarios (active capability, all metadata present)
  - 2 technical-only scenarios (no consolidation doc for the capability)
  - 2 ambiguous scenarios (question with no module or capability anchor)
  - 2 insufficient evidence scenarios (vague question, no file reference)
  - 2 conflict scenarios (intentionally contradictory capability mappings)

- For each test case, record the following:

| Field | Description |
|---|---|
| Case ID | Unique identifier (e.g. EVAL-001) |
| Scenario type | Full evidence / Technical only / Ambiguous / Insufficient / Conflict |
| Question | Exact question asked |
| File referenced | Any file explicitly referenced in the question, or "none" |
| Expected mode | The response mode this question should trigger |
| Baseline result | Copilot answer with no Space instruction (plain GitHub Copilot) |
| AKR Space result | Copilot answer within the configured AKR Space |
| Mode declared | Yes / No — whether the correct mode was declared |
| Capability stated | Yes / No — whether Copilot stated the capability before answering |
| Evidence cited | Yes / No — whether evidence sources were listed |
| Conflict surfaced | Yes / No / N/A — whether conflict warning appeared (conflict cases only) |
| Answer accurate | Rating 1–5 by a reviewer familiar with the capability |
| Notes | Any observed deviation from expected behavior |

- Track the following summary metrics across all 10 cases:

| Metric | Definition | Target |
|---|---|---|
| Mode accuracy | % of cases where declared mode matched expected mode | ≥ 80% |
| Capability declaration rate | % of cases where capability was stated before answering | ≥ 90% |
| Conflict detection rate | % of conflict cases where warning was surfaced | 100% |
| Insufficient evidence rate | % of thin-evidence cases correctly declined | ≥ 80% |
| Answer precision (AKR) | Average accuracy rating across all cases | ≥ 3.5 / 5 |
| Answer precision (baseline) | Average accuracy rating for same cases without Space | Comparison only |

- Run all 10 cases against baseline Copilot first, then against the AKR Space.
  Record results separately so the delta is measurable.
- Produce a one-page evaluation summary that states: what was tested, what the results
  were, how the AKR Space compared to baseline, what gaps remain, and a go/no-go
  recommendation for production investment.

**Acceptance criteria**  
- Minimum 10 documented test cases covering all five scenario types.
- Results recorded for both baseline Copilot and AKR Space configurations.
- All summary metrics calculated and reported.
- Mode accuracy ≥ 80% in the AKR Space configuration.
- Conflict detection rate = 100% for all tested conflict scenarios.
- Evaluation summary reviewed and signed off by the POC lead before management presentation.

**Effort:** Medium  
**Sprint:** 5

---

## Sprint Plan

---

### Sprint 1 — Space Foundation

Deliver the configured Space, the precomputed capability map, the initial Space instruction,
and the maintenance checklist. At the end of this sprint the Space is operational and
developers can ask questions against it for the first time.

| Item | Deliverable |
|---|---|
| Item 1 | Copilot Space created with three repositories attached and indexed |
| Item 2 | `akr-capability-map.json` generated and attached to the Space |
| Item 2 | Capability map generation script in AKR skill bundle |
| Item 3 | `AKR_SPACE_BOOTSTRAP.md` in consolidation repository |
| Item 3 | `AKR_SPACE_INSTRUCTION.md` in consolidation repository |
| Item 4 | Space instruction entered into the Space instruction field |

**Exit criteria:**
- Space is accessible to POC participants.
- All three repositories are indexed and returning results.
- `akr-capability-map.json` is attached and referenced correctly by Copilot in a test query.
- Space instruction is active and Copilot declares a response mode in at least one
  smoke-test question.
- `AKR_SPACE_INSTRUCTION.md` matches the Space instruction field content exactly.

---

### Sprint 2 — Instruction Tuning

Iterate on the Space instruction until all five scenario types produce correct, consistent
behavioral responses. No new artifacts are created in this sprint — the work is entirely
in testing and refining the instruction wording.

| Item | Deliverable |
|---|---|
| Item 5 | Tuned Space instruction passing all five scenario types |
| Item 5 | Updated `AKR_SPACE_INSTRUCTION.md` reflecting all instruction revisions |

**Exit criteria:**
- All five scenario types (full evidence, technical only, ambiguous, insufficient
  evidence, conflict) produce the expected response mode on at least three
  consecutive attempts each.
- Conflict warning surfaces in 100% of conflict scenario tests.
- Capability is stated before the answer in 100% of full-evidence and
  technical-only tests.
- No further instruction changes are made after Sprint 2 is closed without
  rerunning the full five-scenario smoke test and updating `AKR_SPACE_INSTRUCTION.md`.

---

### Sprint 3 — CI Validation Gates

Deliver the automated PR checks that enforce metadata quality at the source repositories.
These gates protect the Space from silent degradation caused by missing or incorrect
`businessCapability` metadata.

| Item | Deliverable |
|---|---|
| Item 6 | Extended `validate-documentation.yml` in each application repository |
| Item 6 | Consolidation repository workflow check for active capability artifact completeness |
| Item 2 | CI stale-map warning operational |

**Exit criteria:**
- PR is blocked in all tested missing-metadata scenarios.
- Stale capability map produces a visible warning with a prompt to regenerate.
- All CI checks complete in under three minutes.

---

### Sprint 4 — Onboarding

Deliver the developer-facing documentation that makes the Space usable by the
full POC team without requiring individual briefing sessions.

| Item | Deliverable |
|---|---|
| Item 7 | `AKR_COPILOT_QUICKSTART.md` in consolidation repository with Space URL filled in |

**Exit criteria:**
- Quickstart is accurate against the current Space configuration.
- Space URL is present and correct.
- At least one developer not involved in building the Space reads the guide and
  successfully asks a correctly scoped question producing `[MODE: BUSINESS + TECHNICAL]`.

---

### Sprint 5 — Evaluation and POC Report

Deliver the structured evaluation that produces the management evidence for a
go/no-go decision on production investment.

| Item | Deliverable |
|---|---|
| Item 8 | `AKR_EVAL_CASES.md` with minimum 10 documented test cases |
| Item 8 | Evaluation results for baseline Copilot vs AKR Space |
| Item 8 | One-page evaluation summary with metrics and go/no-go recommendation |

**Exit criteria:**
- All 10 test cases documented and executed against both configurations.
- All summary metrics calculated.
- Mode accuracy ≥ 80% in AKR Space configuration.
- Conflict detection rate = 100% for tested conflict scenarios.
- Evaluation summary reviewed and signed off before management presentation.

---

## POC Boundary Declaration

This plan delivers an **instruction-governed Copilot Space** layered on top of GitHub's
native retrieval infrastructure. It does not deliver a custom retrieval engine or
programmatic enforcement of behavioral policies. The following limitations are known
and accepted for the POC phase:

| Limitation | Impact | Resolution path for production |
|---|---|---|
| Space retrieval is GitHub-managed and non-deterministic at the file level | Copilot selects which indexed content to surface; not every relevant file is guaranteed to appear in every response | Custom retrieval pipeline via GitHub Copilot API or VSCode extension |
| Behavioral policies are instruction-enforced, not code-enforced | Copilot follows the Space instruction with high but not absolute consistency; edge cases will exist | Programmatic pre-synthesis gate in a custom Chat participant |
| Space instruction has a token limit | If the instruction grows beyond the field limit, lower-priority sections must be trimmed or moved to an attached reference file | Structured system prompt via Copilot API |
| Capability inference is LLM-based | Resolution policy improves consistency but cannot guarantee correct capability identification for all question phrasings | Deterministic capability resolver service |
| Capability map must be manually re-attached after updates | Map staleness is not automatically detected by the Space; CI warning depends on developers acting on it | Automated map generation and attachment via GitHub Actions |

The POC validates whether an instruction-governed Space produces sufficiently reliable
scoped retrieval to justify investment in the production-grade implementation above.
The evaluation in Sprint 5 produces the evidence for that decision.

---

## Artifact Checklist

| Artifact | Location | Owner | Sprint |
|---|---|---|---|
| Copilot Space (three repos configured) | GitHub Copilot Spaces | Space owner | 1 |
| `akr-capability-map.json` attached to Space | Copilot Space file resources | Space owner | 1 |
| `akr-capability-map.json` source file | Workspace root or AKR skill bundle | AKR team | 1 |
| Capability map generation script | AKR skill bundle or workspace utilities | AKR team | 1 |
| `AKR_SPACE_BOOTSTRAP.md` | `<business-docs-repo>/docs/` | Space owner | 1 |
| `AKR_SPACE_INSTRUCTION.md` | `<business-docs-repo>/docs/` | Space owner | 1 |
| Space instruction text (live) | Copilot Space instruction field | Space owner | 1 |
| Tuned Space instruction (post Sprint 2) | Space instruction field + `AKR_SPACE_INSTRUCTION.md` | Space owner | 2 |
| Extended `validate-documentation.yml` — backend repo | `.github/workflows/` in backend repo | AKR team | 3 |
| Extended `validate-documentation.yml` — UI repo | `.github/workflows/` in UI repo | AKR team | 3 |
| Consolidation repo artifact completeness check | `.github/workflows/` in consolidation repo | AKR team | 3 |
| `AKR_COPILOT_QUICKSTART.md` | `<business-docs-repo>/docs/` | AKR team | 4 |
| `AKR_EVAL_CASES.md` | `<business-docs-repo>/docs/references/` | POC lead | 5 |
| POC evaluation report | `<business-docs-repo>/docs/references/` | POC lead | 5 |
