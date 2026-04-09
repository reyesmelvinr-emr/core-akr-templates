# capability-consolidation

## Purpose

Generate or refresh the complete capability artifact set in a consolidation repository.

## Required output set

Write all files for `docs/business-capabilities/<CapabilityName>/`:

- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`
- `enhancements.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

## Template contract

Use canonical templates from `core-akr-templates/templates/`:

- `business_capability_template.md`
- `capability_testing_template.md`
- `capability_enhancement_testing_template.md`
- `capability_enhancements_template.md`
- `capability_limitations_template.md`
- `capability_internal_dependencies_template.md`
- `capability_external_dependencies_template.md`
- `traceability-template.md`

## Required checks

- Validate `businessCapability` against registry before write.
- Validate metadata fields and front matter shape.
- Preserve existing repository-owned policy files.

## Output quality

- Business-facing language only.
- Include explicit traceability to source evidence.
- Mark inferred statements with `🤖` and unknowns with `❓`.
