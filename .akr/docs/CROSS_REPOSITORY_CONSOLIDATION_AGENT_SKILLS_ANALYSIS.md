# Cross-Repository Consolidation Agent Skills Analysis

Date: 2026-04-08
Status: Draft planning analysis
Scope: Replace outdated cross-repository consolidation guidance with a target-state design for agent-skill-driven business documentation consolidation.

## Purpose

This document replaces the planning assumptions in the older cross-repository consolidation guidance with a design that reflects the current AKR direction:

- Cross-repository grouping is driven by `businessCapability`, not by semantic `feature` names.
- The user-facing workflow should be implemented as agent skills, not MCP slash commands.
- The sample consolidation scenario should use `training-tracker-backend` and `training-tracker-ui` as source repositories and a future `training_tracker_business` repository as the consolidation target.

This is a target-state design with delta analysis. It is not an implementation spec for building the skills or creating the target repository.

## Source Documents Reviewed

1. [core-akr-templates/.akr/docs/CROSS_REPOSITORY_CONSOLIDATION.md](c:/Users/E1481541/OneDrive%20-%20Emerson/Documents/CDS%20-%20Team%20Hawkeye/AKR%20with%20MCP/core-akr-templates/.akr/docs/CROSS_REPOSITORY_CONSOLIDATION.md)
2. CROSS_REPOSITORY_FEATURE_CONSOLIDATION_IMPLEMENTATION.md
3. [core-akr-templates/planning/implementation_plans/PHASE_4_FEATURE_CONSOLIDATION.md](c:/Users/E1481541/OneDrive%20-%20Emerson/Documents/CDS%20-%20Team%20Hawkeye/AKR%20with%20MCP/core-akr-templates/planning/implementation_plans/PHASE_4_FEATURE_CONSOLIDATION.md)
4. [core-akr-templates/.github/skills/akr-docs/SKILL.md](c:/Users/E1481541/OneDrive%20-%20Emerson/Documents/CDS%20-%20Team%20Hawkeye/AKR%20with%20MCP/core-akr-templates/.github/skills/akr-docs/SKILL.md)
5. Training tracker sample documentation in backend and UI repositories, including:
   [training-tracker-backend/docs/services/Course_doc.md](c:/Users/E1481541/OneDrive%20-%20Emerson/Documents/CDS%20-%20Team%20Hawkeye/Training%20Test%20Workspace/training-tracker-backend/docs/services/Course_doc.md)
   [training-tracker-ui/docs/modules/CourseCatalogPage_doc.md](c:/Users/E1481541/OneDrive%20-%20Emerson/Documents/CDS%20-%20Team%20Hawkeye/Training%20Test%20Workspace/training-tracker-ui/docs/modules/CourseCatalogPage_doc.md)

## Why The Older Guidance Is Outdated

### 1. The grouping key changed

The older documents assume that cross-repository consolidation groups content by semantic `feature` names such as `ApplicationEditor` or `UserAuthentication`. That no longer matches the AKR direction used in the training tracker sample repositories.

Current AKR documentation requires:

- `businessCapability` as the semantic grouping key.
- `feature` as the work-item traceability field in `FN#####_US#####` format.

This means the older guidance is outdated at the taxonomy level. Any future cross-repository consolidation that still groups by semantic `feature` values will conflict with the current front matter contract.

### 2. The user workflow changed from commands to skills

The older guidance assumes a command surface such as:

- `/docs.list-features`
- `/docs.detect-changes`
- `/docs.consolidate`
- `/docs.map-relationships`
- `/docs.feature-coverage`

That is not the model used by the current AKR documentation system. The current pattern in [core-akr-templates/.github/skills/akr-docs/SKILL.md](c:/Users/E1481541/OneDrive%20-%20Emerson/Documents/CDS%20-%20Team%20Hawkeye/AKR%20with%20MCP/core-akr-templates/.github/skills/akr-docs/SKILL.md) is skill-oriented and mode-driven. Cross-repository consolidation should align with that pattern instead of introducing a second, command-specific user interface.

