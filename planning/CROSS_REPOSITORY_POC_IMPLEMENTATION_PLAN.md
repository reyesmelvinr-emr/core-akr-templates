# Cross-Repository POC Implementation Plan

Date: 2026-04-10
Status: execution-ready
Scope: Deliver end-to-end proof-of-concept readiness so any application repository can onboard to `core-akr-templates` and participate in capability consolidation.

## Objective

Execute the target-state architecture with two skill-distribution tracks:

- Application repository track (`akr-docs`) for module documentation.
- Consolidation repository track (`akr-business-consolidation`) for business capability rollups.

The plan prioritizes deterministic onboarding, explicit ownership boundaries, and verifiable readiness gates.

## Current-state baseline (confirmed)

- App skill distribution exists and is active through `.github/workflows/distribute-skill.yml`.
- A separate first-touch onboarding workflow exists at `.github/workflows/distribute-onboarding-bundle.yml` and must be run once per new app repository to seed `modules.yaml`, CODEOWNERS governance block, and PR documentation template. This workflow is distinct from the recurring skill distribution and is not referenced in the current planning artifacts.
- App target registry is incomplete (`.github/registered-repos.yaml` currently includes backend only).
- Consolidation skill family is not yet implemented in `core-akr-templates`.
- Only two of eight canonical consolidation templates currently exist in `core-akr-templates/templates/` (`business_capability_template.md` and `capability_testing_template.md`). The remaining six are referenced in both planning documents as canonical but are not yet authored.
- Backend baseline is missing `.akr-config.json`; UI and business repositories already include `.akr-config.json`. No `.akr-config.json.seed` file exists in `examples/onboarding/`, meaning new repositories have no automated starting point for this required file.
- Business repository currently has partial capability artifact shape and no `.github/copilot-instructions.md`.

## Workstream A: Core Skill and Distribution Architecture

### A1. Add consolidation skill family in core

Deliverables:

- `.github/skills/akr-business-consolidation/SKILL.md`
- `.github/skills/akr-business-consolidation/scripts/capability-impact-analysis.md`
- `.github/skills/akr-business-consolidation/scripts/capability-coverage-review.md`
- `.github/skills/akr-business-consolidation/scripts/capability-relationship-mapping.md`
- `.github/skills/akr-business-consolidation/scripts/capability-consolidation.md`
- `.github/skills/akr-business-consolidation/scripts/capability-test-maintenance.md`
- `.github/skills/akr-business-consolidation/scripts/capability-test-generation.md`
- Optional: `.github/skills/akr-business-consolidation/SKILL-COMPAT.md`

Canonical consolidation templates (also required as part of this workstream):

Six of eight canonical templates are currently absent from `core-akr-templates/templates/`. These must be authored before consolidation skills can produce accurate output. Required additions:

- `templates/capability_enhancement_testing_template.md`
- `templates/capability_enhancements_template.md`
- `templates/capability_limitations_template.md`
- `templates/capability_internal_dependencies_template.md`
- `templates/capability_external_dependencies_template.md`
- `templates/traceability-template.md`

Acceptance criteria:

- Dispatcher and mode scripts are present in `core-akr-templates`.
- Invocation contracts map 1:1 to target-state phases.
- Scripts enforce metadata checks for `businessCapability`, `feature`, and `layer`.
- All eight canonical consolidation templates are present in `core-akr-templates/templates/`.

### A2. Implement consolidation distribution workflow

Deliverables:

- `.github/workflows/distribute-business-skill.yml`
- `.github/registered-business-repos.yaml`

Distribution rules:

- Distribute only consolidation skill artifacts to consolidation repositories.
- Do not distribute app `akr-docs` artifacts through this workflow.
- Do not distribute unrelated onboarding scaffolds on recurring runs.

Acceptance criteria:

- Workflow supports `workflow_dispatch` and targeted repo operation.
- Workflow creates branch and PR in each target consolidation repository.
- Workflow summary reports per-repo status and no-change outcomes.

### A3. Preserve repository-owned instructions

Required behavior:

- For `.github/copilot-instructions.md` in target consolidation repositories:
  - Seed only when absent.
  - Never overwrite existing file content.

Acceptance criteria:

- Workflow logic explicitly checks file existence before copy.
- PR output identifies whether file was seeded or preserved.

## Workstream B: Application Repository Onboarding Baseline

### B1. Complete app target enrollment

Deliverables:

- Update `.github/registered-repos.yaml` with all current POC app repositories.

Enrollment process:

Registry updates must be made via PR to `core-akr-templates`. The owning team submits the PR; the standards team approves per CODEOWNERS. This process must be documented as a short self-service instruction so new teams can self-enroll without requiring the core team to initiate the change.

Acceptance criteria:

- Registry includes backend and UI repositories for POC.
- App distribution workflow can target all enrolled app repositories.
- Self-service enrollment process is documented for future adopters.

### B2. Establish required baseline files for any app repo

App repo onboarding follows a two-phase sequence:

**Phase 1 (first-touch, one-time per repo): Run `distribute-onboarding-bundle.yml`**

This workflow must be dispatched once per new app repository. It seeds:

- `modules.yaml` (from `examples/onboarding/modules.yaml.seed` if absent)
- `.github/CODEOWNERS` (appends AKR governance block idempotently)
- `.github/pull_request_template/documentation.md`

**Phase 2 (recurring, triggered by tag or dispatch): Run `distribute-skill.yml`**

This workflow distributes the recurring skill bundle:

- `.github/skills/akr-docs/**` (dispatcher, compat matrix, mode scripts, validators)
- `.github/hooks/postToolUse.json` and `.github/hooks/agentStop.json`

**Required baseline files not yet covered by either workflow:**

