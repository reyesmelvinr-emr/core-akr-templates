# Cross-Repository Consolidation Target State

Date: 2026-04-08
Status: Target-state definition
Scope: Define the steady-state model for skill-driven, business capability consolidation across onboarding source repositories and a business documentation repository.

## Purpose

This document defines the target end state for cross-repository business documentation consolidation.

- Cross-repository grouping uses `businessCapability` as the single semantic key.
- User interaction is delivered through agent skills in the AKR skill model.
- Source repositories contribute module-level documentation that is grouped by approved capability metadata.
- A dedicated business documentation repository receives consolidated capability artifacts.
- Repository names and capability names shown in examples are illustrative onboarding examples, not required naming conventions.

## High-Level Architecture

```text
+----------------------------------+
| Source Repository                |
| <source-repo-a>                  |
| docs/services/*.md               |
+----------------+-----------------+
                 |
                 |
                 v
+----------------------------------+
| AKR Consolidation Skill Family   |
| - capability-impact-analysis     |
| - capability-coverage-review     |
| - capability-relationship-mapping|
| - capability-consolidation       |
+----------------+-----------------+
                 |
                 | reads normalized metadata
                 | businessCapability, feature, layer
                 v
+----------------------------------+
| Capability Registry              |
| core-akr-templates/.akr/tags/    |
| tag-registry.json                |
+----------------+-----------------+
                 |
                 | validates approved
                 | businessCapability values
                 v
+----------------------------------+
| Consolidation Output Repository  |
| <business-docs-repo>             |
| docs/business-capabilities/*.md  |
+----------------+-----------------+
                 ^
                 |
+----------------+-----------------+
| Source Repository                |
| <source-repo-b>                  |
| docs/modules/*.md                |
+----------------------------------+
```

## Target-State Principles

1. `businessCapability` is the only cross-repository grouping key.
2. `feature` remains a required traceability field in `FN#####_US#####` format.
3. Consolidation is executed through skills aligned with the AKR mode-driven workflow.
4. Source repositories remain the system of record for module-level documentation.
5. Consolidated capability documents provide a business-level production view across layers.
6. Capability registry governance is required before consolidation writes are executed.
7. Consolidated documents are written for product owners, QA testers, and technical leads.
8. Consolidated content prioritizes business behavior, constraints, and outcomes.
9. During onboarding, the Product Owner defines the initial canonical `businessCapability` values and communicates them to documentation contributors for uniform source-repository usage.

## Canonical Metadata Model

| Field | Consolidation Role | Constraint |
|---|---|---|
| `businessCapability` | Primary grouping key across repositories | Must be an approved value in the capability registry |
| `feature` | Work-item traceability | Must follow `FN#####_US#####` |
| `layer` | Source layer indicator | Typical values: `UI`, `API`, `Database` |
| `project_type` | Source module context | Not used as a grouping key |
| `status` | Source maturity signal | Used for readiness and confidence |
| `compliance_mode` | Governance mode | Used for policy handling of unresolved markers |

## Example Application Capability Set

The following rows illustrate how a specific application may map source-layer documentation into approved business capabilities. Capability names remain application-defined and registry-governed.

| businessCapability | Backend Input | UI Input |
|---|---|---|
| `CourseManagement` | Course service/module docs | Course catalog docs |
| `EnrollmentManagement` | Enrollment service/module docs | Enrollments page docs |
| `UserManagement` | User service/module docs | Users page docs |

## Capability Registry Governance

### Registry authority

The capability registry is the single source of valid `businessCapability` values for consolidation.

Registry location:
`core-akr-templates/.akr/tags/tag-registry.json`

### Onboarding sequence

0. Product Owner defines and publishes the initial canonical `businessCapability` list for the application scope.
1. Normalize and approve capability names in the registry before source-repository consolidation work begins.
2. Cascade approved capability values to documentation contributors across participating source repositories.
3. For each new application repository, dispatch `distribute-onboarding-bundle.yml` (one-time, per repo) from `core-akr-templates`. This seeds `modules.yaml`, the AKR CODEOWNERS governance block, and the documentation PR template.
4. Confirm the following baseline files are present in the application repository after the onboarding bundle runs: `.akr-config.json`, `.github/workflows/validate-documentation.yml`, and `.github/copilot-instructions.md`. The onboarding bundle seeds each of these if absent; they are never overwritten once present.
5. Add the new application repository to `.github/registered-repos.yaml` in `core-akr-templates` via PR, then trigger `distribute-skill.yml` to distribute the `akr-docs` skill bundle and hooks.
6. Generate source-repository module documentation using the approved capability values.
7. Align source docs to approved values where needed.
8. Run assessment and consolidation only after registry alignment is complete.

