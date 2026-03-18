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