- `.akr-config.json` — required for validation and skill behavior. No seed file or distribution mechanism currently exists. Deliverable: add `examples/onboarding/akr-config.json.seed` and update `distribute-onboarding-bundle.yml` to seed it if absent.
- `.github/workflows/validate-documentation.yml` — required for CI validation. Currently present in `core-akr-templates/.akr/workflows/` as a canonical template. Deliverable: the onboarding bundle or a dedicated distribution step must copy this into new app repositories. It must not be overwritten once the app team has customized path filters.
- `.github/copilot-instructions.md` — repo-owned. No seed mechanism exists for brand-new app repos. Deliverable: add `examples/onboarding/app-copilot-instructions.seed.md` and update the onboarding bundle to seed it if absent, following the same non-overwrite pattern used for consolidation repositories.

Immediate remediation item:

- Add missing `.akr-config.json` in backend repository using the seed to be created under `examples/onboarding/akr-config.json.seed`.

Acceptance criteria:

- `distribute-onboarding-bundle.yml` seeds `.akr-config.json`, `validate-documentation.yml`, and `copilot-instructions.md` if each is absent.
- Baseline file audit passes for backend and UI.
- Documentation validation workflow resolves expected file paths.

## Workstream C: Consolidation Repository Baseline

### C1. Complete capability output shape

Per capability folder, ensure presence of:

- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`
- `enhancements.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

Acceptance criteria:

- All configured capabilities have full required file set.
- Missing-file validation fails when any artifact is absent.

### C2. Align template contracts

Canonical template contract:

- `business_capability_template.md`
- `capability_testing_template.md`
- `capability_enhancement_testing_template.md`
- `capability_enhancements_template.md`
- `capability_limitations_template.md`
- `capability_internal_dependencies_template.md`
- `capability_external_dependencies_template.md`
- `traceability-template.md`

Compatibility rule:

- Legacy local naming may be retained as aliases only.

Acceptance criteria:

- Consolidation generation references canonical template names.
- Alias mapping is documented when legacy files are retained.

### C3. Add business-facing copilot instructions baseline

Deliverable:

- `.github/copilot-instructions.md` in each consolidation repository.

Acceptance criteria:

- Business-language and PO/QA/TL intent rules are explicit.
- Distribution process preserves existing local instructions.

## Workstream D: Validation and Readiness Automation

### D1. Add readiness validation checks

Validation scope:

- Registry alignment (`businessCapability` values approved in registry).
- Metadata format checks (`feature` pattern and layer validity).
- Artifact completeness checks (app and consolidation profiles).

Acceptance criteria:

- Pre-consolidation validation reports pass/fail with actionable diagnostics.
- Validation can run in CI and locally.

### D2. Gate implementation

Implement gate evidence for:

- Gate 1: core skill readiness
- Gate 2: distribution readiness
- Gate 3: source repo onboarding baseline
- Gate 4: registry and metadata readiness
- Gate 5: consolidation baseline readiness
- Gate 6: end-to-end execution readiness

Acceptance criteria:

- Each gate has an explicit evidence artifact path.
- Gate status can be reviewed in PR checks or release checklist.

## Workstream E: Pilot Rollout and Proof

### E1. Rollout order

1. Core implementation (Workstream A) — includes authoring the 6 missing canonical consolidation templates
2. Application baseline completion (Workstream B) — start by updating `distribute-onboarding-bundle.yml` to seed `.akr-config.json`, `validate-documentation.yml`, and app `copilot-instructions.md`; then run the bundle for each POC app repo; then trigger skill distribution
3. Consolidation baseline completion (Workstream C)
4. Validation and gates (Workstream D)
5. End-to-end pilot execution (Workstream E)

### E2. End-to-end pilot execution

Run a sample capability flow (recommended: `CourseManagement`):

- Assess (`capability-impact-analysis`, `capability-coverage-review`)
- Consolidate (`capability-consolidation`)
- Test maintenance/generation (`capability-test-maintenance`, `capability-test-generation`)
- Explain (`capability-relationship-mapping`) as needed

Acceptance criteria:

- Consolidated artifacts generated in target repository.
- Traceability links to real source evidence.
- PO/QA/TL review completed against governance workflow.

## Dependency map

- A1 precedes A2.
- A2 precedes E2.
- B1 and B2 can run in parallel with C1-C3 after A2 design is stable.
- D1 depends on A/B/C contracts being defined.
- D2 depends on D1 outputs and agreed evidence paths.
- E2 depends on A2, B2, C1, and D2.

## Risks and mitigations

Risk: registry drift between source docs and capability registry.
Mitigation: mandatory pre-consolidation registry validation and CI gating.

Risk: accidental overwrite of repository-owned instructions.
Mitigation: non-overwrite logic in distribution workflows and PR diff checks.

Risk: template drift between canonical and local names.
Mitigation: canonical-only generation with explicit alias mapping.

Risk: uneven onboarding quality across repos.
Mitigation: profile-specific onboarding checklist and gate evidence artifacts.

Risk: `.akr-config.json` version drift across app repositories due to manual creation.
Mitigation: seed file in `examples/onboarding/akr-config.json.seed` distributed by onboarding bundle; schema validation against `akr-config-schema.json` in CI.

Risk: onboarding bundle and skill distribution run out of order or skipped for new repos.
Mitigation: document the two-phase sequence explicitly; add a readiness check to the validation workflow that reports missing baseline files.

## Definition of ready for POC onboarding at scale

The program is considered ready to onboard any application repository when:

- Both distribution tracks are implemented and tested.
- App and consolidation registries are in place and maintained.
- Mandatory baseline files are validated for any new onboarded repo.
- Consolidation repositories can generate and validate full capability artifact sets.
- At least one end-to-end capability cycle has completed with PO/QA/TL approval evidence.
