# Management Review PR - Documentation-Only Change List

Date: 2026-04-12
Status: Draft for implementation
Scope: Documentation updates only. No code, schema, validator, workflow, or script changes in this PR.

## Purpose
This change list converts management review recommendations into concrete documentation edits that can be merged as a single PR. The goal is to make AKR easier to evaluate by narrowing pilot scope, improving onboarding clarity, and proactively disclosing known PoC limitations.

## PR Scope Guardrails
- Include only Markdown and documentation guidance changes.
- Do not modify Python scripts, JSON schemas, workflow YAML, or skill execution logic.
- Do not change validation behavior in this PR.
- Do not remove existing advanced guidance; move it to clearly labeled "Phase 2+" sections where needed.

## Proposed PR Title
`docs: add management-review pilot package and simplify first-run onboarding narrative`

## File-by-File Change List

## 1) Add a management-facing pilot package document

Target file:
- docs/AKR_MANAGEMENT_REVIEW_PILOT_PACKAGE.md (new)

Sections to add in full:
1. Executive Summary (1 page max)
2. Minimum Viable AKR Scope (Pilot)
3. Out of Scope (Phase 2+)
4. Pilot Structure (6-8 weeks)
5. Pilot Success Criteria
6. Known PoC Limitations and Mitigations
7. Human-in-the-Loop Ownership Table (Decision, Owner, Time)
8. Governance Signal for Pilot (single metric)
9. Evidence Pack Template (one-page results summary)

Content requirements:
- Define pilot workflow as: ProposeGroupings -> GenerateDocumentation -> inline validation -> PR merge.
- Limit pilot to one backend API repository and module-level docs.
- Declare semantic scoring as advisory for pilot.
- Declare consolidation as Phase 2+ for management evaluation.
- Include one governance metric: percent of merged module docs with zero unresolved ❓ markers.

Rationale:
- Creates one clear artifact management can evaluate without reading all architecture docs first.

## 2) Add a first-module quickstart document

Target file:
- docs/GETTING_STARTED_FIRST_MODULE.md (new)

Sections to add in full:
1. Who this is for
2. Four steps only
3. What to ignore for now (later-phase topics)
4. Definition of done for first module
5. Troubleshooting (minimal)

Exact 4-step flow to document:
1. Install VS Code GitHub extension and authenticate.
2. Run `/akr-docs groupings`.
3. Review and approve module entry in `modules.yaml`.
4. Run `/akr-docs generate <ModuleName>` and review draft/final output.

Required exclusions from this quickstart:
- No consolidation setup instructions.
- No semantic scoring instructions.
- No deep compliance graduation content.
- No cache maintenance details unless needed for troubleshooting.

Rationale:
- Reduces first-run cognitive load and supports pilot adoption velocity.

## 3) Update README to route readers to the new quickstart and pilot package

Target file:
- README.md

Sections to update:
1. Start Here
2. How Teams Use AKR
3. Governance, Compliance, and Human-in-the-Loop

Edits:
- In Start Here, add links to:
  - docs/GETTING_STARTED_FIRST_MODULE.md
  - docs/AKR_MANAGEMENT_REVIEW_PILOT_PACKAGE.md
- In How Teams Use AKR, add a short "Pilot Mode (Management Review)" subsection that points to the pilot package.
- In Governance section, add one sentence that pilot governance is measured primarily via unresolved-marker closure.

Rationale:
- Improves discovery and gives evaluators a clear entry path.

## 4) Refactor team onboarding guide for progressive disclosure

Target file:
- docs/TEAM_STARTUP_ONBOARDING_GUIDE.md

Sections to update:
1. 1. Who This Guide Is For
2. 2. Team Setup at a Glance
3. 6. Source Repository Developer Responsibilities
4. 7. Path A - Technical PO/TL: Local Workspace Mode
5. Path B section

Edits:
- Add a short preface at the top: "If you are onboarding your first module, start with docs/GETTING_STARTED_FIRST_MODULE.md."
- Keep all current detail, but add explicit labels:
  - "Pilot core path"
  - "Advanced / Phase 2+"