### 3. The old design assumed a generic documentation hub

The older documents assume a generic consolidation target such as `documentation-hub` or `feature-docs`, with generic examples and placeholder repos. That was useful for early exploration, but it does not match the current planning need.

The current target scenario is concrete:

- Source repo 1: `training-tracker-backend`
- Source repo 2: `training-tracker-ui`
- Consolidation target: `training_tracker_business`

The replacement design should describe this repo model directly instead of leaving the target as a generic aggregator example.

### 4. The branch and change-detection model was too implementation-specific

The older implementation guide goes deep on branch enforcement, command options, and change-detection mechanics tied to a command-oriented surface. That level of detail is not the right primary artifact for the new direction.

The current need is to define the skill responsibilities, inputs, outputs, and repository contracts first. Implementation details such as branch handling, git fetch depth, and change window parsing should follow later in a dedicated build plan if the skill set is approved.

### 5. The older naming examples no longer fit the sample domain

Examples like `ApplicationEditor`, `UserAuthentication`, and `DocumentGeneration` are useful as placeholders, but they are not the business capability vocabulary currently being normalized for the sample repositories.

For the training tracker scenario, the initial canonical capability set is:

- `CourseManagement`
- `EnrollmentManagement`
- `UserManagement`

The new design should adopt those capability names consistently.

## Target-State Principles

The future cross-repository consolidation model should follow these principles:

1. Use `businessCapability` as the only cross-repository grouping key.
2. Keep `feature` as a traceability field rather than a grouping field.
3. Expose consolidation through agent skills that match the existing AKR skill model.
4. Treat repository documentation as the source input and generate business-level rollups into a dedicated destination repository.
5. Keep the first target taxonomy intentionally narrow around the three initial training tracker business capabilities.
6. Separate target-state design from build-time implementation details.
7. The capability registry must be the single source of valid `businessCapability` values. It should be established before or in parallel with codebase documentation onboarding, not after consolidation starts.
8. Consolidated business capability documents are written for product owners and quality assurance testers, not for engineers. Language and structure must reflect that audience.

## Canonical Metadata Model

### Required interpretation

For cross-repository consolidation, the metadata should be interpreted as follows:

| Field | Meaning in consolidation | Notes |
|---|---|---|
| `businessCapability` | Primary grouping key across repositories | Must be a normalized, approved capability value |
| `feature` | Work-item lineage and traceability | Keeps the `FN#####_US#####` contract |
| `layer` | Source layer of the module document | Common values include `UI`, `API`, and `Database` |
| `project_type` | Per-repo module context | Not used as the consolidation grouping key |
| `status` | Maturity of the source document | Can influence readiness and confidence |
| `compliance_mode` | Governance mode of the source repo | Helps decide whether unresolved markers are acceptable |

### Canonical capability set for the training tracker sample

The initial normalized business capability set for cross-repository consolidation should be:

| Canonical `businessCapability` | Included sample repo sources | Notes |
|---|---|---|
| `CourseManagement` | Backend course service docs and UI course catalog docs | Normalize any course catalog phrasing into this capability |
| `EnrollmentManagement` | Backend enrollment docs and UI enrollment page docs | Represents enrollment lifecycle and related policies |
| `UserManagement` | Backend user docs and UI users page docs | Represents user administration and user records |

The design should not introduce `Admin` as a fourth business capability at this stage. Admin-related modules should remain out of the initial consolidation scope until the taxonomy and source coverage are clearer.

## Capability Registry Governance and Timing

### The sequencing challenge

A natural tension exists in the onboarding sequence: module-level documentation must be generated before all business capabilities for an application are fully known. During onboarding, the AI-generated module docs may use capability names that approximate what is intended rather than what is canonical.

Two valid approaches resolve this tension:

**Approach A: Define approximate capabilities before starting documentation generation**

An initial draft capability set is established in the tag registry before the first `/akr-docs generate` run starts. This set does not need to be final — rough, approximate names are acceptable provided they are registered. After a full generation pass, the registry is refined and module docs that used an unclaimed or approximate value are updated before the consolidation step begins.