### Team cascade requirement

After the initial capability list is defined, the values are cascaded to all documentation contributors (backend and UI) and used consistently in generated and edited module documentation.

### Provisioning model

The business documentation repository is provisioned in parallel with source onboarding.

Minimum prerequisites before first consolidation write:

- Output repository exists.
- Output path convention is defined.
- At least one approved `businessCapability` is present in the registry.

## Target Repository Contract

### Source repositories

- One or more application source repositories that publish module-level AKR documentation.
- Example onboarding set: `training-tracker-backend`, `training-tracker-ui`.

### Consolidation repository

- A business documentation repository for consolidated capability artifacts.
- Example onboarding repository: `training_tracker_business`.

### Output shape

```text
<business-docs-repo>/
  .akr-config.json
  .github/
    copilot-instructions.md
    skills/
      akr-business-consolidation/
        SKILL.md
  governance/
    review-workflow.md
    definition-of-done.md
  architectural/
    system-context.md
    business-capability-map.md
    diagrams/
      high-level-flow.png
  docs/
    business-capabilities/
      <CapabilityName>/
        index.md
        test-conditions.md
        enhancement-test-conditions.md
        enhancements.md
        limitations.md
        internal_dependencies.md
        external_dependencies.md
        traceability.md
        diagrams/
    references/
      glossary.md
      source-repo-map.md
      capability-registry-sync.md
  templates/
    business_capability_template.md
    capability_testing_template.md
    capability_enhancement_testing_template.md
    capability_enhancements_template.md
    capability_limitations_template.md
    capability_internal_dependencies_template.md
    capability_external_dependencies_template.md
    traceability-template.md
  validation/
    run-validation.ps1
    scripts/
      validate_business_docs.py
      validate_traceability.py
```

### Consolidation skill file contract

To support a repository-specific skill surface, `core-akr-templates` maintains a dedicated consolidation skill bundle separate from application module-documentation skills.

Required consolidation bundle shape in `core-akr-templates`:

- `.github/skills/akr-business-consolidation/SKILL.md`
- `.github/skills/akr-business-consolidation/scripts/*` for capability modes (`capability-impact-analysis`, `capability-coverage-review`, `capability-relationship-mapping`, `capability-consolidation`, `capability-test-maintenance`, `capability-test-generation`) as the implementation is introduced
- Optional compatibility and governance companion artifacts when adopted (for example `SKILL-COMPAT.md`)

### Distribution workflow contract for consolidation repositories

`core-akr-templates` must use a consolidation-specific distribution workflow for business documentation repositories.

Required workflow separation:

- Keep `.github/workflows/distribute-skill.yml` scoped to application code repositories and `akr-docs` artifacts.
- Add a dedicated workflow for consolidation repositories (for example `.github/workflows/distribute-business-skill.yml`) that distributes only consolidation-skill artifacts.
- Maintain a dedicated consolidation target registry (for example `.github/registered-business-repos.yaml`) to avoid coupling with application repository enrollment.

Required copy behavior for consolidation workflow:

- Copy consolidation skill assets only (`.github/skills/akr-business-consolidation/**`).
- Copy consolidation hook/validation assets only when explicitly part of the business-repo contract.
- Do not copy application `akr-docs` dispatcher or its scripts into consolidation repositories.
- Do not copy Vale rule packs or unrelated onboarding scaffolds as recurring distribution artifacts.

### Business-facing copilot-instructions contract

The consolidation repository should include a business-facing `.github/copilot-instructions.md` that guides capability-level, PO/QA/TL-oriented outputs.

Distribution safety rule:

- The consolidation distribution workflow must never overwrite an existing `.github/copilot-instructions.md` in the target repository.
- If the file does not exist, the workflow may seed a baseline business-facing version.
- If the file exists, preserve the current repository-owned file and continue skill distribution without modification.

### Rationale for split setup

This separation is required to keep architecture and governance aligned:

- Source repositories remain the system of record for module-level docs and require module-generation skills.
- Consolidation repositories produce business capability artifacts and require cross-repository synthesis skills.
- Separate workflows and registries prevent accidental artifact drift and reduce PR noise across unrelated repos.
- Independent release cadence allows app-skill and consolidation-skill evolution without forced cross-repository coupling.
- Preserving existing `copilot-instructions.md` maintains repository ownership and prevents unintentional local instruction loss.

