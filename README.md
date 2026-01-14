# Core AKR Templates Repository

**Centralized documentation templates and standards for Emerson AKR (Actionable Knowledge Repository) system**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/YourUsername/core-akr-templates)
[![License](https://img.shields.io/badge/license-Internal-red.svg)](LICENSE)
[![Maintained by](https://img.shields.io/badge/maintained%20by-CDS%20Team%20Hawkeye-green.svg)](README.md)

---

## 📋 Overview

This repository serves as the **single source of truth** for AKR documentation templates, charters, and standards used across all Emerson projects. It enables:

- ✅ **Consistent documentation** across all teams and projects
- ✅ **Template-driven generation** with GitHub Copilot and Local MCP
- ✅ **Version-controlled standards** with semantic versioning
- ✅ **Team customization** through template inheritance
- ✅ **Zero infrastructure cost** (leverages existing GitHub Copilot licenses)

---

## 🎯 Key Features

### 📚 8 Documentation Templates
- **Comprehensive** - Complex, critical services (15-20 min)
- **Standard** - Typical backend services (10-15 min)
- **Lean** - Simple utilities (5-10 min)
- **Minimal** - Very simple classes (3-5 min)
- **UI Component** - React/Angular components (8-12 min)
- **Table** - Database tables (6-10 min)
- **Embedded Database** - Local storage (6-10 min)
- **Legacy Inventory** - Legacy systems (10-15 min)

### 📖 4 AKR Charters
- **General** - Overall AKR standards
- **Backend** - Backend service guidelines
- **UI** - Frontend component guidelines
- **Database** - Database documentation standards

### 🔧 Template Inheritance
- **Organization templates** - Base templates with mandatory sections
- **Team extensions** - Custom sections per team
- **Merge strategy** - Extend base templates without forking

### 🏷️ Tagging Strategy
- Feature-to-component traceability
- Cross-repository relationship mapping
- Automated tag registry and synonym support

---

## 📁 Repository Structure

```
core-akr-templates/
├── .akr/
│   ├── TEMPLATE_MANIFEST.json          # Template metadata and versioning
│   ├── templates/                      # Base organization templates
│   │   ├── comprehensive_service_template.md
│   │   ├── standard_service_template.md
│   │   ├── lean_baseline_service_template.md
│   │   ├── minimal_service_template.md
│   │   ├── ui_component_template.md
│   │   ├── table_doc_template.md
│   │   ├── embedded_database_template.md
│   │   └── legacy_inventory_template.md
│   ├── charters/                       # AKR documentation standards
│   │   ├── AKR_CHARTER.md
│   │   ├── AKR_CHARTER_BACKEND.md
│   │   ├── AKR_CHARTER_UI.md
│   │   └── AKR_CHARTER_DB.md
│   ├── standards/                      # Guidelines and instructions
│   │   └── copilot-instructions.md
│   └── examples/                       # Example configurations
│       ├── akr-config-webapp1-ui.json
│       ├── akr-config-webapp1-api.json
│       └── akr-config-webapp1-feature.json
├── README.md                           # This file
└── LICENSE                             # Internal use license
```

---

## 🚀 Getting Started

### Prerequisites
- Git installed
- GitHub account with access to this repository
- GitHub Copilot license (for documentation generation)
- Python 3.10+ (for local MCP server)
- VS Code with GitHub Copilot extension

### For Application Teams

#### 1. Clone Template Repository (Automatic)
Templates are automatically synced when you set up your application repository with AKR documentation support.

#### 2. Add `.akr-config.json` to Your Repository
Copy one of the example configs from `.akr/examples/` and customize:

```bash
# For UI projects
cp core-akr-templates/.akr/examples/akr-config-webapp1-ui.json YourRepo/.akr-config.json

# For API projects
cp core-akr-templates/.akr/examples/akr-config-webapp1-api.json YourRepo/.akr-config.json
```

Edit `.akr-config.json`:
- Update `project.name` and `project.description`
- Set `templates.repository` to this repository URL
- Configure `component_mappings` for your project structure
- Add team member emails to `team.roles`

#### 3. Run Setup Script
```powershell
# Windows
.\setup.ps1

# Mac/Linux
./setup.sh
```

This will:
- ✅ Install Python dependencies
- ✅ Clone template repository to `~/.akr/templates/`
- ✅ Configure VS Code MCP
- ✅ Install Git hooks for auto-sync
- ✅ Run health check

#### 4. Start Using AKR Documentation
In VS Code with GitHub Copilot:

```
/docs.generate src/components/Button.tsx
→ Generates docs/components/Button.md

/docs.interview
→ Answer business context questions

/docs.update src/components/Button.tsx
→ Updates docs when code changes
```

---

## 📊 Template Selection Guide

| Code Type | Complexity | Template | Time |
|-----------|-----------|----------|------|
| Critical backend services | High | Comprehensive | 15-20 min |
| Standard CRUD services | Medium | Standard | 10-15 min |
| Utility classes | Low | Lean | 5-10 min |
| DTOs, constants, enums | Very Low | Minimal | 3-5 min |
| React/Angular components | Medium | UI Component | 8-12 min |
| Database tables | Medium | Table | 6-10 min |
| Embedded databases | Medium | Embedded DB | 6-10 min |
| Legacy systems | High | Legacy Inventory | 10-15 min |

---

## 🔄 Template Versioning

Templates follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - Breaking changes to template structure
- **MINOR** (1.X.0) - New templates added, backwards-compatible
- **PATCH** (1.0.X) - Bug fixes, clarifications

**Current Version**: 1.0.0

### Version History
- **1.0.0** (2026-01-14) - Initial release with 8 templates

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

## 🔧 Template Inheritance

Teams can extend base templates with custom sections while preserving organizational standards.

### Example: Extending UI Component Template

**Base Template** (`.akr/templates/ui-component.md`):
```markdown
## Overview (Mandatory - Org)
## Purpose (Mandatory - Org)
## Props (Mandatory - Org)
## Usage Examples (Mandatory - Org)
```

**Team Extension** (`.akr/templates/team/ui-component-webapp1.md`):
```markdown
## Performance Considerations (Mandatory - Team)
## Accessibility Checklist (Mandatory - Team)
## Storybook Story (Optional - Team)
```

**Merged Result**:
```markdown
## Overview (Mandatory - Org)
## Purpose (Mandatory - Org)
## Props (Mandatory - Org)
## Usage Examples (Mandatory - Org)
## Performance Considerations (Mandatory - Team)
## Accessibility Checklist (Mandatory - Team)
## Storybook Story (Optional - Team)
```

---

## 📚 Documentation

- **Setup Guide**: See `setup.ps1` or `setup.sh`
- **User Guide**: `USER_GUIDE.md` (in application repositories)
- **Cheat Sheet**: `CHEAT_SHEET.md` (in application repositories)
- **Copilot Instructions**: `.akr/standards/copilot-instructions.md`
- **Template Manifest**: `.akr/TEMPLATE_MANIFEST.json`

---

## 🤝 Contributing

### For Template Maintainers

#### Adding a New Template
1. Create template in `.akr/templates/`
2. Update `TEMPLATE_MANIFEST.json` with metadata
3. Add charter/guidelines if needed
4. Create example config in `.akr/examples/`
5. Update README.md
6. Tag with new version: `git tag -a v1.1.0 -m "Add new template"`

#### Updating Existing Templates
1. Make changes to template file
2. Update `TEMPLATE_MANIFEST.json` version
3. Add changelog entry
4. Consider backwards compatibility
5. Tag appropriately (patch, minor, or major)

#### Template Guidelines
- ✅ Use transparency markers (🤖 ❓ 👤)
- ✅ Include comprehensive usage examples
- ✅ Define clear mandatory vs optional sections
- ✅ Provide interview questions for human-required sections
- ✅ Keep estimated time accurate
- ✅ Follow Vale linting rules

---

## 📈 Metrics and Success Criteria

### Coverage Metrics
- **Documentation coverage**: % of code files with documentation
- **Completeness**: Average completeness score
- **Freshness**: Days since last update

### Time Savings
- **Before AKR**: 60-80 minutes per file
- **With AKR**: 10-15 minutes per file
- **Time savings**: 70-90%

### Quality Metrics
- **Vale lint pass rate**: >80% target
- **PR merge time**: 50% reduction target
- **Team satisfaction**: >4.0/5.0 target

---

## 💰 Cost Analysis

### Implementation Cost
- **Template repository setup**: $0 (Git repository)
- **GitHub Copilot licenses**: $0 (existing licenses)
- **Local MCP setup**: $0 (runs on developer machines)
- **GitHub Actions**: $0-20/month (free tier sufficient for most teams)

### Monthly Operating Cost
- **LLM inference**: $0 (included in GitHub Copilot)
- **GitHub Actions**: $0-15/month (depends on usage)
- **Infrastructure**: $0 (no cloud resources needed)

**Total Monthly Cost**: $0-15 🎉

---

## 🆘 Support

### Common Issues

**Templates not syncing**
```bash
# Manual sync
cd ~/.akr/templates
git pull origin main

# Or use MCP command
/docs.update-templates
```

**MCP server not connecting**
```bash
# Check Python version
python --version

# Reload VS Code
Ctrl+Shift+P → "Reload Window"

# Run health check
/docs.health-check
```

**Validation failing in CI/CD**
- Check `.akr-config.json` syntax
- Verify template repository access
- Review GitHub Actions logs
- Run local validation: `python scripts/validate-docs.py`

### Getting Help
- **Support Channel**: #akr-documentation (Teams/Slack)
- **Technical Lead**: [Your Name]
- **Documentation**: See `.akr/standards/copilot-instructions.md`
- **Health Check**: `/docs.health-check` in VS Code

---

## 📄 License

**Internal Use Only** - Emerson Electric Co.  
Not for public distribution.

---

## 🙏 Acknowledgments

**Maintained by**: CDS - Team Hawkeye  
**Contributors**: [List of contributors]  
**Special Thanks**: GitHub Copilot team for MCP support

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-14  
**Status**: Production Ready ✅
