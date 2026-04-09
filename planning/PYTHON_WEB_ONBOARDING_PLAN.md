# Plan to Onboard Python Web Applications into AKR (Monorepo and Multi-Repo)

## Document Purpose
This draft defines how core-akr-templates can onboard Python web applications — whether they live in a single monorepo or are split across multiple repositories — while preserving current .NET onboarding behavior. It is written as an implementation-ready plan for template maintainers and pilot teams.

## Scope
### In Scope
- Python web applications (Django, FastAPI, Flask style architectures).
- Monorepo layouts: all application layers in one repository.
- Multi-repo layouts: separate repositories per layer (API backend, UI frontend, database).
- Module grouping, generated documentation, validation, and onboarding examples.
- Additive updates only (no breaking changes to current .NET usage).

### Out of Scope for Initial Rollout
- Immediate production implementation of deterministic Python AST extraction logic.
- Replacing existing .NET examples or workflows.
- Broad non-web Python scenarios (data science, ETL-only repos).

## Background and Problem Statement
core-akr-templates has primarily been exercised using .NET web service codebases. Existing examples and some guidance assume C# file roles and .NET project structure. Python web projects — in both monorepo and multi-repo configurations — commonly organize logic around route/view handlers, service helpers, form/schema validation, and external API orchestration.

Without targeted updates, Python onboarding can still happen, but documentation quality and consistency degrade due to role-name mismatch and overly .NET-specific examples. Multi-repo Python applications face an additional gap: no Python-flavored example of the cross-repository linking config exists, even though AKR already supports cross-repo linking in a language-agnostic way.

## Monorepo vs Multi-Repo: Key Differences for Python Web Apps
Understanding both layouts is important before reading the implementation plan.

### Monorepo
All layers of the application live in a single repository. One `modules.yaml` covers the full project. AKR is onboarded once for the entire codebase.

Typical structure:
```
my-python-app/
  app/          <- Django app: views, helpers, forms, models
  CusVis/       <- Django project: settings, URLs, WSGI
  templates/    <- HTML templates
  static/       <- CSS, JS, images
  manage.py
```

### Multi-Repo
Each layer lives in its own repository, exactly like a .NET multi-repo split. AKR is onboarded separately on each repository, and repos reference each other via the `crossRepository` config.

Typical split:

| Repository | Layer | Technology |
|---|---|---|
| my-python-api | API | Django REST Framework, FastAPI, or Flask |
| my-web-ui | UI | React, Vue, or Angular (still JavaScript/TypeScript) |
| my-db-migrations | Database | Alembic or Django migration scripts + SQL |

**Key insight:** The UI repository of a multi-repo Python application is almost always still JavaScript/TypeScript (React/Vue/Angular). Python replaces the .NET backend only. AKR's existing `crossRepository` linking config is already language-agnostic at the `layer: UI / API / Database` level, so the multi-repo linking mechanism needs no structural change — only a Python-flavored backend config example.

The only genuinely Python-UI scenario is when the backend also serves Django-rendered HTML templates (the monorepo or a dedicated template-rendering app). That case maps to `layer: UI` with `project_type: ui-component` and Python path mappings.

## Current-State Findings (Summary)
### Observed AKR Assumptions that Need Generalization
1. Multiple onboarding examples use C# source paths and .NET naming.
2. Backend role guidance uses Controller/Service/Repository/DTO terminology as the default mental model.
3. Existing workshop and sample module docs emphasize .NET layering as the canonical example.
4. Some monorepo path mapping examples are C#-centric.

### Python Web Patterns to Support
Based on sample Django repository analysis, Python web modules commonly center on:
1. URL routes and view handlers as entry points.
2. Service/helper orchestration for business behavior.
3. Form/schema classes for validation and sanitization.
4. External API clients and integration calls.
5. Settings and middleware-based security/configuration.
6. Server-rendered templates and static assets (for Django-style web apps).

## Target Outcome
Enable Python web applications — monorepo or multi-repo — to complete AKR onboarding with:
1. Clear grouping guidance for both layout styles.
2. Accurate module role labels that reflect Python frameworks.
3. Complete operations maps and data operations sections.
4. No forced .NET naming in generated markdown.
5. CI validation and lint behavior equivalent to .NET onboarding.
6. Correct cross-repository linking config for multi-repo Python applications.

## Guiding Principles
1. Backward compatibility first.
2. Additive migration path.
3. Language-agnostic architecture wording where possible.
4. Keep project_type stable initially (prefer api-backend with role mapping guidance).
5. Separate immediate onboarding support from future extractor enhancements.
6. Multi-repo support is a superset of monorepo support: all monorepo changes apply directly to the backend repo of a multi-repo, with one additional config example for cross-repo linking.

## Implementation Plan