### Ownership boundaries

To avoid implementation ambiguity, ownership is explicitly split:

- `core-akr-templates` owns skill definitions, distribution workflows, target-registries, and canonical templates.
- Application repositories own source code, modules manifests, module documentation, and local repo conventions.
- Consolidation repositories own business-facing capability outputs and local editorial governance decisions.
- Existing local `.github/copilot-instructions.md` files in target repositories remain repository-owned artifacts.

Within each capability folder:

- `index.md` is the primary output of `capability-consolidation`.
- `test-conditions.md` captures QA-oriented acceptance and edge-case conditions.
- `enhancement-test-conditions.md` captures enhancement-driven test scenarios and change-cycle test additions separate from baseline coverage.
- `enhancements.md` records ongoing capability enhancements, including Product Owner business requirements, Technical Lead technical requirements, and optional Azure DevOps work-item references.
- `limitations.md` records known business or technical limitations for the capability and any established application-team workarounds.
- `limitations.md` may reference rule IDs from `index.md` when the limitation is directly tied to a documented rule for traceability.
- `internal_dependencies.md` records dependency and impact relationships to other capabilities, processes, or functions within the current application that must be considered when changes are made to the current capability.
- `external_dependencies.md` records interfaces and dependency relationships with external applications or platforms that interact with the current application and may be affected by capability changes.
- Internal and external dependency documents support impact-aware planning and help QA testers derive cross-capability and integration-oriented test cases when enhancements are introduced.
- `traceability.md` maps consolidated claims to source evidence, including source repository, source document path, section reference, and validation notes.
- `diagrams/` stores capability-specific visuals relevant to Product Owner and business-owner review.

### Canonical template sources

The canonical consolidation templates are stored in `core-akr-templates/templates` and used by consolidation skills when producing capability artifacts:

- `business_capability_template.md` -> pattern for `docs/business-capabilities/<Capability>/index.md`
- `capability_testing_template.md` -> pattern for `docs/business-capabilities/<Capability>/test-conditions.md`
- `capability_enhancement_testing_template.md` -> pattern for `docs/business-capabilities/<Capability>/enhancement-test-conditions.md`
- `capability_enhancements_template.md` -> pattern for `docs/business-capabilities/<Capability>/enhancements.md`
- `capability_limitations_template.md` -> pattern for `docs/business-capabilities/<Capability>/limitations.md`
- `capability_internal_dependencies_template.md` -> pattern for `docs/business-capabilities/<Capability>/internal_dependencies.md`
- `capability_external_dependencies_template.md` -> pattern for `docs/business-capabilities/<Capability>/external_dependencies.md`
- `traceability-template.md` -> pattern for `docs/business-capabilities/<Capability>/traceability.md`

For environments that still reference the legacy naming, `capabilitytTesting_template.md` is maintained as an alias pointing to the same testing template contract.

For local compatibility in consolidation repositories, legacy local template filenames may exist as aliases, but canonical generation contracts remain bound to the template names listed above.

## Skill Surface

### capability-impact-analysis

Purpose: Identify capabilities affected by documentation or implementation changes.

Outputs:
- Affected capability list
- Changed source module map
- Re-consolidation recommendation

### capability-coverage-review

Purpose: Assess whether each capability has sufficient and valid source material for consolidation.

Outputs:
- Coverage matrix by capability and layer
- Metadata quality findings
- Readiness recommendation

### capability-relationship-mapping

Purpose: Produce cross-layer relationship summaries for a selected capability.

Outputs:
- UI-to-API relationship flow
- Integration assumptions and gaps

### capability-consolidation

Purpose: Generate or refresh a business capability document in the business documentation repository.

Outputs:
- `index.md` rendered from `core-akr-templates/templates/business_capability_template.md`
- `test-conditions.md` rendered from `core-akr-templates/templates/capability_testing_template.md`
- `enhancements.md` rendered from `core-akr-templates/templates/capability_enhancements_template.md`
- `limitations.md` rendered from `core-akr-templates/templates/capability_limitations_template.md`
- `internal_dependencies.md` rendered from `core-akr-templates/templates/capability_internal_dependencies_template.md`
- `external_dependencies.md` rendered from `core-akr-templates/templates/capability_external_dependencies_template.md`
- `traceability.md` rendered from `core-akr-templates/templates/traceability-template.md`
- Source-to-section traceability entries and confidence markers

Template usage rules:

- `index.md` is the primary source of truth for scenario IDs and scenario descriptions.
- `test-conditions.md` must reference scenario IDs defined in `index.md` and provide detailed QA steps.
- `enhancements.md` tracks active and planned enhancement work for the capability and may include links to delivery-system records such as Azure DevOps Boards.
- `limitations.md` captures operationally relevant capability limitations and associated workarounds, and may cite rule IDs from `index.md` for traceability.
- `internal_dependencies.md` captures downstream and adjacent in-application capability impacts that must be considered for design review, change planning, and QA scenario expansion.
- `external_dependencies.md` captures cross-application interfaces and integration impacts that must be considered for change planning, regression scope, and end-to-end QA coverage.
- Scenario and test condition IDs must remain synchronized (`SCN-*` <-> `TC-*`) across both files.

### capability-test-maintenance

Purpose: Update existing test scenarios and test conditions to reflect the latest consolidated capability baseline.

Inputs:
- `index.md` as the primary source of scenario intent and baseline behavior.
- `limitations.md` for constraints and workaround-aware test adjustments.
- `internal_dependencies.md` for in-application impact and regression scope updates.
- `external_dependencies.md` for integration-aware impact and regression scope updates.

Outputs:
- Updated `test-conditions.md` aligned to current `index.md` scenario definitions.
- Revised test-condition steps and expected outcomes for impacted baseline behaviors.
- Change notes identifying updated coverage areas and dependency-driven additions.

### capability-test-generation

Purpose: Generate new test scenarios and test conditions for enhancement-driven changes while preserving existing capability behavior.

Inputs:
- `enhancements.md` as the source of proposed business and technical changes.
- `index.md` as the comparison baseline for existing behavior and rule intent.
- `limitations.md` for known constraints that influence enhancement test design.
- `internal_dependencies.md` for cross-capability change impact within the application.
- `external_dependencies.md` for cross-application integration impact.

Outputs:
- Newly proposed test scenarios and test conditions added to `enhancement-test-conditions.md`.
- Baseline-versus-change impact coverage that identifies affected existing functionality.
- Enhancement-focused edge-case and regression test additions for QA execution.

## Audience and Language Contract

### Primary audience

- Product Owner: Validates business behavior and policy intent.
- Quality Assurance Tester: Derives test cases, edge cases, and acceptance expectations.
- Technical Lead: Validates cross-layer consistency and production behavior alignment.

### Language expectations

Consolidated documents must:

- Use business-facing language.
- Describe what the system does in production terms.
- Include edge cases, conditional rules, and constraints.
- Keep implementation details in references or annexes.

Consolidated documents must not:

- Depend on class, DTO, controller, or entity terminology as primary narrative.
- Require architecture expertise to understand business behavior.
- Omit rule conditions that are necessary for QA test design.

## Operational Workflow

### Phase A: Define

The application team, led by the Product Owner, defines the initial business capability set and aligns those values in the capability registry early in onboarding.

### Phase B: Assess

Run `capability-impact-analysis` for change-driven updates and `capability-coverage-review` for readiness validation.

### Phase C: Consolidate

Run `capability-consolidation` per capability into the business documentation repository.

### Phase D: Maintain Tests

Run `capability-test-maintenance` to refresh existing test conditions using the latest `index.md` baseline and supporting limitation and dependency artifacts.

### Phase E: Generate Enhancement Tests

Run `capability-test-generation` to create new enhancement-focused tests from `enhancements.md` compared against `index.md`, with limitation and dependency considerations.

### Phase F: Explain

Run `capability-relationship-mapping` when cross-layer explanation is needed without file generation.

### Phase-to-skill execution map

| Phase | Workflow name | Skill(s) | Primary trigger | Primary outputs |
|---|---|---|---|---|
| A | Define | Human-led registry and onboarding setup | New application onboarding | Canonical `businessCapability` list and repository prerequisites |
| B | Assess | `capability-impact-analysis`, `capability-coverage-review` | Source documentation change or onboarding readiness check | Impact list, coverage matrix, readiness recommendation |
| C | Consolidate | `capability-consolidation` | Phase B ready state | Capability document set (`index.md`, test artifacts, dependencies, traceability) |
| D | Maintain tests | `capability-test-maintenance` | Baseline capability change without new enhancement scope | Updated `test-conditions.md` aligned to baseline scenarios |
| E | Generate enhancement tests | `capability-test-generation` | Enhancement scope defined in `enhancements.md` | Updated `enhancement-test-conditions.md` |
| F | Explain | `capability-relationship-mapping` | On-demand architecture and impact explanation request | Cross-layer relationship summary |

