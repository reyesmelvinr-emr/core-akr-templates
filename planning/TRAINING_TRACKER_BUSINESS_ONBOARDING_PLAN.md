# Training Tracker Business Repository Onboarding Plan

Date: 2026-04-08
Status: Draft
Scope: Onboard the consolidation repository training_tracker_business into core-akr-templates workflows, beginning with repository creation.

## Purpose

This plan defines how to stand up and onboard the training_tracker_business repository as the business documentation consolidation target for training-tracker-backend and training-tracker-ui.

The plan is intentionally front-loaded with repository creation, then runs in parallel with source codebase onboarding activities.

## Outcome Definition

At completion, training_tracker_business will:

- Exist as a provisioned and governed repository.
- Follow an agreed folder and document contract for business capability outputs.
- Be integrated into the AKR consolidation workflow.
- Have active review ownership by Product Owner and Technical Lead.
- Be ready to receive capability rollups for CourseManagement, EnrollmentManagement, and UserManagement.

## Phase 0: Create The Repository First

### Step 0.1 Repository provisioning

Create repository:

- Name: training_tracker_business
- Owner: target organization or owner account used for training tracker assets
- Visibility: internal or private (recommended)
- Default branch: main

### Step 0.2 Core controls and governance

Configure baseline governance immediately after creation:

- Branch protection on main
- Pull request required for direct updates
- Required reviewers include Product Owner and Technical Lead for business capability documents
- Issue templates for capability change requests and rule clarification requests
- Labels for status and ownership, such as capability, qa-ready, po-review, tl-review

### Step 0.3 Product Owner capability definition and team cascade

Before consolidation starts, the Product Owner defines the initial canonical `businessCapability` values for the application scope and publishes them for the team.

Initial list for training tracker:

- CourseManagement
- EnrollmentManagement
- UserManagement

Cascade actions:

- Share approved values with backend and UI documentation contributors.
- Require these exact values in module documentation front matter updates.
- Treat non-canonical values as normalization defects before consolidation.

### Step 0.4 Initial repository scaffolding

Initialize required files:

- README.md
- CONTRIBUTING.md
- CODEOWNERS
- .akr-config.json
- .github/skills/akr-business-consolidation/SKILL.md
- docs/ root and capability folders
- governance/ and architectural/ root folders
- templates/ for consolidation output templates
- validation/ with scripts/ for document quality checks

## Parallel Delivery Model

The onboarding should run as two coordinated tracks.

Track A: Source codebase onboarding

- Continue module documentation onboarding in training-tracker-backend.
- Continue module documentation onboarding in training-tracker-ui.
- Normalize businessCapability metadata values.

Track B: Consolidation repository onboarding

- Create and govern training_tracker_business.
- Finalize folder structure and template contract.
- Define review workflow with Product Owner and Technical Lead.

Both tracks should run in parallel and synchronize on explicit readiness gates.

## Synchronization Gates

Gate 1: Repository readiness

- training_tracker_business created
- Branch protection and CODEOWNERS active
- Folder structure committed

Gate 2: Metadata readiness

- businessCapability values normalized and approved in central registry
- Initial capability set confirmed: CourseManagement, EnrollmentManagement, UserManagement
- Product Owner-published canonical value list has been communicated to all documentation contributors

Gate 3: Consolidation readiness

- Consolidation template approved by Product Owner and Technical Lead
- First pilot capability selected for initial consolidation write

## Product Owner and Technical Lead Involvement

### Product Owner responsibilities

- Validate business rule intent and production behavior statements.
- Approve business-facing language and completeness for acceptance use.
- Confirm that capability documents match policy and business outcomes.

### Technical Lead responsibilities

- Validate cross-layer consistency between API and UI narratives.
- Confirm technical feasibility of documented behavior claims.
- Approve traceability and quality gates before publication.

### Joint approval model

A capability document is considered approved when:

- Product Owner signs off on business correctness.
- Technical Lead signs off on cross-layer consistency and implementation alignment.

## Proposed Folder Structures

Option A: Lean structure (recommended for initial rollout)