**Approach B: Bootstrap from generated documentation, then normalize**

Generate module-level documentation without requiring a pre-approved capability set. After the generation pass, extract all `businessCapability` values from the generated front matter, deduplicate and normalize them, and register the approved set in the tag registry. Module docs that used interim or approximate values are then updated in a normalization pass before consolidation runs.

**Recommended approach for the training tracker sample**

Approach B is more practical for the initial onboarding of `training-tracker-backend` and `training-tracker-ui`. The three capability names that surfaced from the generated docs — `CourseManagement`, `EnrollmentManagement`, and `UserManagement` — should be registered in `core-akr-templates/.akr/tags/tag-registry.json` as approved entries before any consolidation step runs.

### Parallel provisioning of the consolidation repository

The consolidation repository `training_tracker_business` does not need to wait for full onboarding of the source repositories to be created. Provisioning it in parallel with the source repository onboarding has these advantages:

- The output structure and conventions can be established while source documentation is still being generated.
- The capability template and audience-focused document format can be drafted before the first consolidation run.
- Capability coverage gaps become visible early, before consolidation is attempted.

The minimum required before consolidation can write to `training_tracker_business` is:

- The repository exists.
- The output path convention is agreed upon.
- At least one business capability is registered in the tag registry with approved status.

## Target Audience and Document Tone

The documents generated in `training_tracker_business` serve a different readership than module-level AKR documentation in the source repositories. This difference should drive content decisions in both the consolidation template and the skill that generates it.

### Primary readers

| Reader | How they use the consolidated document |
|---|---|
| Product Owner | Reviews consolidated business rules to ensure the system behaves as intended. Approves or challenges rule interpretations before they are treated as authoritative for testing or compliance purposes. |
| Quality Assurance Tester | Uses business rules to derive test cases, edge cases, and expected outcomes. Relies on completeness of the rules to cover scenarios not described in user stories, requirements, or code comments. |
| Technical Lead | Uses the consolidated view to understand cross-cutting concerns, validate that implementation matches business intent, and identify gaps between what the system does and what the business expects. |

### Tone and language expectations

Consolidated capability documents should:

- Use business language rather than technical or implementation language. Refer to business concepts rather than class names, method signatures, or database columns.
- Describe what the system does from the perspective of the business, not how it is implemented.
- Favor complete sentences and plain descriptions over bullet dumps or code-oriented notation.
- Reserve technical implementation details for annexes or reference sections rather than primary content.

Consolidated capability documents should not:

- Lead with controller method names, DTO field names, or entity class names as primary content.
- Require the reader to understand software architecture to understand the business rules.
- Omit edge cases, eligibility constraints, or conditional logic on the assumption that a reader will infer them from the codebase.

### Role in the SDLC

In the normal software development lifecycle, the consolidated business capability documents in `training_tracker_business` represent the business rules reference for what the application does in Production. These documents are expected to be:

- **More complete than individual module-level documentation.** They deliberately include nuances, boundary conditions, and operational exceptions that module docs do not capture.
- **The authoritative input for QA teams** writing test cases and acceptance scenarios.
- **Updated when Production behavior changes**, not only when code changes occur.
- **Readable by non-engineers** involved in acceptance testing, compliance review, or business readiness activities.

The gap between what module-level documentation describes and what the consolidated business document should describe is intentional. Module-level docs describe the module's job. Business capability docs describe the application's behavior from a business perspective, including edge cases, ordering rules, eligibility logic, and operational assumptions that emerge from combining multiple modules across layers.

## Proposed Repository Model

### Source repositories

The future consolidation flow should treat the following repositories as inputs:

- `training-tracker-backend`
- `training-tracker-ui`

These repositories remain the system-of-record for module-level AKR documentation.

### Consolidation repository

The future consolidation destination should be a dedicated repository named `training_tracker_business`.

Its purpose should be:

