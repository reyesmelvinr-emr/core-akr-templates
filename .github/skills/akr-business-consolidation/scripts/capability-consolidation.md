# capability-consolidation

## Purpose

Generate or refresh baseline capability artifacts in a consolidation repository using markdown documentation evidence only.

## Allowed output set (write allowlist)

`capability-consolidation` may write only these files for `docs/business-capabilities/<CapabilityName>/`:

- `index.md`
- `test-conditions.md`
- `traceability.md`

## Protected files (must never be written by this mode)

- `backlog.md`
- `enhancements.md`
- `enhancement-test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`

If any planned write includes a protected file, stop with `BLOCKED_PROTECTED_FILE`.

## Source discovery policy

Only use markdown source artifacts that match capability metadata.

- Allowed: `.md` files under application repo `docs/` trees.
- Required match: front matter `businessCapability: <CapabilityName>` exact match.
- Prohibited: non-markdown files (`.cs`, `.ts`, `.tsx`, `.sql`, test files, scripts).

## Required source minimum

Before writing output, verify minimum sources:

- Backend markdown sources found: `>= 1`
- UI markdown sources found: `>= 1`
- Database markdown sources: optional

If minimum is not met, stop with `BLOCKED_MISSING_SOURCES` and do not write files.

When blocked, return:

- Missing source layer(s)
- Expected source pattern (markdown with matching `businessCapability`)
- Instruction: PO/TL should request developers in application repos to generate missing docs via repo-local documentation skills

## Template contract

Use canonical templates from `core-akr-templates/templates/`:

- `business_capability_template.md`
- `capability_testing_template.md`
- `traceability-template.md`

## Required checks

- Validate `businessCapability` against registry before write.
- Validate metadata fields and front matter shape.
- Validate source discovery uses only markdown files.
- Validate every source file has exact front matter capability match.
- Validate planned writes are allowlisted only.

## Execution sequence

1. Discover candidate markdown sources across backend/UI docs folders.
2. Filter to exact `businessCapability` match.
3. Validate required minimum source layers.
4. If validation fails: return `BLOCKED_MISSING_SOURCES` and exit with no writes.
5. If validation passes: synthesize and write only `index.md`, `test-conditions.md`, and `traceability.md`.
6. Emit `Source Manifest` and `Write Manifest` in response.

## Output quality

- Business-facing language only.
- Include explicit traceability to source evidence.
- Mark inferred statements with `🤖` and unknowns with `❓`.
- No code-level checking or fallback inference.
