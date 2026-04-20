# AKR Copilot Instructions (Module-Centric)

Version: 1.1.0
Last Updated: 2026-03-18
Scope: Module-centric AKR documentation generation for Copilot and agent workflows.

## Purpose

This document is the canonical guidance for creating and updating AKR documentation using module-aware workflows.

This is a full replacement of legacy MCP-server-centric guidance. Do not use legacy `/docs.*` commands from older instructions.

## Core Principles

1. Transparency markers are mandatory.
- Use `??` for AI-inferred content.
- Use `?` for required unresolved human inputs.
- Use `??` for confirmed human-authored content.

2. Completeness scoring remains unchanged.

```
Completeness = (Completed Sections / Total Sections) * 100
- ?? sections count as complete.
- ? unresolved required sections count as incomplete.
- ?? sections count as complete.
```

3. Surgical updates only.
- Preserve existing `??` content.
- Update only impacted `??` sections.
- Keep unresolved `?` sections visible until resolved or explicitly deferred.

4. Use centralized Vale policy.
- Validate against `.akr/.vale.ini` when running local checks.

## Required Invocation Pattern

Always invoke this skill explicitly:

- `/akr-docs groupings`
- `/akr-docs generate`
- `/akr-docs resolve`

Never rely on implicit skill auto-discovery for production-bound output.

At the start of each response, skill runs must include this confirmation block:

```
? akr-docs INVOKED AND STEPS EXECUTED
Steps followed: 1. [step] - completed | 2. [step] - completed | ...
```

If the block is absent:

1. Run `/skills` and confirm `akr-docs` is enabled.
2. Retry with explicit slash command invocation.
3. If still absent, treat output as untrusted and run CI validation before merge.

Model compatibility note:
- Optimized for `claude-sonnet-4-6`.
- `gpt-4o` can produce lower first-run pass rates on large modules.
- CI validation is the final enforcement gate for all models.
- See `.github/skills/akr-docs/SKILL-COMPAT.md` for full compatibility details.

## Module Grouping Principles

Apply all four principles during grouping and documentation generation:

1. Domain noun identity
- Group files that operate on the same business noun (for example, Course, Enrollment).

2. Dependency graph continuity
- Follow vertical flow: controller -> service interface/implementation -> repository interface/implementation -> persistence.

3. DTO and contract alignment
- Keep request/response DTOs and contracts with the owning module.

4. Interface/implementation pairing
- Keep interfaces with their concrete implementations in the same module unless they are explicitly shared.

## Three-Mode Skill Guidance

### ProposeGroupings (Grouping proposal)
Use when:
- `modules.yaml` is missing.
- Existing groupings are draft or outdated.
- Repository structure changed significantly.

Output:
- Draft `modules.yaml` groupings.
- Unassigned file list with reasons.
- Human review checklist.

### GenerateDocumentation (Documentation generation)
Use when:
- `modules.yaml` entries are approved.
- You need generated module documentation.

Output:
- Module documentation from approved template.
- Required metadata header in generated document.
- Validation execution and pass/fail summary.

### ResolveUnknowns (Interactive HITL completion)
Use when:
- A generated draft contains unresolved `?` markers.
- Human context or decisions are needed before production mode.

Output:
- Resolved sections from targeted Q&A.
- Deferred items with owner and rationale where applicable.
- Re-validation summary after updates.

## Template Selection Table

| project_type | Template | Notes |
|---|---|---|
| api-backend | .akr/templates/lean_baseline_service_template_module.md | Controller + service + repository + DTO scope |
| ui-component | .akr/templates/ui_component_template_module.md | Page + components + hooks + types |
| microservice | .akr/templates/lean_baseline_service_template_module.md | Service-to-service boundaries |
| general | .akr/templates/lean_baseline_service_template.md | Fallback for non-module legacy docs |
| table | .akr/templates/table_doc_template.md | Database object docs |
| view | .akr/templates/table_doc_template.md | Database object docs |
| procedure | .akr/templates/embedded_database_template.md | Database object docs |

## project_type -> Condensed Charter Mapping

| project_type | Condensed Charter |
|---|---|
| api-backend | copilot-instructions/backend-service.instructions.md |
| microservice | copilot-instructions/backend-service.instructions.md |
| ui-component | copilot-instructions/ui-component.instructions.md |
| general | copilot-instructions/backend-service.instructions.md |
| table | copilot-instructions/database.instructions.md |
| view | copilot-instructions/database.instructions.md |
| procedure | copilot-instructions/database.instructions.md |

## modules.yaml Front Matter Contract Reference

For module documentation (`doc_type=module`) front matter must include:

- `businessCapability`: PascalCase (for example, `CourseCatalogManagement`)
- `feature`: Work-item format `FNxxxxx_USxxx`
- `layer`: UI/API/Database/Integration/Infrastructure
- `project_type`: `api-backend` | `ui-component` | `microservice` | `general`
- `status`: `draft` | `review` | `approved` | `deprecated`
- `compliance_mode`: `pilot` | `production`

For database objects, require object-appropriate tags and keep `businessCapability` PascalCase when present.

## HITL and Validation Expectations

- In `pilot`, unresolved `?` markers are allowed but must be visible.
- In `production`, unresolved required `?` markers are blocking.
- Use ResolveUnknowns to resolve marker debt before graduating compliance mode.

## Operational Checklist

Before merge:

1. Module grouping reviewed (if ProposeGroupings changed module boundaries).
2. Generated docs contain metadata header and required sections.
3. `businessCapability` values are PascalCase.
4. Validator passes at intended compliance mode.
5. CI checks and annotations are clean.

## Explicitly Removed Legacy Guidance

The following legacy behaviors are deprecated and out of scope:

- Legacy `/docs.generate`, `/docs.interview`, and `/docs.update*` command set.
- Legacy MCP health-check/server bootstrapping instructions.
- Legacy tree-sitter-only assumptions as a hard requirement.
- Legacy path references to removed setup and troubleshooting scripts.

Use AKR skill modes and the current validator workflows instead.

---

# Coding Agent Guidelines
Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
