# Changelog

## 2026-03-18 - Phase 1 Deliverables 4-7A

### Added

- Rewrote canonical Copilot guidance at `.akr/standards/copilot-instructions.md` to module-centric mode guidance.
- Added governance/HITL documentation:
  - `docs/DEVELOPER_REFERENCE.md`
  - `docs/VALIDATION_GUIDE.md`
  - `docs/TAG_REGISTRY_GUIDE.md`
- Added workflow step in `.akr/workflows/validate-documentation.yml` to verify SKILL template references resolve to known templates.

### Updated

- `.akr/schemas/modules-schema.json`:
  - Added optional `ssg_pass3_source_reread` and `ssg_pass4_source_reread` fields.
  - Added `compliance_mode` enum for module entries.
  - Added `review` to module status enum.
- `.akr/schemas/akr-config-schema.json`:
  - Updated default required tags to include `businessCapability` and `project_type`.
  - Added `humanInput.script_approval_required`.
  - Added monitoring metrics enums: `ssg-pass-timings`, `ssg-slow-module-events`.
- `.github/hooks/agentStop.json` to pass explicit changed-files list to validator.
- `.github/skills/akr-docs/SKILL-COMPAT.md` with explicit hook-unavailable fallback command.
- `.gitignore` to exclude `.akr/logs` session artifacts.
- `.akr/templates/lean_baseline_service_template.md` and `.akr/templates/ui_component_template.md` front matter examples aligned to PascalCase `businessCapability`.
- `examples/modules.trainingtracker.api.yaml` includes both SSG override flags with caution comments.

### Governance Decision

- `TEMPLATE_MANIFEST.json` remains the source for template version mapping.
- Template selection logic is governed by skill mode + project_type mapping, not by legacy complexity routing.

## 2026-03-31 - Skill Command Rename (Phase 0)

### Breaking Change

- AKR agent skill mode labels renamed from Mode A / Mode B / Mode C to verb-first functional names.
  Consumers of the `/akr-docs` slash command must update invocations immediately.

| Old command | New command | Purpose |
|---|---|---|
| `/akr-docs mode-a [target]` | `/akr-docs groupings [target]` | Propose module groupings |
| `/akr-docs mode-b [target]` | `/akr-docs generate [target]` | Generate module documentation |
| `/akr-docs mode-c [target]` | `/akr-docs resolve [target]` | Resolve unresolved markers |

### Updated

- `.github/skills/akr-docs/SKILL.md`: section headers, step references, and invocation description updated to ProposeGroupings / GenerateDocumentation / ResolveUnknowns.
- `.github/skills/akr-docs/SKILL-COMPAT.md`: model matrix, invocation surface matrix, HITL role mapping, and governance stability seed updated. `Last updated` bumped to 2026-03-31. Eval re-run deferral note added.
- `.akr/scripts/validate_documentation.py`: user-visible error/warning messages and preview header updated to new names.
- `.akr/scripts/tests/test_validate_documentation.py`: subprocess test assertions updated to match.
- `.akr/standards/copilot-instructions.md`: invocation patterns and Three-Mode Skill Guidance section headers updated.
- `copilot-instructions/backend-service.instructions.md`, `ui-component.instructions.md`, `database.instructions.md`: Audience headers updated to GenerateDocumentation.
- `evals/cases/mode-a-standard.yaml` → renamed to `groupings-standard.yaml`; `mode-b-coursedomain.yaml` → `generate-coursedomain.yaml`; `mode-b-large-module.yaml` → `generate-large-module.yaml`. Internal `id`, `command`, and `description` fields updated.
- `evals/cases/ssg-pass-sequence.yaml`: command field updated to `/akr-docs generate CourseDomain`.
- `evals/benchmark.json`: all fixture keys, SSG sub-keys, and quality metric `avg-mode-c-resolution-minutes` renamed. `last-updated` bumped to 2026-03-31.
- `README.md`: Key Architecture section, repository tree, docs link text, and support commands updated.
- `metadata header` contract: `mode: B` → `mode: generation`.

### Excluded (intentionally immutable)

- Historical planning docs and prior decision records in `akr-mcp-server/docs/` remain unchanged as immutable records.
