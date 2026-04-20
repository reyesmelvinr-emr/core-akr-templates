---
name: akr-business-consolidation
description: >
  Consolidate backend and UI module documentation into business capability artifacts.
  Invoke explicitly via /akr-business-consolidation [capability-impact-analysis | capability-coverage-review | capability-consolidation | capability-promote | capability-promote-new | capability-test-maintenance | capability-relationship-mapping] [CapabilityName].
disable-model-invocation: true
compatibility:
  models:
    - claude-sonnet-4-6
    - gpt-5.4
metadata:
  skill-version: 1.0.0
  optimized-for: claude-sonnet-4-6
user-invocable: true
---
<!-- SKILL_VERSION: v1.0.0 -->
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
| `/akr-business-consolidation capability-promote-new [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-promote-new.md` | Promote a new capability to active status after PO/TL acceptance |
| `/akr-business-consolidation capability-test-maintenance [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-test-maintenance.md` | Update baseline test conditions from current behavior |
| `/akr-business-consolidation capability-relationship-mapping [CapabilityName]` | `.github/skills/akr-business-consolidation/scripts/capability-relationship-mapping.md` | Explain dependency and cross-layer relationships |

Dispatcher pre-check for `capability-promote-new`:
- Determine capability status from `docs/business-capabilities/{active|new|archived}/<CapabilityName>/`.
- If status is not `new`, stop before loading the mode script and return:
  "capability-promote-new is only available for new capabilities. <CapabilityName> is currently <status>."

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

Mode scripts must reference this section as the authoritative metadata contract and avoid restating duplicate check blocks.

## Output Contract

Primary output location in consolidation repositories (status-aware paths):

**Active capabilities:**
- `docs/business-capabilities/active/<CapabilityName>/index.md`
- `docs/business-capabilities/active/<CapabilityName>/test-conditions.md`
- `docs/business-capabilities/active/<CapabilityName>/enhancement-test-conditions.md`
- `docs/business-capabilities/active/<CapabilityName>/enhancements.md`
- `docs/business-capabilities/active/<CapabilityName>/backlog.md`
- `docs/business-capabilities/active/<CapabilityName>/limitations.md`
- `docs/business-capabilities/active/<CapabilityName>/internal_dependencies.md`
- `docs/business-capabilities/active/<CapabilityName>/external_dependencies.md`
- `docs/business-capabilities/active/<CapabilityName>/traceability.md`

**New capabilities:**
- `docs/business-capabilities/new/<CapabilityName>/index.md`
- `docs/business-capabilities/new/<CapabilityName>/test-conditions.md`
- `docs/business-capabilities/new/<CapabilityName>/limitations.md`
- `docs/business-capabilities/new/<CapabilityName>/internal_dependencies.md`
- `docs/business-capabilities/new/<CapabilityName>/external_dependencies.md`
(excludes enhancements, enhancement-test-conditions, backlog, traceability)

**Archived capabilities:**
- `docs/business-capabilities/archived/<CapabilityName>/index.md`
- `docs/business-capabilities/archived/<CapabilityName>/limitations.md`
- `docs/business-capabilities/archived/<CapabilityName>/internal_dependencies.md`
- `docs/business-capabilities/archived/<CapabilityName>/external_dependencies.md`
- `docs/business-capabilities/archived/<CapabilityName>/traceability.md`
(read-mostly historical; excludes test/enhancement artifacts)

## Determinism Rules

- Never invent capability names not present in registry.
- Preserve repository-owned `.github/copilot-instructions.md` files.
- Keep outputs business-facing for PO/QA/TL audiences.
- Mark unknowns with `❓` and inferred statements with `🤖`.

## Consolidation Mode

The skill reads source documentation from different locations depending on the `consolidation.mode` setting in `.akr-config.json`.

| Mode | Description | Who uses it |
|---|---|---|
| `local-workspace` | Source docs read directly from workspace folders. Source repositories must be open in the active VS Code multi-root workspace. | Technical PO/TL with local clones of source repos |
| `source-evidence` | Source docs read from `docs/references/source-evidence/<repo-name>/` inside the consolidation repository. Snapshot is refreshed via `sync-source-evidence.yml` workflow. | Non-technical PO with consolidation repo access only |

If `consolidation.mode` is absent, default to `source-evidence`.

Mode scripts must reference this section as the authoritative source-access contract and avoid duplicating this table.

## Source Evidence Schema (sync-manifest.json)

In `source-evidence` mode, each evidence folder may include `sync-manifest.json` with this schema:

```json
{
  "source_repo": "owner/repo",
  "branch": "branch-name",
  "commit_sha": "commit-sha-or-placeholder",
  "synced_at": "ISO-8601 timestamp",
  "triggering_pr": "pr-number-or-manual-dispatch-id",
  "files_synced": ["glob/or/path", "..."]
}
```

Field usage:
- `commit_sha`: source revision identifier for traceability output.
- `synced_at`: evidence freshness indicator.
- `triggering_pr`: upstream trigger reference for auditability.

Refer to [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](../../docs/TEAM_STARTUP_ONBOARDING_GUIDE.md) for setup instructions for each mode.