## Phase 1: MVP Onboarding Compatibility
Goal: Unblock Python web monorepo onboarding now with no breaking changes.

### 1. Update onboarding and quick-start documentation
#### Files
- README.md

#### Changes
1. Add Python web examples beside existing .NET snippets.
2. Show an alternative modules.yaml sample with Python paths.
3. Expand technology/tag examples so they are not .NET-only.

#### Result
Pilot teams can follow onboarding steps without translating .NET-only examples manually.

### 2. Add Python-compatible AKR config examples (monorepo)
#### Files
- examples/.akr-config-api.json
- .akr/examples/akr-config-monorepo.json

#### Changes
1. Add Python include patterns and Python package path mappings.
2. Keep existing C# mappings; do not remove them.
3. Demonstrate a monorepo API package pattern for Python.

#### Result
Teams can seed AKR config quickly for Python monorepo package layouts.

### 2b. Add Python multi-repo cross-repository config example
#### Files
- New file: examples/.akr-config-python-api.json

#### Changes
1. Create a Python-flavored version of `.akr-config-api.json` that shows the API backend repo pointing to a separate `web-ui` repo via the `crossRepository` block.
2. Use Python paths and include patterns throughout (no C# paths).
3. The `crossRepository.relatedRepositories` block is identical in structure to the existing .NET example; only the `layer: API` repo description and include patterns change.

#### Result
Multi-repo Python teams have a direct reference config showing how to link their API backend to a separate UI and/or database repo.

### 3. Add Python module manifest examples
#### Files
- examples/modules.trainingtracker.api.yaml (retain as .NET reference)
- New file: examples/modules.python-web-monorepo.yaml
- New file: examples/modules.python-web-api.yaml

#### Changes
1. `modules.python-web-monorepo.yaml`: covers all layers in one manifest (views, helpers, forms, templates, settings).
2. `modules.python-web-api.yaml`: covers only the API backend layer, matching the multi-repo case where the UI and database are in separate repos.
3. Both use realistic Python roles: View Handler, Service/Helper, Validation Form, Integration Client.
4. Monorepo example includes UI template modules and an `unassigned` block for shared utilities.
5. Multi-repo API example omits UI templates; references the related UI repo via project metadata notes.

#### Result
ProposeGroupings and GenerateDocumentation have canonical Python examples for both layout styles.

### 4. Generalize backend role guidance
#### Files
- copilot-instructions/backend-service.instructions.md

#### Changes
1. Keep current Module Files coverage requirement.
2. Add explicit role mapping guidance table:
   - Controller -> Route/View Handler
   - Service -> Service/Helper
   - Repository -> DAO/Repository/Integration Adapter
   - DTO -> Schema/Form/Serializer
3. Clarify that role names should reflect framework reality, not forced naming.

#### Result
Generated docs become accurate for Python architectures while preserving standard section structure.

### 5. Expand terminology acceptance for linting
#### Files
- validation/vale-rules/AKR/accept.txt

#### Changes
1. Add Python framework and architecture vocabulary (for example Django, FastAPI, Flask, Pydantic, SQLAlchemy, Form, Schema, Handler).

#### Result
Vale false positives drop for Python-generated docs.

## Phase 2: Schema and Workflow Alignment
Goal: Make metadata and CI examples explicitly monorepo/Python-aware while remaining backward compatible.

### 6. Add optional metadata hints in schema
#### Files
- .akr/schemas/modules-schema.json
- .akr/schemas/akr-config-schema.json

#### Changes
1. Add optional fields (non-required) for language/framework/runtime profile.
2. Keep all existing required fields and enums unchanged where not necessary.
3. Update schema examples/defaults to reflect mixed-language or Python package paths.

#### Result
Tools and teams can carry explicit context for language/framework without breaking existing manifests.

### 7. Validate workflow path coverage for Python monorepos
#### Files
- examples/workflows/validate-documentation.yml

#### Changes
1. Confirm changed-file pattern coverage for Python source and docs paths.
2. Ensure no assumptions around .cs-only API folders in examples.

#### Result
CI sample workflow remains reliable for Python and .NET repos.

### 8. Improve onboarding seed defaults
#### Files
- examples/onboarding/modules.yaml.seed

#### Changes
1. Add optional commented hints for language/framework and package layout usage.
2. Keep seed minimal and standards-compliant.

#### Result
First-run onboarding is easier for Python teams with minimal template editing.

## Phase 3: Documentation Parity and Future Extensibility
Goal: Provide equivalent reference quality and chart forward compatibility for richer automation.

### 9. Add Python workshop reference document
#### Files
- workshops/courses_service_module_doc.md (retain as .NET workshop)
- New companion workshop file for Python web module documentation

#### Changes
1. Add a Python workshop artifact showing generated structure and role mapping.
2. Keep .NET workshop unchanged as a parallel example.

#### Result
Documentation consumers understand AKR works across architectures.

### 10. Record Python extraction roadmap
#### Files
- planning/ARCHITECTURE.md

#### Changes
1. Add a roadmap section for deterministic Python extraction in a later phase.
2. Define constraints and fallback behavior expectations.

#### Result
Future work is explicit; MVP rollout is not blocked.

## Proposed File Update Matrix

| Priority | File | Change Type | Layout | Why It Is Needed |
|---|---|---|---|---|
| High | README.md | Update | Both | Remove .NET-only onboarding impression; add Python monorepo and multi-repo paths/examples |
| High | examples/.akr-config-api.json | Update | Monorepo | Add Python API include/component mapping examples |
| High | .akr/examples/akr-config-monorepo.json | Update | Monorepo | Add Python monorepo path mappings |
| High | examples/.akr-config-python-api.json | New | Multi-repo | Python backend repo config with crossRepository linking to UI repo |
| High | examples/modules.trainingtracker.api.yaml | Keep existing | .NET reference | Preserve .NET reference while adding Python companions |
| High | examples/modules.python-web-monorepo.yaml | New | Monorepo | Canonical Python all-layers module grouping example |
| High | examples/modules.python-web-api.yaml | New | Multi-repo | Canonical Python backend-only module grouping example |
| High | copilot-instructions/backend-service.instructions.md | Update | Both | Framework-neutral role taxonomy guidance |
| High | validation/vale-rules/AKR/accept.txt | Update | Both | Allow Python vocabulary in generated docs |
| Medium | .akr/schemas/modules-schema.json | Update | Both | Optional language/framework hints |
| Medium | .akr/schemas/akr-config-schema.json | Update | Both | Better Python/monorepo and multi-repo examples and defaults |
| Medium | examples/workflows/validate-documentation.yml | Verify/update | Both | Ensure Python file pattern and docs coverage |
| Medium | examples/onboarding/modules.yaml.seed | Update | Both | Add optional onboarding hints for Python projects |
| Low | workshops/python_web_module_doc.md | New | Monorepo | Python workshop parity artifact (monorepo style) |
| Low | planning/ARCHITECTURE.md | Update | Both | Capture deterministic Python extraction roadmap |

## Suggested Python Web Module Taxonomy (Initial)
Use existing project_type values where possible to avoid schema churn.

1. api-backend
   - Route/View handlers
   - Service/helper orchestration
   - Validation forms/schemas
   - Integration clients
   - Applies in both monorepo and multi-repo backend repo
2. ui-component
   - Server-rendered templates and page-level UI modules
   - Use when Django templates are in the same repo as the backend (monorepo) or in a dedicated template-rendering repo
   - JavaScript/TypeScript UI repos in multi-repo setups continue to use the existing ui-component template unchanged
3. database/table docs
   - If SQL or Alembic/Django migration assets are included in-repo
   - In multi-repo: applies to the dedicated database repo

## Layout-to-AKR Config Mapping

| Layout | Repository | AKR Config Example | modules.yaml Example |
|---|---|---|---|
| Monorepo | Single repo: all layers | .akr-config-monorepo.json (update with Python paths) | modules.python-web-monorepo.yaml |
| Multi-repo API backend | Python backend repo only | .akr-config-python-api.json (new) | modules.python-web-api.yaml |
| Multi-repo UI | JS/TS frontend repo | Existing .akr-config-ui.json (no change needed) | Existing JS/TS examples |
| Multi-repo Database | Migration/SQL repo | Existing .akr-config-database.json (no change needed) | Existing database examples |

## Example Mapping for a Django-Style Module

### Monorepo: Shipment Tracking Search Module
- Entry points: app/urls.py + app/views.py
- Business logic: app/helpers.py
- Validation: app/forms.py
- Output docs: docs/modules/ShipmentTracking_doc.md

### Multi-Repo API Backend: Same Module (backend repo only)
- Entry points: app/urls.py + app/views.py
- Business logic: app/helpers.py
- Validation: app/forms.py
- Output docs: docs/modules/ShipmentTracking_doc.md
- Cross-repo link: `.akr-config-python-api.json` crossRepository block references the UI repo

### Suggested Module Files Role Labels (both layouts)
- app/views.py -> View Handler
- app/helpers.py -> Service/Integration Helper
- app/forms.py -> Validation Form
- app/urls.py -> Route Mapping

## Risks and Mitigations

### Risk 1: Over-expanding project_type enums too early
Mitigation: Keep api-backend as baseline and solve with role mapping guidance first.

### Risk 2: Breaking existing .NET onboarding behavior
Mitigation: Additive examples and optional schema fields only; retain all current .NET artifacts.

### Risk 3: Inconsistent generated terminology across teams
Mitigation: Update backend instruction guidance and Vale accepted terms in the same release.

### Risk 4: Teams expect deterministic Python extraction immediately
Mitigation: Clearly document MVP scope and Phase 3 roadmap in architecture planning docs.

### Risk 5: Multi-repo teams attempt to share a single modules.yaml across repos
Mitigation: Document clearly in the multi-repo config example and README note that each repository has its own modules.yaml scoped to that layer. The crossRepository block handles linking, not the manifest.

### Risk 6: Teams confuse monorepo Django template UI with a JavaScript UI repo
Mitigation: The layout mapping table in the taxonomy section explicitly distinguishes Django-rendered templates (Python, same repo) from JavaScript/TypeScript frontend repos (separate repo, existing UI config applies).

## Validation and Acceptance Criteria

### Technical Acceptance
1. Existing .NET examples continue validating with current schema.
2. Both new Python module manifest examples validate against modules schema.
3. The new multi-repo Python API config validates against the AKR config schema.
4. Sample workflow catches Python source and docs changes.
5. Vale passes against generated Python module docs with no avoidable terminology failures.

### Usability Acceptance
1. A Python web monorepo can complete onboarding using docs/examples without custom hidden instructions.
2. A Python web multi-repo team can configure cross-repository linking using the new Python API config example.
3. Generated docs use framework-accurate role names in both layout scenarios.
4. Operations Map and Data Operations sections remain complete and readable.
5. The layout mapping table unambiguously guides teams to the correct config and manifest example.

## Rollout Strategy

### Release 1 (MVP)
- README updates (monorepo and multi-repo paths)
- Python monorepo config examples
- Python multi-repo API config example (new .akr-config-python-api.json)
- Python module manifest examples (monorepo and multi-repo API)
- Backend role mapping guidance
- Vale accepted vocabulary updates

### Release 2 (Compatibility Hardening)
- Optional schema metadata enhancements
- Workflow and seed updates

### Release 3 (Parity + Roadmap)
- Python workshop artifact
- Architecture roadmap updates

## Proposed PR Breakdown

### PR 1: Python MVP Onboarding Assets
- README.md
- examples/.akr-config-api.json
- .akr/examples/akr-config-monorepo.json
- examples/.akr-config-python-api.json (new: multi-repo Python backend config)
- examples/modules.python-web-monorepo.yaml (new: monorepo manifest example)
- examples/modules.python-web-api.yaml (new: multi-repo API manifest example)
- copilot-instructions/backend-service.instructions.md
- validation/vale-rules/AKR/accept.txt

### PR 2: Schema and Workflow Alignment
- .akr/schemas/modules-schema.json
- .akr/schemas/akr-config-schema.json
- examples/workflows/validate-documentation.yml
- examples/onboarding/modules.yaml.seed

### PR 3: Documentation Parity and Roadmap
- workshops/python_web_module_doc.md
- planning/ARCHITECTURE.md

## Definition of Done
1. Python web monorepo onboarding path is documented and reproducible.
2. Python web multi-repo onboarding path (API backend layer) is documented and reproducible.
3. Both new Python module manifest examples are published and schema-valid.
4. The new multi-repo Python API config is published and schema-valid.
5. .NET onboarding behavior remains unchanged.
6. AKR maintainers have a staged roadmap for deeper Python automation.

## Appendix A: Minimal Onboarding Checklist for Python Teams

### Monorepo
1. Add AKR templates and skill assets using existing onboarding process.
2. Start from `examples/.akr-config-monorepo.json` or `examples/.akr-config-api.json` with Python paths.
3. Create `modules.yaml` from `examples/modules.python-web-monorepo.yaml` and review groupings.
4. Run documentation generation for one approved module.
5. Resolve unknown markers and run validation workflow.

### Multi-Repo (per repository)
1. Add AKR templates and skill assets to each repository separately using existing onboarding process.
2. For the API backend repo: start from `examples/.akr-config-python-api.json` and update `crossRepository` URLs.
3. For the UI repo: use existing `examples/.akr-config-ui.json` (JavaScript/TypeScript UI is already supported); no change needed.
4. For the database repo: use existing `examples/.akr-config-database.json`; no change needed.
5. Create `modules.yaml` per repository. The API backend uses `examples/modules.python-web-api.yaml` as reference.
6. Run documentation generation per repository independently.
7. Verify cross-repo linking by confirming related repo references are reachable and documented.

## Appendix B: Notes for Future Enhancements
1. Add deterministic extraction support for Python classes/functions/decorators.
2. Add framework profiles for Django/FastAPI/Flask.
3. Add optional role normalization checks during validation to improve consistency across projects.
4. Consider a dedicated multi-repo Python workshop artifact once the monorepo workshop artifact is stable.
