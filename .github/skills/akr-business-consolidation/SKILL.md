---
name: akr-business-consolidation
description: >
	Consolidate backend and UI module documentation into business capability artifacts.
	Invoke explicitly via /akr-business-consolidation [capability-impact-analysis | capability-coverage-review | capability-consolidation | capability-promote | capability-test-maintenance | capability-test-generation | capability-relationship-mapping] [CapabilityName].
disable-model-invocation: true
compatibility:
	models:
		- claude-sonnet-4-6
		- gpt-5.4
metadata:
	skill-version: 1.0.1
	optimized-for: claude-sonnet-4-6
user-invocable: true
---
<!-- SKILL_VERSION: v1.0.1 -->
<!-- Managed by core-akr-templates. Do not edit directly in consolidation repositories. -->

CRITICAL: Begin EVERY response with this confirmation block.

✅ akr-business-consolidation INVOKED AND STEPS EXECUTED
Steps followed: 1. [step] - completed | 2. [step] - completed | ...

# AKR Business Consolidation Skill - Dispatcher

## Invocation Routing

Load only the mode script required by the command.

| Command | Mode Script | Primary Use |
|---|---|---|
| `/akr-business-consolidation capability-impact-analysis [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-impact-analysis.md` | Determine impacted capabilities from source changes |
| `/akr-business-consolidation capability-coverage-review [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-coverage-review.md` | Evaluate source coverage and metadata quality |
| `/akr-business-consolidation capability-consolidation [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-consolidation.md` | Generate or refresh the capability artifact set |
| `/akr-business-consolidation capability-promote [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-promote.md` | Promote delivered enhancements into baseline capability and QA artifacts |
| `/akr-business-consolidation capability-test-maintenance [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-test-maintenance.md` | Update baseline test conditions from current behavior |
| `/akr-business-consolidation capability-test-generation [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-test-generation.md` | Generate enhancement-focused tests |
| `/akr-business-consolidation capability-relationship-mapping [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-relationship-mapping.md` | Explain dependency and cross-layer relationships |

## Required Metadata and Governance

All generated capability files must include front matter with:

- `businessCapability` (approved value from registry)
- `feature` (format: `FN#####_US#####`)
- `layer` (for consolidation outputs use `Business` when applicable)
- `project_type` (for consolidation outputs use `business-consolidation`)
- `status` (`draft` or `approved`)
- `compliance_mode` (`pilot` or `production`)

Registry source of truth:

- `core-akr-templates/.akr/tags/tag-registry.json`

## Source Policy

For all consolidation-repo business capability workflows, source evidence must come from markdown documentation artifacts only.

- Allowed source files: `.md` files under application repo `docs/` trees.
- Required metadata match: front matter `businessCapability: <CapabilityName>` exact match.
- Prohibited source files: any non-markdown files including `.cs`, `.ts`, `.tsx`, `.sql`, `.ps1`, and test files.

If required markdown sources are missing, stop with `BLOCKED_MISSING_SOURCES` and do not infer from code.

## Output Contract

Primary output location in consolidation repositories:

- `docs/business-capabilities/<CapabilityName>/index.md`
- `docs/business-capabilities/<CapabilityName>/test-conditions.md`
- `docs/business-capabilities/<CapabilityName>/traceability.md`

### capability-consolidation mode write allowlist

`/akr-business-consolidation capability-consolidation [CapabilityName]` may update only:

- `docs/business-capabilities/<CapabilityName>/index.md`
- `docs/business-capabilities/<CapabilityName>/test-conditions.md`
- `docs/business-capabilities/<CapabilityName>/traceability.md`

### Protected files for capability-consolidation mode

`capability-consolidation` must never write:

- `docs/business-capabilities/<CapabilityName>/backlog.md`
- `docs/business-capabilities/<CapabilityName>/enhancements.md`
- `docs/business-capabilities/<CapabilityName>/enhancement-test-conditions.md`
- `docs/business-capabilities/<CapabilityName>/limitations.md`
- `docs/business-capabilities/<CapabilityName>/internal_dependencies.md`
- `docs/business-capabilities/<CapabilityName>/external_dependencies.md`

## Determinism Rules

- Never invent capability names not present in registry.
- Preserve repository-owned `.github/copilot-instructions.md` files.
- Keep outputs business-facing for PO/QA/TL audiences.
- Mark unknowns with `❓` and inferred statements with `🤖`.
- Never perform code-level verification in consolidation mode.
- Emit a `Source Manifest` listing every markdown source used.
- Emit a `Write Manifest` listing every file updated.
- If a write target is outside the allowlist, stop with `BLOCKED_PROTECTED_FILE`.
