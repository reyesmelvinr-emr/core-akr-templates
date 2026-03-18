# Tag Registry Guide

## Feature Entry Requirements

Each new `registry.features.<FeatureName>` entry in `tag-registry.json` must include:

- `approved` (boolean)
- `domain` (string)
- `description` (string)
- `owner` (string)
- `status` (`active` or `deprecated`)

Optional fields:

- `synonyms`
- `relatedFeatures`
- `addedDate`

## Naming Rule

Feature keys must match PascalCase regex:

- `^[A-Z][a-zA-Z0-9]*$`

Example valid keys:

- `CourseCatalogManagement`
- `EnrollmentManagement`

Example invalid keys:

- `course-catalog-management`
- `course_catalog_management`

## Governance Notes

- Layer governance in tag registry excludes `Full-Stack` by design.
- Module taxonomy in `modules-schema.json` may include `Full-Stack` for grouping, but this does not change tag registry layer constraints.
