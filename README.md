# Core AKR Templates Repository

**Centralized documentation templates, charters, and standards for Emerson AKR (Application Knowledge Repository) system**

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/reyesmelvinr-emr/core-akr-templates)
[![Status](https://img.shields.io/badge/status-Pilot%20Phase%202-orange.svg)](AKR_Tracking.md)
[![License](https://img.shields.io/badge/license-Internal-red.svg)](LICENSE)
[![Maintained by](https://img.shields.io/badge/maintained%20by-CDS%20Team%20Hawkeye-green.svg)](README.md)

---

## 📋 Overview

This repository serves as the **single source of truth** for AKR documentation templates, charters, and standards used across all Emerson projects. It enables:

- ✅ **Module-based documentation** with three-tier architecture (source modules, database objects, consolidated features)
- ✅ **GitHub Copilot Agent Skill workflow** with three modes: grouping proposal, documentation generation, and interactive HITL completion
- ✅ **Context-efficient generation** with compressed charters and template variants
- ✅ **Version-controlled standards** with semantic versioning and traceability
- ✅ **Zero infrastructure cost** (leverages existing GitHub Copilot licenses)

**⚠️ Status: Currently in Phase 2 (Pilot Onboarding).** Not yet production ready. See [AKR_Tracking.md](AKR_Tracking.md) for implementation status and roadmap.

---

## 🎯 Key Architecture

### 🏗️ Three-Tier Documentation Hierarchy
- **Level 1: Module Documentation** - Grouped source files (5-8 files per module) with condensed charter context
- **Level 2: Database Object Documentation** - Individual database objects (tables, views, procedures)
- **Level 3: Feature Consolidation** - Cross-module feature documentation aggregated from Levels 1 and 2

### 📚 Documentation Templates (10 Total)
**Level 1 (Module) Templates:**
- `lean_baseline_service_template_module.md` - Backend module variant
- `ui_component_template_module.md` - UI module variant

**Level 2 (Database) Templates:**
- `table_doc_template.md` - Database tables
- `embedded_database_template.md` - Embedded database services

**Level 3 (Feature) Templates:**
- `feature-consolidated.md` - Feature consolidation
- `feature-testing-consolidated.md` - Feature testing consolidation

**Reference Templates** (kept for legacy and specialized use):
- `comprehensive_service_template.md` - Reference material
- `standard_service_template.md` - Reference material
- `minimal_service_template.md` - Reference material
- `legacy_inventory_template.md` - Legacy system documentation

### 📖 4 AKR Charters (with Compressed Variants)
- **General** - Overall AKR standards (compressed: ~2,500 tokens)
- **Backend** - Backend service guidelines (compressed: ~2,500 tokens)
- **UI** - Frontend component guidelines (compressed: ~2,500 tokens)
- **Database** - Database documentation standards (compressed: ~2,500 tokens)

### 🤖 GitHub Copilot Agent Skill Workflow
- **Mode A** - Propose module groupings from project source code
- **Mode B** - Generate module documentation with SSG-style semantic search/generation passes
- **Mode C** - Interactive HITL completion for unresolved `❓` sections in existing drafts

### 🏷️ Tagging Strategy
- **Module grouping** via `modules.yaml` manifest
- **Feature-to-module traceability** with tag registry
- **Project classification** with `project_type` enum (api-backend, ui-component, microservice, general)
- **Compliance modes** with pilot vs. production governance

---

## 📁 Repository Structure

```
core-akr-templates/
├── .akr/
│   ├── TEMPLATE_MANIFEST.json          # Template metadata and version registry
│   ├── schemas/
│   │   ├── modules-schema.json         # Module manifest JSON Schema
│   │   ├── akr-config-schema.json      # Project configuration schema
│   │   └── consolidation-config-schema.json  # Feature consolidation config
│   ├── templates/                      # All documentation templates (Level 1, 2, 3)
│   │   ├── lean_baseline_service_template_module.md
│   │   ├── ui_component_template_module.md
│   │   ├── table_doc_template.md
│   │   ├── embedded_database_template.md
│   │   ├── feature-consolidated.md
│   │   ├── feature-testing-consolidated.md
│   │   ├── comprehensive_service_template.md (reference)
│   │   └── ...
│   ├── charters/                       # Full charters (for reference)
│   │   ├── AKR_CHARTER.md
│   │   ├── AKR_CHARTER_BACKEND.md
│   │   ├── AKR_CHARTER_UI.md
│   │   └── AKR_CHARTER_DB.md
│   ├── scripts/                        # Validation and automation
│   │   └── validate_documentation.py   # Core validation engine
│   ├── workflows/                      # GitHub Actions workflows
│   │   └── validate-documentation.yml
│   └── vale-rules/                     # Vale prose linting rules
│       └── AKR/
├── copilot-instructions/               # Compressed charters for context efficiency
│   ├── backend-service.instructions.md
│   ├── ui-component.instructions.md
│   └── database.instructions.md
├── .github/
│   ├── skills/                         # GitHub Copilot Agent Skills
│   │   └── akr-docs/
│   │       ├── SKILL.md                # Three-mode workflow (A, B, C)
│   │       ├── SKILL-COMPAT.md         # Model compatibility matrix
│   │       ├── postToolUse.json        # Hook for session logging
│   │       └── agentStop.json          # Hook for change detection
│   ├── workflows/
│   │   └── distribute-skill.yml        # Skill distribution to registered repos
│   └── registered-repos.yaml           # List of authorized pilot/production repos
├── docs/                               # Documentation
│   ├── DEVELOPER_REFERENCE.md
│   ├── VALIDATION_GUIDE.md
│   ├── TAG_REGISTRY_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── ...
├── evals/                              # Evaluation cases and benchmarks
│   ├── benchmark.json                  # Premium request, quality, and quota metrics
│   └── cases/                          # Test cases for different scenarios
│       ├── mode-a-standard.yaml
│       ├── mode-b-coursedomain.yaml
│       ├── mode-b-large-module.yaml
│       └── ssg-pass-sequence.yaml
├── examples/                           # Example configurations
│   ├── modules.trainingtracker.api.yaml
│   └── workflows/
│       └── validate-documentation.yml
├── templates/                          # Historical module templates (deprecated)
│   ├── lean_baseline_service_template_module.md
│   └── ui_component_template_module.md
├── workshops/                          # Training and acceptance test examples
│   └── courses_service_module_doc.md   # Example module doc output
├── README.md                           # This file
├── CHANGELOG.md                        # Release notes and changes
└── LICENSE                             # Internal use license
```

---

## 🚀 Getting Started

### Prerequisites
- Git installed (with submodule support)
- GitHub account with access to this repository
- GitHub Copilot license (for documentation generation with Agent Skills)
- VS Code with GitHub Copilot extension (or use with Copilot CLI)
- Python 3.10+ (for validation and automation scripts)

### Phase 2 Pilot Onboarding (Current)

AKR is currently in **Phase 2 - Pilot Onboarding**. Teams interested in participating should:

1. **Review** [AKR_Tracking.md](AKR_Tracking.md) for current status and roadmap
2. **Contact** the CDS Team Hawkeye #akr-documentation channel
3. **Understand** that this is a managed pilot with structured feedback collection

### For Pilot Application Teams

#### 1. Add `.akr` Submodule
Add this repository as a submodule to your project:

```bash
git submodule add https://github.com/reyesmelvinr-emr/core-akr-templates.git .akr/templates
git submodule update --init --recursive
```

#### 2. Create `modules.yaml` Manifest
Create a `modules.yaml` file in your project root to define module groupings:

```yaml
project:
  name: YourProject.Api
  layer: API
  standards_version: "1.1.0"
  compliance_mode: pilot  # or production

modules:
  - name: CourseDomain
    project_type: api-backend
    feature: CourseManagement
    files:
      - src/Controllers/CourseController.cs
      - src/Services/CourseService.cs
      - src/Repositories/ICourseRepository.cs
      - src/Infrastructure/EfCourseRepository.cs
      - src/Dtos/CourseDto.cs
    doc_output: docs/modules/CourseDomain_doc.md
    status: approved

database_objects:
  - name: training.Courses
    type: table
    doc_output: docs/database/Courses_doc.md
```

See [examples/modules.trainingtracker.api.yaml](examples/modules.trainingtracker.api.yaml) for full schema.

#### 3. Copy Distributed Skill Files
The GitHub Copilot Agent Skill and supporting files are distributed via:  
- `.github/skills/akr-docs/SKILL.md` - Three-mode workflow definition
- `.github/skills/akr-docs/SKILL-COMPAT.md` - Model compatibility matrix
- `.github/hooks/postToolUse.json` - Session logging hook
- `.github/hooks/agentStop.json` - Change detection hook

These are automatically copied during enrollment from the [skill distribution workflow](distribute-skill.yml).

#### 4. Add Condensed Charter Instructions
Copy the compressed charter for your project type to `.github/copilot-instructions.md`:

```bash
# For API/backend projects
cp .akr/templates/copilot-instructions/backend-service.instructions.md .github/copilot-instructions.md

# For UI projects
cp .akr/templates/copilot-instructions/ui-component.instructions.md .github/copilot-instructions.md
```

#### 5. Set Up Validation
Copy the validation workflow to enable CI checks:

```bash
cp .akr/templates/examples/workflows/validate-documentation.yml .github/workflows/
```

#### 6. Use the Agent Skill Workflow

**Mode A — Propose Module Groupings** (first time)
```
/akr-docs mode-a
→ Scans project files, proposes module groupings, creates draft modules.yaml PR
```

**Mode B — Generate Documentation** (after Mode A approval)
```
/akr-docs mode-b CourseDomain
→ Reads approved modules.yaml, generates module documentation, creates draft PR
```

**Mode C — Interactive HITL Completion** (during review)
```
/akr-docs mode-c CourseDomain_doc.md
→ Walks through unresolved ❓ sections interactively, applies edits as you approve
```

See [.github/skills/akr-docs/SKILL.md](.github/skills/akr-docs/SKILL.md) for full details.

---

## 📊 Module Documentation Selection

| Project Type | Use Template | Level | Time to Document |
|---|---|---|---|
| API / Backend Service | `lean_baseline_service_template_module.md` | Level 1 | 10-15 min per module |
| UI Component Library | `ui_component_template_module.md` | Level 1 | 8-12 min per module |
| Database Table / View | `table_doc_template.md` | Level 2 | 6-10 min per object |
| Embedded Database | `embedded_database_template.md` | Level 2 | 6-10 min per service |
| Cross-Module Feature | `feature-consolidated.md` | Level 3 | 15-20 min (auto-aggregated) |

**Key Differences from v1.0:**
- Module grouping is **human-proposed first** (Mode A), then approved by tech lead
- Documentation is **generated per module**, not per individual file
- **Condensed charters** (2,500 tokens) provide context efficiency vs. full charters
- **Three documentation levels** with clear ownership and audience (Level 1: developer, Level 2: DBA, Level 3: product owner)

---

## 🔄 Versioning and Roadmap

Follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - Breaking changes to architecture or template structure
- **MINOR** (1.X.0) - New templates, features, or backwards-compatible enhancements
- **PATCH** (1.0.X) - Bug fixes, documentation clarifications

**Current Version**: 1.1.0 (Phase 1 - Foundation Complete)

### Version History
- **1.1.0** (2026-03-18) - Module-based architecture, Agent Skill workflow, three-tier hierarchy. Phase 1 (Foundation) COMPLETE.
- **1.0.0** (2026-01-14) - Initial release with 8 templates and MCP infrastructure (bootstrapped).

### Upcoming Phases
- **Phase 2** (Current): Pilot Onboarding — 1-2 weeks/project, structured feedback collection
- **Phase 2.5**: Coding Agent Spike — Binary GO/NO-GO decision on automation scope (1 week)
- **Phase 3** (Conditional): Automation Extension — Extended automation if Phase 2.5 identifies gaps (2-4 weeks)
- **Phase 4**: Feature Consolidation — Cross-module aggregation and scaling (3-4 weeks)

See [AKR_Tracking.md](AKR_Tracking.md) for detailed phase gates and metrics.

---

## 🏷️ Tagging Strategy

All documentation includes YAML front matter for traceability:

```yaml
---
title: "UserService Documentation"
component_type: "Backend Service"
features:
  - "Authentication"
  - "User Management"
technologies:
  - "C#"
  - ".NET Core 8.0"
business_domain: "Identity Management"
status: "Active"
priority: "High"
---
```

**Benefits:**
- ✅ Feature-to-component traceability
- ✅ Cross-repository relationship mapping
- ✅ Automated architecture diagrams
- ✅ Orphaned component detection

---

## 🛡️ Quality Validation

### Vale Prose Linting
- Enforces terminology standards
- Checks writing style and readability
- Validates mandatory sections

### GitHub Actions CI/CD
- Automated validation on every PR
- Completeness scoring (0-100%)
- Branch protection rules
- Inline annotations with Checks API

### Completeness Thresholds
- **Critical components**: 85%+ required
- **Standard components**: 75%+ required
- **Utilities**: 70%+ required

---

## � Transparency and HITL Markers

All generated documentation uses transparency markers to communicate automation state and human input requirements:

| Marker | Meaning | Action |
|---|---|---|
| `🤖` | Automated content generated with confidence | Review for accuracy; minimal edits expected |
| `❓` | Unresolved question requiring human input | **PROD MODE**: Blocks PR merge; **PILOT**: Warning only |
| `👤` | Section marked for human completion | Developer provides input during Mode C HITL pass |
| `DEFERRED` | Intentionally deferred to later phase or external owner | Document rationale and owner; no merge block |
| `VERIFY` | Content auto-generated but confidence low; needs verification | Verify against actual code during review |
| `NEEDS` | Indicates a gap or missing prerequisite | Address explicitly; cannot defer in production mode |

These markers enable:
- ✅ Clear visibility of automation completeness
- ✅ Structured HITL workflows (Mode C)
- ✅ Progressive compliance mode graduation (pilot → production)
- ✅ Audit trail for governance and compliance

---

## 📚 Documentation

**Core Documentation** (in this repository):
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Three-tier hierarchy, module grouping, agent skill design
- **[VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md)** — Compliance modes, CI validation, rule reference
- **[DEVELOPER_REFERENCE.md](docs/DEVELOPER_REFERENCE.md)** — HITL role mapping, section requirements, template usage
- **[TAG_REGISTRY_GUIDE.md](docs/TAG_REGISTRY_GUIDE.md)** — Feature tagging, tag registry schema, traceability
- **[CHANGELOG.md](CHANGELOG.md)** — Release notes and breaking changes
- **[Copilot Instructions](copilot-instructions/)** — Compressed charters (backend, UI, database)
- **[Agent Skill](/.github/skills/akr-docs/SKILL.md)** — Mode A/B/C workflow definition
- **[Compatibility Matrix](/.github/skills/akr-docs/SKILL-COMPAT.md)** — Model pass rates and workarounds

**Full Charters** (reference and detail):
- `charters/AKR_CHARTER.md` — General standards
- `charters/AKR_CHARTER_BACKEND.md` — Backend service documentation standards
- `charters/AKR_CHARTER_UI.md` — UI component documentation standards
- `charters/AKR_CHARTER_DB.md` — Database documentation standards

**In Application Repositories**:
- `.akr/modules.yaml` — Your project's module manifest
- `.github/copilot-instructions.md` — Compressed charter for your project type
- `.github/skills/akr-docs/SKILL.md` — Agent Skill workflow (distributed)

---

## 🤝 Contributing

### For Pilot Teams
Currently accepting managed pilot teams. See [AKR_Tracking.md](AKR_Tracking.md) for onboarding workflow.

### For Standards Maintainers (CDS Team Hawkeye)

#### Adding a New Template
1. Create template in `templates/` with YAML front matter structure
2. Update `TEMPLATE_MANIFEST.json` with metadata and version
3. Add or update corresponding charter section if introducing new documentation level
4. Create acceptance test in `workshops/` or `evals/cases/` demonstrating expected output
5. Update this README.md and `CHANGELOG.md`
6. Submit PR with template, schema updates (if needed), and tests
7. After merge, tag with new version: `git tag -a vX.Y.Z -m "Release message"`

#### Updating Existing Templates
1. Assess scope: patch (bug/clarification) vs. minor (new section) vs. major (breaking structure)
2. Make changes to template file(s) and corresponding schemas
3. Update `TEMPLATE_MANIFEST.json` version field
4. Add entry to `CHANGELOG.md` with rationale
5. Consider backwards-compatibility impact on existing docs
6. Update `evals/benchmark.json` if affecting generation quality criteria
7. Submit PR with impact assessment
8. After merge, tag appropriately

#### Updating Compressed Charters
1. Start from full charter source in `charters/`
2. Retain required sections, compress explanatory prose
3. Keep token targets: backend/UI ~2,500, database ~2,500, general ~2,500
4. Output to `copilot-instructions/{type}.instructions.md`
5. Validate token counts with dual tokenizers (cl100k for Copilot, o200k for GPT-4o)
6. Update charter front matter with `compressed: true` and source reference

#### Template Guidelines
- ✅ Use transparency markers (🤖 ❓ 👤 VERIFY DEFERRED NEEDS)
- ✅ Include comprehensive usage examples
- ✅ Define clear mandatory vs optional sections per `project_type`
- ✅ Provide interview questions/prompts for human-required sections
- ✅ Target token load: keep templates < 7,000 tokens at 7,000 chars
- ✅ Follow Vale linting rules from `vale-rules/AKR/`
- ✅ Include YAML front matter with `feature`, `layer`, `project_type`, `status`, `compliance_mode`

---

## 📈 Pilot Metrics and Success Criteria

Phase 2 (Pilot) is actively collecting the following metrics:

### Module Grouping (Mode A)
- **Grouping validation time**: Target ≤ 15 min per project
- **Reassignment count**: Files moved during review (measures agent accuracy)
- **Unassigned file rate**: % of files requiring manual assessment

### Documentation Generation (Mode B)
- **Time-to-first-documented-PR**: Target ≤ 45 min
- **First-run CI pass rate**: Target ≥ 95%
- **Unresolved marker rate**: Target < 5% of generated content

### Quality and Compliance
- **Vale lint pass rate**: Target > 85%
- **Completeness score**: Target ≥ 75%
- **Premium request baseline**: Tracks cost per documentation task (Phase 2/2.5 data collection)

### Time Savings
- **Pre-AKR baseline**: 60-90 minutes per module (full manual documentation)
- **With AKR v1.1**: 10-15 minutes per module (Mode B generation + Mode C HITL)
- **Target savings**: 70-85%

Detailed metrics captured in [AKR_Tracking.md](AKR_Tracking.md#metrics)


---

## 🆘 Support

### Common Issues

**Agent Skill not loading in VS Code**
- ✅ Confirm `disable-model-invocation: true` is in SKILL.md frontmatter
- ✅ Use explicit `/akr-docs mode-a` command instead of conversational intent
- ✅ Check that `SKILL.md` is in `.github/skills/akr-docs/` (distributed via workflow)
- ⚠️ See [SKILL-COMPAT.md](/.github/skills/akr-docs/SKILL-COMPAT.md) for model-specific workarounds

**Submodule not updating**
```bash
# Update submodule to latest core-akr-templates
git submodule update --remote .akr/templates

# Or pinned version (Phase 0)
git submodule set-branch --branch v1.1.0 .akr/templates
git submodule update .akr/templates
```

**Validation failing in CI/CD**
- Check `modules.yaml` syntax against [schemas/modules-schema.json](schemas/modules-schema.json)
- Verify `feature` field matches an entry in `tag-registry.json`
- Review GitHub Actions logs for `validate_documentation.py` output
- Run local validation: `python .akr/templates/.akr/scripts/validate_documentation.py --changed-files`
- See [VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md) for compliance mode details

**Unresolved ❓ markers blocking merge (production mode)**
- Use Mode C: `/akr-docs mode-c docs/modules/YourModule_doc.md`
- Or manually resolve and replace `❓` markers with content
- Mark as `DEFERRED` with rationale if deferring intentionally (documented owner required)

### Getting Help
- **Support Channel**: #akr-documentation (MS Teams / Slack)
- **Implementation Tracking**: [AKR_Tracking.md](AKR_Tracking.md)
- **Technical Documentation**: See [docs/](docs/) directory
- **Agent Skill Compatibility**: [SKILL-COMPAT.md](/.github/skills/akr-docs/SKILL-COMPAT.md)
- **Validation Reference**: [VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md)

---

## 🙏 Acknowledgments

**Maintained by**: CDS - Team Hawkeye  
**Contributors**: [List of contributors]  
**Special Thanks**: GitHub Copilot team for MCP support

---

**Version**: 1.1.0 (Phase 1 - Foundation Complete)  
**Last Updated**: 2026-03-18  
**Status**: Beta / Pilot Phase (Phase 2 - Onboarding) ⚠️  
**Next Gate**: Phase 2.5 (Coding Agent Spike) — TBD  
