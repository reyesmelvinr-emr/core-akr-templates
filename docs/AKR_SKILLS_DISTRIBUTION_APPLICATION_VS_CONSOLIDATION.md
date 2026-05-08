# AKR Skills Distribution: Application Repositories vs Consolidation Repositories

## Executive Summary

AKR uses a controlled distribution model so teams can execute documentation workflows locally while preserving centralized governance. This model separates what must be copied into consuming repositories from what should remain centrally managed and runtime-fetched.

The result is a maintainable operating pattern with reduced standards drift and clear ownership.

## Distribution Design Principles

- Keep standards authoritative in one source.
- Distribute only execution-critical assets to consuming repositories.
- Preserve repository-specific ownership for local operating context.
- Enforce governance and compliance in both application and consolidation lanes.

## Application Repository Distribution Model

Application repositories receive the assets needed to run module-level documentation workflows close to the code.

## Distributed to Application Repositories

- Skill dispatcher and supporting scripts for workflow execution.
- The application bundle currently includes `akr-docs`, `akr-interview`, and the developer-facing `akr-capability` modes (`enhancement-clarify`, `capability-define-clarify`, and `code-review`) only.
- Skill compatibility guidance and hook integrations.
- Onboarding seed artifacts such as project config and module manifest seeds.
- Validation workflow definitions used in repository CI.

## Runtime-Fetched or Centrally Managed

- Canonical validation logic and rule sets.
- Core template and charter guidance that must remain synchronized.
- Central standards references and governance updates.

This split reduces local maintenance burden while keeping enforcement behavior consistent.

## Application Repository Responsibilities

Application teams are accountable for:

- Maintaining module manifests and local documentation outputs.
- Running the skill workflows with required approvals.
- Running `enhancement-clarify` before coding when a closed enhancement is handed off from the consolidation repository.
- Running `code-review` after implementation delivery to assess alignment with the mini-spec and `enhancements.md` before PO/TL closeout.
- Resolving unknown markers and quality gaps before merge.
- Operating within the configured compliance mode.

## Consolidation Repository Distribution Model

Consolidation repositories focus on business capability aggregation across application repositories.

## Distributed to Consolidation Repositories

- Consolidation workflow package for capability lifecycle management.
- The consolidation bundle includes `akr-business-consolidation` plus the PO/TL-facing `akr-capability` modes (`enhancement-review`, `enhancement-review-close`, `enhancement-test-generation`, `capability-define-review`, and `capability-define-close`).
- Standardized operating patterns for impact assessment, readiness review, consolidation, baseline promotion, enhancement assessment, and test governance.
- Capability-level content structures for business narratives, dependencies, and traceability.
- Orchestration assets needed for cross-repository synthesis operations.

## Centrally Managed Dependencies

- Business capability taxonomy and standards contracts.
- Validation and governance references that align with application-lane outputs.
- Canonical content and instruction semantics used for normalized consolidation.

## Consolidation Repository Responsibilities

Consolidation owners are accountable for:

- Maintaining accurate capability-to-module mappings.
- Producing consolidated documentation that remains traceable to source module docs.
- Enforcing governance expectations for cross-repo outputs.
- Preserving business readability while retaining technical traceability.
- Running enhancement assessment and closeout workflows before handing coding work to developers.
- Running promotion and maintenance cycles when enhancement items are delivered so baseline capability views stay current.

## Implemented Consolidation Promotion Flow

The implemented promotion capability provides a controlled path for elevating delivered enhancements into baseline capability documentation.

- Identifies enhancement entries that include delivery-tracking references.
- Uses human confirmation to determine which referenced delivery items are closed or complete.
- Requests explicit PO/TL acceptance and asks whether testing is complete for each accepted item.
- Updates baseline capability narratives with delivered behavior and rule changes.
- Updates baseline limitations and internal/external dependency artifacts when delivered enhancements changed those baselines.
- Merges enhancement-driven test coverage into baseline quality conditions only when testing completion is confirmed; otherwise it records deferred test-promotion follow-up notes.
- Synchronizes enhancement status so planning and baseline views remain aligned.

Current verification scope:

- Delivery-state verification is human-in-the-loop.
- Testing completion confirmation is human-in-the-loop and is not inferred from artifacts in the current proof-of-concept.
- Automated delivery-system verification is documented as a future extension path.

Template impact:

- Enhancement backlog structures include a delivery-reference field to support promotion readiness.

## Governance, Compliance, and Human-in-the-Loop Across Both Lanes

## Governance Controls in Distribution

- Central governance defines contracts, formats, and acceptance criteria.
- Distributed workflows implement those contracts in repo-local execution.
- Ownership boundaries prevent ambiguity over who approves what.

## Compliance Controls in Distribution

- Compliance mode settings determine strictness in validation outcomes.
- Production settings require stronger resolution discipline before merge.
- Exception handling follows documented approval and remediation paths.

## Human-in-the-Loop Controls in Distribution

- Application lane: technical leads and developers validate module intent and implementation fidelity.
- Consolidation lane: product and QA-oriented reviewers validate business coherence and evidence quality, including delivery-state, PO/TL acceptance, and testing-completion confirmation for promotion.
- In both lanes, unresolved unknowns are visible, assigned, and intentionally closed.

## Comparative View

## Application Repositories

- Primary purpose: code-proximate module and database documentation.
- Workflow emphasis: grouping, generation, unknown resolution, local validation, pre-coding enhancement clarification, and post-coding implementation review.
- Control focus: implementation accuracy and standards adherence.

## Consolidation Repositories

- Primary purpose: cross-repo business capability narratives.
- Workflow emphasis: impact assessment, enhancement review/close/test generation, consolidation, promotion, quality maintenance, and relationship mapping.
- Control focus: governance consistency and portfolio-level maintainability.

## Why This Distribution Model Is Maintainable

The model scales because it avoids two common failures:

- Duplication of standards logic in every repository.
- Centralized control that ignores repository-level execution realities.

By distributing only what teams need to execute and keeping standards centralized, AKR maintains consistency while supporting practical team workflows.

## Conclusion

AKR distribution architecture is intentionally hybrid: centralized governance with distributed execution. This is a strong fit for organizations that need sustainable documentation workflows spanning application teams, business context, and cross-repository consolidation.