training_tracker_business/
  README.md
  CONTRIBUTING.md
  CODEOWNERS
  .akr-config.json
  .github/
    skills/
      akr-business-consolidation/
        SKILL.md
  governance/
    review-workflow.md
  architectural/
    system-context.md
    business-capability-map.md
    diagrams/
  docs/
    business-capabilities/
      CourseManagement/
        index.md
        test-conditions.md
        traceability.md
        diagrams/
      EnrollmentManagement/
        index.md
        test-conditions.md
        traceability.md
        diagrams/
      UserManagement/
        index.md
        test-conditions.md
        traceability.md
        diagrams/
    references/
      glossary.md
      source-repo-map.md
      capability-registry-sync.md
  templates/
    capability-rollup-template.md
    business-rules-template.md
    qa-test-conditions-template.md
    traceability-template.md
  validation/
    run-validation.ps1
    scripts/
      validate_business_docs.py
      validate_traceability.py

Option B: Expanded structure (for scaling after pilot)

training_tracker_business/
  README.md
  CONTRIBUTING.md
  CODEOWNERS
  .akr-config.json
  .github/
    skills/
      akr-business-consolidation/
        SKILL.md
  governance/
    review-workflow.md
    definition-of-done.md
    confidence-markers.md
  architectural/
    system-context.md
    business-capability-map.md
    operating-model.md
    diagrams/
      high-level-system-flow.png
      business-process-map.png
  docs/
    business-capabilities/
      CourseManagement/
        index.md
        business-rules.md
        test-conditions.md
        traceability.md
        diagrams/
      EnrollmentManagement/
        index.md
        business-rules.md
        test-conditions.md
        traceability.md
        diagrams/
      UserManagement/
        index.md
        business-rules.md
        test-conditions.md
        traceability.md
        diagrams/
    references/
      glossary.md
      source-repo-map.md
      capability-registry-sync.md
  templates/
    capability-rollup-template.md
    business-rules-template.md
    qa-test-conditions-template.md
    traceability-template.md
  validation/
    run-validation.ps1
    scripts/
      validate_business_docs.py
      validate_traceability.py

Recommendation:

- Start with Option A for speed and lower coordination overhead, while keeping one folder per capability from day one.
- Transition to Option B when capability count grows or review depth increases.

Per-capability file contract:

- `index.md`: Initial and primary output from `capability-consolidation`.
- `test-conditions.md`: QA-oriented acceptance, edge cases, and expected outcomes.
- `traceability.md`: Evidence map of business claims to sources. Minimum columns should include business statement, source repository, source document path, source section, and validation status.
- `diagrams/`: Capability-specific diagrams helpful to Product Owner and business-owner review.

## Integration With Core AKR Templates

Onboarding into core-akr-templates should include:

- A repository contract reference for training_tracker_business.
- A consolidation output template aligned to Product Owner and Technical Lead review needs.
- A skill invocation pattern that targets training_tracker_business as destination.
- A distributed repository skill file and validation script package.
- A readiness checklist that blocks consolidation writes until registry and governance gates are met.

## Step-By-Step Onboarding Checklist

1. Create training_tracker_business repository.
2. Apply branch protection, CODEOWNERS, labels, and issue templates.
3. Product Owner publishes canonical `businessCapability` values and cascades them to backend/UI documentation contributors.
4. Commit initial folder structure (Option A) including governance and architectural folders.
5. Publish capability rollup template.
6. Confirm Product Owner and Technical Lead review path.
7. Complete capability registry normalization for initial capability set.
8. Run first pilot consolidation for CourseManagement into `docs/business-capabilities/CourseManagement/index.md`.
9. Conduct PO and TL review on pilot output and supporting traceability/test conditions artifacts.
10. Refine template and workflow from pilot findings.
11. Roll out EnrollmentManagement and UserManagement consolidation.

## Definition Of Done For Onboarding

Onboarding is complete when all are true:

- Repository exists and governance controls are active.
- Folder structure and templates are in place.
- Product Owner and Technical Lead review workflow is active.
- At least one capability has completed pilot consolidation and review.
- Consolidation process is ready for repeatable capability-level execution.

## Risks and Mitigations

Risk: Repository created but no review ownership

- Mitigation: Enforce CODEOWNERS with Product Owner and Technical Lead reviewers from day one.

Risk: Consolidation starts before capability normalization

- Mitigation: Hard readiness gate requiring approved capability registry values.

Risk: Business documents become too technical for intended readers

- Mitigation: Use template language rules and PO-led readability review before approval.

## Immediate Next Action

Execute Phase 0 in this order:

1. Provision training_tracker_business repository.
2. Apply baseline governance controls.
3. Commit lean folder structure and starter templates.
4. Start pilot consolidation planning with Product Owner and Technical Lead.