- In Developer Responsibilities, separate required-first-run steps from advanced operational steps.
- Move cache and cross-repo coordination detail into clearly marked advanced subsections.

Rationale:
- Preserves full guidance while reducing confusion for first-time users.

## 5) Add explicit PoC limitations document for transparent reliability communication

Target file:
- docs/POC_LIMITATIONS_AND_MITIGATIONS.md (new)

Sections to add in full:
1. Purpose of this document
2. Known limitations by workflow area
3. Impact to pilot outcomes
4. Current mitigations and operator guidance
5. Reliability threshold definition for pilot
6. Re-evaluation cadence

Required limitation entries:
- GenerateDocumentation truncation risk.
- Tool re-call / extra fetch behavior in deep passes.
- Mid-session partial save behavior for interview flow.

Required mitigation entries:
- Restart/re-run procedures.
- Use of split-pass strategy where applicable.
- Validator/manual checks before merge.

Rationale:
- Builds trust by proactively disclosing known behavior and mitigations.

## 6) Align architecture/governance docs to explicitly support phased pilot framing

Target files:
- docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md
- docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md

Sections to update in architecture doc:
1. Executive Summary
2. 5. Consolidation Layer
3. Compliance Operating Model
4. Suggested Additions for Ongoing Governance Reviews

Sections to update in solution-features doc:
1. Executive Summary
2. High-Level Capability Map
3. Governance, Compliance, and Human-in-the-Loop Design

Edits:
- Add concise "Phase 1 vs Phase 2+" framing language.
- Clarify that consolidation is an enabled target-state capability but optional for pilot success.
- Add short KPI statement for pilot evidence collection (quality delta, onboarding time, documentation effort).

Rationale:
- Keeps strategic vision intact while making pilot evaluation criteria explicit.

## 7) Clarify score-mode guidance as optional in pilot-facing docs

Target files:
- docs/TEAM_STARTUP_ONBOARDING_GUIDE.md
- docs/VALIDATION_GUIDE.md

Sections to update:
1. In onboarding command sequence section
2. In validation guidance where pilot/production behavior is described

Edits:
- Add wording: score mode is advisory in PoC and not required for pilot completion.
- Keep scoring documented as a quality signal for teams that opt in.

Rationale:
- Removes ambiguity between required workflow and optional quality signal.

## 8) Add management-ready one-page evidence template

Target file:
- docs/templates/MANAGEMENT_PILOT_RESULTS_ONE_PAGER.md (new)

Sections to add in full:
1. Pilot context (repo, team, duration)
2. Baseline vs after-AKR metrics table
3. Accuracy/completeness/hallucination summary
4. Onboarding time delta
5. Documentation effort delta
6. Governance metric result (unresolved ❓ at merge)
7. Recommendation: proceed / adjust / pause

Rationale:
- Standardizes pilot reporting for investment decisions.

## Suggested Commit Breakdown (single PR, multiple commits)
1. Add new management and quickstart docs.
2. Update README routing and onboarding progressive disclosure.
3. Add limitations and one-page evidence template.
4. Update architecture/solution/validation language for phased pilot framing.

## Acceptance Criteria for This PR
1. New readers can find a 4-step first-module path in under 1 minute from README.
2. Management can review a single pilot package document without reading implementation internals.
3. Known PoC reliability limitations are explicitly documented with mitigations.
4. All edits are documentation-only; no code or behavior changes are introduced.
5. Existing advanced guidance remains available and clearly marked as Phase 2+ where applicable.

## Explicit Non-Goals for This PR
- No changes to `.akr/scripts/validate_documentation.py`.
- No changes to `.akr/schemas/*.json`.
- No changes to `.github/skills/**` behavior scripts.
- No changes to CI workflows.

## Follow-Up PR (separate, optional)
If approved after documentation merge, open a separate implementation PR for behavior changes such as metadata simplification or workflow enforcement tuning. That work is intentionally excluded from this management-review documentation PR.
