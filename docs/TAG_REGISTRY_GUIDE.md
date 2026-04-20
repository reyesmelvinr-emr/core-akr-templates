# Tag Registry Guide

## Version

This guide describes `tag-registry.json` schema **v1.3.0**.

## File Purpose

`tag-registry.json` is a **distribution template** used during application onboarding.

- Core reusable tags live in `registry.features`.
- Each onboarding application must populate `registry.businessCapabilities` with its own approved values.
- `examples.businessCapabilities` is reference-only and must not be treated as active registry data.

## v1.3.0 Top-Level Structure

`tag-registry.json` contains these top-level sections:

- `version`
- `lastUpdated`
- `template`
- `registry`
- `examples`
- `governance`
- `changelog`

## Template Section

`template` provides metadata for distributed onboarding usage:

- `name`
- `distributionTarget`
- `purpose`
- `usage` (array of onboarding rules)

## Registry Section

`registry` is the authoritative section used by validation and consolidation.

### registry.features (core reusable tags)

Each new `registry.features.<FeatureName>` entry must include:

- `approved` (boolean)
- `domain` (string; must exist in `registry.domains`)
- `description` (string)
- `owner` (string)
- `status` (`active` or `deprecated`)

Optional fields:

- `synonyms` (string array)
- `relatedFeatures` (string array)
- `addedDate` (ISO date string)

### registry.businessCapabilities (application-specific tags)

This object is intentionally empty in distributed template form.

- During onboarding, application teams add canonical entries here.
- Consolidation accepts only approved values from this section.
- Do not place live capabilities in `examples.businessCapabilities`.

Each new `registry.businessCapabilities.<CapabilityName>` entry should include:

- `approved` (boolean)
- `description` (string)
- `owner` (string)
- `status` (`draft`, `review`, `approved`, or `deprecated`)

For capability workflow execution, maintain an operational lifecycle status for each capability (`new`, `active`, `archived`) in the workflow-facing capability metadata used by consolidation and enhance skills.
The operational lifecycle status determines which skill families can run:

- `new` -> capability-define workflow and capability-promote-new.
- `active` -> enhancement workflow and capability-promote.
- `archived` -> read-mostly mode; no enhancement intake.

Optional field:

- `addedDate` (ISO date string)

### registry enums

The template also defines reusable enums:

- `registry.domains`
- `registry.layers`
- `registry.statuses`
- `registry.componentTypes`

## Examples Section

`examples.businessCapabilities` holds sample onboarding data only.

- Keep examples clearly non-authoritative.
- Teams may copy/edit examples into `registry.businessCapabilities` via PR.

## Governance Section

`governance` defines approval and naming controls:

- `approvers`
- `namingConvention.featureKeys`
- `namingConvention.businessCapabilityKeys`
- `approvalProcess.requiredApprovals`
- `approvalProcess.changeMethod`
- `approvalProcess.rules`
- `changelogRequired`

## Naming Rule

Feature and business capability keys must be PascalCase and match:

- `^[A-Z][a-zA-Z0-9]*$`

Example valid keys:

- `CourseCatalogManagement`
- `EnrollmentManagement`

Example invalid keys:

- `course-catalog-management`
- `course_catalog_management`

## Onboarding Workflow (v1.3.0)

1. Team copies distributed template.
2. Team adds application-specific entries to `registry.businessCapabilities`.
3. Team submits PR for approvals required by `governance.approvalProcess.requiredApprovals`.
4. After approval, source documentation must use only approved capability keys.
5. Consolidation validation gates on approved `registry.businessCapabilities` values.

For teams using the new-capability workflow, also ensure each newly approved capability is initialized with operational lifecycle status `new` before PO/TL begin authoring capability artifacts.

## Governance Notes

- Layer governance in tag registry excludes `Full-Stack` by design.
- Module taxonomy in `modules-schema.json` may include `Full-Stack` for grouping, but this does not change tag registry layer constraints.
