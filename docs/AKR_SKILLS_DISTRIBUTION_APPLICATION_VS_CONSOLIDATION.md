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
- Resolving unknown markers and quality gaps before merge.
- Operating within the configured compliance mode.

## Consolidation Repository Distribution Model

Consolidation repositories focus on feature-level aggregation across application repositories.

## Distributed to Consolidation Repositories

- Consolidation configuration contracts and schema alignment references.
- Feature-level templates for consolidated business narratives and dependency views.
- Workflow scaffolds needed for cross-repo synthesis operations.

## Centrally Managed Dependencies

- Feature taxonomy and standards contracts.
- Validation and governance references that align with application-lane outputs.
- Core templates and instruction semantics used for normalized consolidation.

## Consolidation Repository Responsibilities

Consolidation owners are accountable for:

- Maintaining accurate feature-to-module mappings.
- Producing consolidated documentation that remains traceable to source module docs.
- Enforcing governance expectations for cross-repo outputs.
- Preserving business readability while retaining technical traceability.

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
- Consolidation lane: product and QA-oriented reviewers validate business coherence and evidence quality.
- In both lanes, unresolved unknowns are visible, assigned, and intentionally closed.

## Comparative View

## Application Repositories

- Primary purpose: code-proximate module and database documentation.
- Workflow emphasis: grouping, generation, unknown resolution, local validation.
- Control focus: implementation accuracy and standards adherence.

## Consolidation Repositories

- Primary purpose: cross-repo feature and capability narratives.
- Workflow emphasis: aggregation, traceability, business-context coherence.
- Control focus: governance consistency and portfolio-level maintainability.

## Why This Distribution Model Is Maintainable

The model scales because it avoids two common failures:

- Duplication of standards logic in every repository.
- Centralized control that ignores repository-level execution realities.

By distributing only what teams need to execute and keeping standards centralized, AKR maintains consistency while supporting practical team workflows.

## Conclusion

AKR distribution architecture is intentionally hybrid: centralized governance with distributed execution. This is a strong fit for organizations that need sustainable documentation workflows spanning application teams, business context, and cross-repository consolidation.