### POC readiness status (as of 2026-04-10)

The target-state architecture is directionally defined, but the current implementation is not yet fully ready for onboarding any arbitrary application repository in the proof-of-concept phase.

| Severity | Current gap | Evidence summary | Required action |
|---|---|---|---|
| Critical | Consolidation skill family is not yet implemented in `core-akr-templates` | Expected path `.github/skills/akr-business-consolidation/` is absent in `core-akr-templates` | Add consolidation skill dispatcher, mode scripts, and companion artifacts in `core-akr-templates` |
| Critical | Distribution registry is not yet broad enough for cross-repository POC | `.github/registered-repos.yaml` currently lists backend repo only | Add UI and additional POC repositories to app registry; maintain a separate consolidation registry |
| High | Backend baseline configuration is incomplete | `training-tracker-backend` currently has no `.akr-config.json` while UI and business repositories do | Add backend `.akr-config.json` seed and validate against `akr-config-schema.json` |
| High | Consolidation output repository baseline is partial | `training_tracker_business` has only partial capability artifacts and no business-facing `.github/copilot-instructions.md` | Complete capability folder artifact set and seed business-facing instructions if file is absent |
| High | Consolidation distribution workflow is defined conceptually but not yet implemented | Target state specifies dedicated consolidation distribution, but only app-oriented distribution workflow exists currently | Implement `.github/workflows/distribute-business-skill.yml` and `.github/registered-business-repos.yaml` |
| Medium | Local template naming drift can cause confusion | Existing business-repo local template names differ from canonical names listed in this target-state contract | Adopt canonical template naming for generation, support local aliases only for compatibility |

### POC readiness gates

The following gates must all pass before declaring cross-repository POC onboarding readiness for new application repositories.

| Gate | Exit criteria | Validation evidence |
|---|---|---|
| Gate 1: Core skill readiness | Both skill families exist in `core-akr-templates` (`akr-docs` and `akr-business-consolidation`) with versioned invocation contracts; all eight canonical consolidation templates are present in `core-akr-templates/templates/` | Presence of skill files and scripts under `.github/skills/`; presence of all eight template files under `templates/` |
| Gate 2: Distribution readiness | App distribution and consolidation distribution workflows both exist and use separate target registries | Workflow files present; registry files present; workflow dry-run or dispatch evidence |
| Gate 3: Source repo onboarding baseline | New app repository contains required AKR files (`modules.yaml`, `.akr-config.json`, skill bundle, hooks, validation workflow, repo-owned instructions); `distribute-onboarding-bundle.yml` has been dispatched for the repository and absence-seeded files are confirmed present | Repository file audit against onboarding checklist; PR evidence from `distribute-onboarding-bundle.yml` run |
| Gate 4: Registry and metadata readiness | Source documentation metadata values (`businessCapability`, `feature`, `layer`) are normalized and valid | Validation output showing alignment to capability registry and front matter constraints |
| Gate 5: Consolidation baseline readiness | Consolidation repository contains business-facing instructions, full capability artifact shape, and validation coverage | File audit and validation script output |
| Gate 6: End-to-end execution readiness | One full run succeeds for a sample capability across Assess -> Consolidate -> Test Maintenance/Generation | Traceability evidence and generated capability artifacts reviewed by PO/QA/TL |

### Clarification on references and annexes

Implementation details that are not primary business narrative should be placed in repository references (for example `docs/references/`) or annex-style supporting sections linked from capability documents.

Examples of reference/annex content:

- Source repository mappings and path-level traceability detail.
- Registry synchronization notes and normalization evidence.
- Integration assumptions and implementation caveats not required for primary business readability.

## Scope

This target-state definition includes:

- Capability-centric consolidation model
- Registry governance and sequencing
- Skill surface and workflow
- Audience and language contract
- Consolidation repository output contract

This target-state definition excludes:

- Skill implementation details
- CI pipeline and branch policy design
- Deterministic script implementation

## Decisions

1. Consolidation is capability-centric and skill-driven.
2. `businessCapability` is the canonical grouping field.
3. Registry normalization is required early in onboarding before consolidation writes.
4. A dedicated business documentation repository is the consolidation destination, with `training_tracker_business` as an example implementation.
5. Consolidated outputs are designed primarily for PO/QA/TL consumption.
6. Consolidated documents are treated as production-state business behavior references.

## Next Planning Artifact

Implementation details are defined in:

- `planning/CROSS_REPOSITORY_POC_IMPLEMENTATION_PLAN.md`