- Store consolidated business capability documentation written for product owners and quality assurance testers, not for engineers.
- Present cross-layer business narratives that join UI and API module docs into a single production-state view of the application's behavior.
- Serve as the authoritative business rules reference for testing and acceptance activities.
- Capture nuances, boundary conditions, and operational scenarios that module-level documentation in source repositories does not record.
- Provide a stable review location for product-facing or business-facing documentation that should not live inside implementation repositories.

### Expected output shape

The initial output structure should be capability-centric rather than feature-centric.

Example structure:

```text
training_tracker_business/
  docs/
    business-capabilities/
      CourseManagement.md
      EnrollmentManagement.md
      UserManagement.md
```

This output naming is deliberate. It avoids reusing the older `docs/features/` convention, which is too closely tied to the outdated semantic model.

## Proposed Agent Skill Surface

Cross-repository consolidation should be modeled as a small skill family that mirrors the existing AKR mode-driven approach without copying the old slash commands.

### Skill 1: capability-discovery

Purpose:
List available business capabilities across participating repositories and summarize current documentation coverage.

Inputs:

- Source repository set
- Documentation root paths
- Optional capability filter

Outputs:

- Available `businessCapability` values
- Source documents found for each capability
- Layer coverage summary
- Missing coverage warnings

Primary user value:
Lets a user see what can be consolidated before any generation step runs.

### Skill 2: capability-impact-analysis

Purpose:
Determine which business capabilities are affected by recent documentation or code changes.

Inputs:

- Source repositories
- Comparison window or branch/ref selection
- Optional path filters

Outputs:

- Affected `businessCapability` values
- Changed modules and their source repos
- Confidence level for whether re-consolidation is needed

Primary user value:
Replaces the old `detect-changes` concept while keeping the result focused on capabilities instead of features.

### Skill 3: capability-consolidation

Purpose:
Generate or refresh a business capability document in `training_tracker_business` from approved source docs in the backend and UI repositories.

Inputs:

- Target `businessCapability`
- Participating source repositories
- Output repository and output path
- Consolidation template or section contract

Outputs:

- A capability rollup document
- Source-to-section traceability summary
- Gaps, unresolved assumptions, and missing layers

Primary user value:
This is the main replacement for the old `consolidate` action.

### Skill 4: capability-relationship-mapping

Purpose:
Summarize how UI and API modules relate within a business capability without necessarily writing output files.

Inputs:

- Target `businessCapability`
- Source documents or modules

Outputs:

- Textual layer flow
- Component-to-service relationship summary
- Documented integration gaps

Primary user value:
Provides the equivalent of the older relationship-mapping workflow while staying within the skill-based model.

### Skill 5: capability-coverage-review

Purpose:
Assess whether a business capability is ready for consolidation based on source-document completeness and metadata quality.

Inputs:

- Source repositories
- Capability set
- Validation rules

Outputs:

- Coverage matrix by capability and layer
- Missing module documentation warnings
- Readiness recommendation

Primary user value:
Replaces the older `feature-coverage` concept and gives a governance gate before rollup generation.

## Old Command Concepts To New Skill Equivalents

| Older concept | New skill-based equivalent | Updated terminology |
|---|---|---|
| `list-features` | `capability-discovery` | List business capabilities |
| `detect-changes` | `capability-impact-analysis` | Detect affected business capabilities |
| `consolidate` | `capability-consolidation` | Generate business capability documentation |
| `map-relationships` | `capability-relationship-mapping` | Map cross-layer capability relationships |
| `feature-coverage` | `capability-coverage-review` | Review capability readiness and gaps |
| `refresh-repos` | Fold into skill implementation or repository preflight, not a user-facing skill by default | Internal repository synchronization |

`refresh-repos` should not be preserved as a first-class user skill unless the eventual implementation proves that users need explicit control over repository synchronization. In the target model, repo refresh should be an internal preflight responsibility of the consolidation-oriented skills.

## Training Tracker Sample Mapping

### Current usable source mapping

The initial sample mapping should be:

| `businessCapability` | Backend source | UI source | Consolidation status |
|---|---|---|---|
| `CourseManagement` | Course module documentation | Course catalog module documentation | Ready for initial design mapping |
| `EnrollmentManagement` | Enrollment module documentation | Enrollments page documentation | Ready for initial design mapping |
| `UserManagement` | User module documentation | Users page documentation | Ready for initial design mapping, but source assumptions should be reviewed |

### Current gaps that affect consolidation readiness

The sample repositories are good enough to define the target design, but not yet complete enough to be treated as production-ready inputs.

Observed readiness gaps include:

- Backend and UI repositories still have modules without completed documentation.
- Some business capability alignment has required normalization from repo-specific naming into the canonical set.
- The initial sample does not yet include a dedicated database repository, so the first target state should assume UI and API inputs only.
- Some source documents are still in draft status, which means the consolidated output should preserve visible confidence markers or readiness warnings.

These are planning constraints, not blockers for writing the design.

## Recommended Consolidation Workflow

### Phase A: Discover

Use `capability-discovery` to inventory all normalized business capabilities across `training-tracker-backend` and `training-tracker-ui`.

Expected result:

- The skill reports `CourseManagement`, `EnrollmentManagement`, and `UserManagement`.
- The skill identifies the source docs and their layers.
- The skill flags missing or draft-only modules.

### Phase B: Review impact or readiness

Use `capability-impact-analysis` when the goal is change-driven refresh, or `capability-coverage-review` when the goal is readiness validation.

Expected result:

- The user sees which capabilities changed.
- The user sees whether a capability has enough source material to justify consolidation.

### Phase C: Consolidate

Use `capability-consolidation` to generate or refresh one business capability document in `training_tracker_business`.

Expected result:

- A single consolidated capability document is written.
- The output includes source references, current gaps, and layer coverage.

### Phase D: Explain relationships when needed

Use `capability-relationship-mapping` when the user needs cross-layer explanation without file generation.

Expected result:

- A concise textual relationship summary for the selected capability.

## Scope Boundaries

This document covers:

- Why the earlier cross-repository consolidation guidance is outdated.
- The target repository model for `training_tracker_business`.
- The use of `businessCapability` as the grouping key.
- The proposed agent skill family that replaces command-driven workflows.
- The training tracker sample-repo mapping used to ground the design.
- Capability registry governance and timing relative to onboarding.
- Target audience, document tone, and SDLC role for consolidated business documentation.

This document does not cover:

- Implementing the new skills.
- Creating the `training_tracker_business` repository.
- Writing `.akr-config.json` changes in the sample repositories.
- Building deterministic scripts, branch policies, or CI workflows.
- Producing final consolidated business documents.

## Decisions Recorded

1. Cross-repository consolidation should move to a skill-based interaction model.
2. `businessCapability` is the canonical cross-repository grouping field.
3. `feature` remains a required traceability field but is not the grouping key.
4. The initial training tracker target scope is limited to `CourseManagement`, `EnrollmentManagement`, and `UserManagement`.
5. The future consolidation output should live in `training_tracker_business` under a capability-centric path.
6. Admin-oriented and non-normalized modules remain outside the initial consolidation scope.
7. `businessCapability` values must be registered in the central tag registry before consolidation runs. Bootstrapping from generated docs followed by a normalization pass is the recommended approach for initial onboarding.
8. `training_tracker_business` can and should be provisioned in parallel with source repository onboarding, not sequentially after it.
9. Consolidated capability documents are written for product owners and QA testers. Language must be business-facing, not implementation-facing. Technical detail belongs in annexes or source-repo docs, not in the primary consolidated content.

## Recommended Next Step

If this design is accepted, the next document should be a focused implementation plan that defines:

- The exact skill filenames and descriptions.
- The repository contract for `training_tracker_business`.
- The output template for business capability rollups, written in alignment with the Target Audience and Document Tone requirements in this document.
- The preflight rules for source-repo discovery, normalization, and readiness validation.
- The registry setup sequence — specifically, when to register `businessCapability` values relative to onboarding documentation generation passes.
- The parallel provisioning checklist for `training_tracker_business` so it can be created while source repo onboarding is still in progress.