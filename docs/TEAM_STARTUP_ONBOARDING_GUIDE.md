# Team Startup Onboarding Guide

Date: 2026-04-11
Status: Active
Scope: Getting a team fully operational with AKR consolidation workflows from day one.

---

## 1. Who This Guide Is For

Source repo developers, Technical Leads, and Product Owners each have setup work that starts on the same day. The consolidation workflow depends on source documentation being in place first, which means the developer setup track and the PO/TL consolidation track run in parallel and coordinate — they do not execute in strict serial order.

This guide covers all three roles. Each has distinct responsibilities and setup steps.

| Role | Description | Setup path in this guide |
|---|---|---|
| **Technical PO / Technical Lead** | Has local access to both source (application) repos and the business consolidation repo. Runs consolidation skills directly across all repos. | [Path A — Local Workspace Mode](#path-a--technical-potl-local-workspace-mode) |
| **Non-Technical PO** | Has access to the business consolidation repo only. Relies on automated sync to bring source documentation into the consolidation repo. | [Path B — Source Evidence Mode](#path-b--non-technical-po-source-evidence-mode) |
| **Source Repository Developer** | Works in application codebases (backend, UI). Produces and maintains AKR module documentation that feeds the consolidation workflow. | [Source Repository Developer Responsibilities](#source-repository-developer-responsibilities) |

A single person can hold multiple roles. A Technical PO/TL typically holds all three.

---

## 2. Team Setup at a Glance

The following tracks run in parallel during onboarding. All three are required before the first consolidation run.

| Track | Who | What it produces |
|---|---|---|
| **Source repo setup** | Developers, Technical Lead | Application repos with module documentation, correct `businessCapability` metadata, and validation CI active |
| **Capability registry** | Product Owner, Technical Lead | Approved `businessCapability` values agreed and cascaded to all contributors |
| **Consolidation repo setup** | Product Owner / Technical Lead | Consolidation repo provisioned, skill bundle distributed, consolidation mode configured |

Before execution, classify each capability as `new` or `active` so the team uses the correct workflow branch.

```text
Day 1+
├── Developer track ──────────────────────────────────────────────────────────────→
│   Onboard source repos → generate module docs → normalize metadata → validate CI
│
└── PO/TL track ───────────────────────────────────────────────────────────────→
    Define capability registry → provision consolidation repo → configure mode (A or B)
                                                                        │
                                                     When dev track is ready:
                                                     └── Run consolidation skills
```

The Decision Tree below applies to the PO/TL track and determines which mode the consolidation skill uses to access source documentation.

---

## 3. Decision Tree: Choose Your Mode

Answer the following questions to determine your consolidation mode.

```
Q1: Do you have (or can you get) local clones of the application source repos
    on the same machine where you run VS Code for consolidation work?
    │
    ├─ Yes → Use Path A (local-workspace mode)
    │         You get direct, live access to source documentation.
    │         No sync workflow required.
    │
    └─ No  → Use Path B (source-evidence mode)
              Automated sync brings source docs into the consolidation repo.
              You only need the consolidation repo open in VS Code.
```

Both modes produce the same consolidation outputs. The difference is only in **where the skill reads source documentation from**.

---

## 4. Terminology

| Term | Meaning |
|---|---|
| **Source repo** | An application codebase repository (e.g., `training-tracker-backend`, `training-tracker-ui`) |
| **Consolidation repo** | The business documentation repository that aggregates capability artifacts (e.g., `training_tracker_business`) |
| **Source evidence** | A synced read-only snapshot of relevant documentation files from source repos, stored inside the consolidation repo |
| **Consolidation mode** | The configuration setting in `.akr-config.json` that tells the skill where to read source docs from |
| **businessCapability** | The approved registry key used to group module docs across repos (e.g., `CourseManagement`) |

---

## 5. Team Kickoff Prerequisites

Complete these steps as a team before starting individual path setup.

### 5.1 Capability registry alignment

The Product Owner and Technical Lead agree on and publish the initial canonical `businessCapability` values. This is a team decision that must happen before source repo documentation contributors begin generating module docs.

1. PO and TL define the capability list for your application scope (e.g., `CourseManagement`, `EnrollmentManagement`, `UserManagement`).
2. Submit values for approval in `core-akr-templates/.akr/tags/tag-registry.json` via PR.
3. Cascade approved values to all documentation contributors in source repos.
4. Require exact canonical values in module documentation front matter. Non-canonical values are normalization defects and block consolidation.
5. For each capability, record operational lifecycle status for workflow routing:
  - `new`: run capability-define workflow before coding handoff.
  - `active`: run enhancement workflow.

### 5.1.1 POC sequencing for new capability test conditions

When authoring `docs/business-capabilities/new/<CapabilityName>/test-conditions.md`:

1. PO drafts business-tier `TC-*` conditions.
2. TL appends technical-tier `TC-*` conditions.
3. PO/TL run one reconciliation pass.
4. Unresolved wording is split by ownership:
  - PO finalizes business acceptance wording.
  - TL finalizes technical feasibility wording.

### 5.2 Consolidation repository provisioned

The consolidation repository must exist, be governed, and have the consolidation skill bundle distributed to it.

1. Create the repository (see [docs/CONSOLIDATION REPO SETUP.md](CONSOLIDATION%20REPO%20SETUP.md) for the full consolidation repository setup checklist and target-state contract).
2. Ensure branch protection is enabled on the default branch.
3. Run `distribute-business-skill.yml` targeting this repository to install the consolidation skill bundle (`akr-business-consolidation` plus the PO/TL-facing `akr-capability` modes) and seed `.github/copilot-instructions.md` if absent.
4. Seed `.akr/tags/tag-registry.json` in the consolidation repo by copying the file from `core-akr-templates/.akr/tags/tag-registry.json` and committing it to the consolidation repository. The `distribute-business-skill.yml` workflow does not distribute the tag registry. Tag registry distribution is a manual step performed by the standards team owner whenever capability values change in `core-akr-templates`.
5. To refresh the tag registry after an approved capability update: pull the latest `core-akr-templates/.akr/tags/tag-registry.json`, copy it into the consolidation repo at `.akr/tags/tag-registry.json`, and open a PR. Do not edit the local copy directly — request capability name changes through `core-akr-templates`.
6. Treat `.akr/tags/tag-registry.json` in the consolidation repo as a read-only distributed artifact from `core-akr-templates`; request registry changes through the central repository instead of editing the local copy.

### 5.3 Source repositories have AKR module documentation

The consolidation workflow requires that source repositories already have:

- `.akr-config.json` (seeded by `distribute-onboarding-bundle.yml`)
- `modules.yaml` (seeded by `distribute-onboarding-bundle.yml`)
- Module documentation files with correct `businessCapability`, `feature`, `layer` front matter

If source repos are not yet onboarded, run `distribute-onboarding-bundle.yml` for each, then run `distribute-skill.yml` to install the application skill bundle (`akr-docs`, `akr-interview`, and the developer-facing `akr-capability` mode).

---

## 6. Source Repository Developer Responsibilities

Source repo developers produce the module documentation that the consolidation workflow depends on. This setup track runs in parallel with consolidation repo and PO/TL setup — developers do not need to wait for PO path configuration before starting.

### Step D0: Complete source repo onboarding

If the source repository has not yet been onboarded to AKR:

1. Have the AKR maintainer run `distribute-onboarding-bundle.yml` targeting this repository. This seeds `modules.yaml`, `.akr-config.json`, `validate-documentation.yml`, `copilot-instructions.md`, and the `notify-consolidation-on-doc-merge.yml` workflow.
2. Run `distribute-skill.yml` targeting this repository to install the `akr-docs`, `akr-interview`, and developer-facing `akr-capability` skill bundle.

### Step D1: Keep `modules.yaml` current

`modules.yaml` is the primary metadata index. Ensure it is updated whenever new modules are added or `businessCapability` values change.

```yaml
# Example entry
- name: CourseService
  path: docs/services/course-service.md
  businessCapability: CourseManagement
  layer: API
  feature: FN00001_US00001
  status: approved
  compliance_mode: pilot
```

### Step D2: Use approved `businessCapability` values

Every module document front matter must use an approved value from the capability registry. Unapproved values will cause consolidation skill validation failures.

If you are unsure of the current approved values, check `core-akr-templates/.akr/tags/tag-registry.json` or ask the PO/TL.

### Step D3: Generate module documentation

Use the `akr-docs` skill to generate and maintain module documentation:

```text
/akr-docs groupings                  ← discover and group modules into documentation units
/akr-docs generate <ModuleName>      ← generate draft module documentation
/akr-docs generate --batch <ModuleA ModuleB ...>  ← generate multiple approved modules (max 5)
/akr-docs resolve <DocFile>          ← close unknowns with HITL input
/akr-docs score <DocFile>            ← check documentation readiness score
```

Batch generate behavior:
- Batch mode validates all listed module names up front and requires `grouping_status: approved` for each.
- A single confirmation gate is shown after all drafts are written.
- Inline validation still runs per module.
- Semantic scoring is auto-skipped in batch mode; run `/akr-docs score <DocFile>` later for modules that need scoring metadata.

The `validate-documentation.yml` CI workflow runs automatically on documentation PRs. Address any failures before merging. Use `cache-status` and `update-cache` to maintain local fallback assets in `.akr/cache/` when remote GitHub access is unstable.

All module documentation must have correct `businessCapability`, `feature`, and `layer` front matter before the PO/TL can run consolidation.

### Step D4: Configure the notify dispatch workflow (Path B teams)

This step is only required if the PO/TL is using Path B (source-evidence mode).

The `notify-consolidation-on-doc-merge.yml` workflow is seeded into your source repo by `distribute-onboarding-bundle.yml`. After that:

1. Go to your source repo's `Settings > Secrets and variables > Actions > Variables`.
2. Add a new repository variable:
   - Name: `AKR_CONSOLIDATION_REPO`
   - Value: `owner/repo` of the business consolidation repository (e.g., `reyesmelvinr-emr/training_tracker_business`)
3. Confirm `AKR_DISTRIBUTION_PAT` secret is present (it should already be there from onboarding).

Once set, any merge to the default branch that touches `docs/services/**`, `docs/modules/**`, or `modules.yaml` will automatically notify the consolidation repo.

> **POC note:** The `notify-consolidation-on-doc-merge.yml` workflow is seeded automatically for POC convenience. If your team prefers opt-in control, you may disable the workflow in your source repo's Actions tab, or delete the file and use the manual `workflow_dispatch` path in the consolidation repo instead. Either mode is supported.

> **Python Web Applications:** Python projects (Django, FastAPI, Flask) follow the identical onboarding and consolidation workflow as .NET projects. The only difference is the `.akr-config.json` template you copy during source repo setup. Python API backends should start with `examples/akr-config-python-api.json` (instead of `examples/akr-config-webapp1-api.json`). All subsequent consolidation steps, governance gates, and metadata requirements are identical. See [copilot-instructions/backend-service.instructions.md — Python Role Mapping](../copilot-instructions/backend-service.instructions.md#python-role-mapping-framework-aware-guidance) for framework-to-AKR role equivalents.

---

## 7. Path A — Technical PO/TL: Local Workspace Mode

Use this path when you have local clones of both source repos and the consolidation repo.

In this mode the consolidation skill reads source documentation directly from your local workspace folders. No sync workflow is required.

### Step A1: Clone all repositories locally

Clone the consolidation repo and each source repo to your local machine.

```bash
# Example for training tracker setup
git clone https://github.com/your-org/training_tracker_business.git
git clone https://github.com/your-org/training-tracker-backend.git
git clone https://github.com/your-org/training-tracker-ui.git
```

### Step A2: Set up the multi-root VS Code workspace

1. Copy `core-akr-templates/examples/onboarding/akr-consolidation.code-workspace.seed` to your consolidation repo root.
2. Rename it: remove the `.seed` suffix so it becomes `akr-consolidation.code-workspace`.
3. Fill in the placeholder paths with your actual local clone paths:

```json
{
  "folders": [
    {
      "name": "business-consolidation-repo",
      "path": "."
    },
    {
      "name": "training-tracker-backend",
      "path": "REPLACE_WITH_ABSOLUTE_LOCAL_PATH_TO_BACKEND_REPO"
    },
    {
      "name": "training-tracker-ui",
      "path": "REPLACE_WITH_ABSOLUTE_LOCAL_PATH_TO_UI_REPO"
    }
  ],
  "settings": {}
}
```

4. Open: `File > Open Workspace from File...` and select `akr-consolidation.code-workspace`.
5. All three repos are now visible in your VS Code Explorer.

> The `.code-workspace` file is intentionally excluded from `.gitignore` in the seed. You may commit it to your consolidation repo if the team agrees on shared local paths, or keep it personal if paths differ per machine.

### Step A3: Configure `.akr-config.json` in the consolidation repo

Set `consolidation.mode` to `"local-workspace"` and list the local folder names matching your workspace entry names:

```json
{
  "consolidation": {
    "mode": "local-workspace",
    "sourceRepos": [
      "training-tracker-backend",
      "training-tracker-ui"
    ],
    "sourceEvidencePath": "docs/references/source-evidence"
  }
}
```

`sourceRepos` values here correspond to the `name` fields in your `.code-workspace` file, not GitHub repo paths.

### Step A4: Keep source repos current

Before running a consolidation skill, pull the latest from source repos:

```bash
cd training-tracker-backend && git pull
cd training-tracker-ui && git pull
```

This is the only ongoing responsibility for the local-workspace path.

### Step A5: Run consolidation skills

With all repos open in the multi-root workspace, invoke skills normally:

```
/akr-business-consolidation capability-coverage-review CourseManagement
/akr-business-consolidation capability-consolidation CourseManagement
```

The skill reads source docs from the local source repo workspace folders directly.

---

## 8. Path B — Non-Technical PO: Source Evidence Mode

Use this path when you work only in the consolidation repo. Automated sync brings source documentation into your repo before consolidation runs.

In this mode the skill reads from `docs/references/source-evidence/` inside the consolidation repo. You do not need source repos open locally.

### Step B1: Configure `.akr-config.json` in the consolidation repo

Set `consolidation.mode` to `"source-evidence"` and list the GitHub repo names:

```json
{
  "consolidation": {
    "mode": "source-evidence",
    "sourceRepos": [
      "your-org/training-tracker-backend",
      "your-org/training-tracker-ui"
    ],
    "sourceEvidencePath": "docs/references/source-evidence"
  }
}
```

### Step B2: Confirm the sync workflow is in place

The `sync-source-evidence.yml` workflow must be present in the consolidation repo's `.github/workflows/` folder. It is distributed there by `distribute-business-skill.yml`.

To verify:

```
consolidation-repo/
  .github/
    workflows/
      sync-source-evidence.yml    ← must be present
```

If missing, run `distribute-business-skill.yml` targeting the consolidation repo.

### Step B3: Initial sync — trigger manually

The first time, trigger the sync manually for each source repo using `workflow_dispatch`:

1. Go to the consolidation repo on GitHub.
2. Navigate to `Actions > Sync Source Evidence`.
3. Click `Run workflow`.
4. Enter the source repo (e.g., `your-org/training-tracker-backend`) and branch (e.g., `master`).
5. Repeat for each source repo.
6. Review and merge the resulting PRs.

After merge, the consolidation repo will have:

```
docs/
  references/
    source-evidence/
      training-tracker-backend/
        sync-manifest.json
        modules.yaml
        docs/
          services/
            course-service.md
            ...
      training-tracker-ui/
        sync-manifest.json
        modules.yaml
        docs/
          modules/
            course-catalog.md
            ...
```

### Step B4: Ongoing sync — event-driven (automatic after source setup)

Once source repo developers complete [Source Repository Developer Responsibilities](#source-repository-developer-responsibilities) Step D4, subsequent documentation merges in source repos will automatically trigger the sync workflow in the consolidation repo via `repository_dispatch`.

You will receive a PR in the consolidation repo whenever source documentation changes. Review and merge that PR, then run consolidation skills.

### Step B5: Run consolidation skills

With the evidence snapshot current (merged from the sync PR), invoke skills:

```
/akr-business-consolidation capability-coverage-review CourseManagement
/akr-business-consolidation capability-consolidation CourseManagement
```

The skill reads from `docs/references/source-evidence/` automatically when `consolidation.mode` is `source-evidence`.

---

## 9. First Consolidation Run Walkthrough

This is a step-by-step sequence for the very first capability run, regardless of mode.

| Step | Who | Action |
|---|---|---|
| 1 | PO | Confirm approved `businessCapability` values are in registry |
| 2 | Devs (source repos) | Confirm module docs have correct front matter metadata |
| 3 | PO/TL | Complete Path A or Path B setup |
| 4 | PO/TL | Run `/akr-business-consolidation capability-coverage-review [CapabilityName]` |
| 5 | PO/TL | Review coverage gaps and blockers. Address `❓` items before full consolidation |
| 6 | PO/TL | Run `/akr-business-consolidation capability-impact-analysis [CapabilityName]` if re-consolidating |
| 7 | PO/TL | Run `/akr-business-consolidation capability-consolidation [CapabilityName]` |
| 8 | PO | Review generated files in `docs/business-capabilities/<CapabilityName>/` |
| 9 | TL | Validate cross-layer consistency and traceability |
| 10 | Both | Open PR, sign off, merge |

**Tip:** Start with one capability (e.g., `CourseManagement`) for the first run. Verify the full artifact set is correct before running subsequent capabilities.

---

## 10. Governance Gates

### Gate 1 — Registry alignment

**Condition:** All `businessCapability` values used in source repo module docs match approved registry entries.

**Block:** Consolidation writes are blocked when non-canonical values are detected. The `capability-coverage-review` script reports mismatches.

### Gate 2 — Source evidence currency (Path B only)

**Condition:** `sync-manifest.json` `synced_at` is recent enough for the current consolidation run.

**Block:** No automated block, but the `traceability.md` file will include the sync timestamp for reviewer inspection.

### Gate 3 — Capability completeness

**Condition:** Each capability folder contains all required files for its lifecycle status.

**Active capabilities** require all nine files:
- `index.md`, `test-conditions.md`, `enhancement-test-conditions.md`, `enhancements.md`, `backlog.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md`

**New capabilities** require five files (no enhancement/backlog/traceability artifacts):
- `index.md`, `test-conditions.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`

**Archived capabilities** require five files (read-mostly historical baseline):
- `index.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md`

**Block:** Consolidation writes are blocked when any status-specific requirement is missing. The validation script reports completeness by status and designates missing files as errors or (for archived/new) as warnings if non-critical section headers are absent.

---

## 11. References

| Document | Purpose |
|---|---|
| [docs/CONSOLIDATION REPO SETUP.md](CONSOLIDATION%20REPO%20SETUP.md) | Consolidation repository setup, target-state architecture, and repository contracts |
| [planning/CROSS_REPOSITORY_POC_IMPLEMENTATION_PLAN.md](../planning/CROSS_REPOSITORY_POC_IMPLEMENTATION_PLAN.md) | POC implementation workstreams and acceptance criteria |
| [docs/AKR_PROPOSED_ARCHITECTURE_ONBOARDING_AND_SKILLS.md](AKR_PROPOSED_ARCHITECTURE_ONBOARDING_AND_SKILLS.md) | Full architecture diagram and skills inventory |
| [docs/DEVELOPER_REFERENCE.md](DEVELOPER_REFERENCE.md) | HITL role alignment and configuration reference |
| [docs/VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) | Validation rules and CI enforcement |
| [examples/onboarding/](../examples/onboarding/) | All seed files referenced in this guide |
