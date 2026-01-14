# GitHub Copilot Instructions for AKR Documentation

## 🎯 Purpose

This repository contains **centralized AKR documentation templates** used across all Emerson projects. When working with AKR documentation, follow these guidelines to ensure consistency, quality, and compliance with organizational standards.

---

## 📋 Core Principles

### 1. **Transparency First**
Every documentation file MUST use transparency markers to distinguish content origins:
- 🤖 **AI-generated** - Content created by AI that should be reviewed
- ❓ **Human-required** - Sections requiring human input (business context, decisions, troubleshooting)
- 👤 **Human-written** - Content written by humans that must be preserved

### 2. **Template-Driven Generation**
Always use the appropriate template from `.akr/templates/`:
- **comprehensive_service_template.md** - Complex, critical services (15-20 min)
- **standard_service_template.md** - Typical backend services (10-15 min)
- **lean_baseline_service_template.md** - Simple utilities (5-10 min)
- **minimal_service_template.md** - Very simple classes (3-5 min)
- **ui_component_template.md** - React/Angular components (8-12 min)
- **table_doc_template.md** - Database tables (6-10 min)
- **embedded_database_template.md** - Embedded databases (6-10 min)
- **legacy_inventory_template.md** - Legacy systems (10-15 min)

### 3. **Human-in-the-Loop Workflow**
Documentation generation follows this workflow:
1. **Analyze code** using Tree-sitter AST parsing
2. **Select appropriate template** based on code complexity
3. **Generate AI content** (🤖 sections)
4. **Mark human-required sections** (❓) for interview questions
5. **Conduct interview** to gather business context
6. **Finalize documentation** with both AI and human content

### 4. **Surgical Updates Only**
When updating existing documentation:
- **Preserve all 👤 human-written content**
- **Update only 🤖 AI-generated sections** that correspond to code changes
- **Never remove ❓ human-required sections**
- **Maintain changelog** with update history

---

## 🚀 Slash-Commands for Documentation Generation

### Generation Commands
```
/docs.generate <filepath>
- Generate new documentation for a source file
- Automatically selects appropriate template
- Creates file at configured output path

/docs.interview
- Start interactive interview to answer ❓ sections
- Routes questions based on user's role
- Saves answers to documentation file
```

### Update Commands
```
/docs.update <filepath>
- Surgical update of AI sections only
- Preserves all human-written content
- Updates only sections affected by code changes

/docs.update.api <filepath>
- Update only API-related sections
- Used after API signature changes

/docs.update.architecture <filepath>
- Update only architecture sections
- Used after dependency or design changes
```

### Role Management
```
/docs.my-role
- Show your current role (auto-detected from git config)

/docs.set-role <role>
- Temporarily override role for interview mode
- Roles: tech-lead, developer, product-owner, qa, architect
- Override persists until MCP restart
```

### Utility Commands
```
/docs.health-check
- Validate MCP setup and configuration
- Check template repository sync status
- Verify Tree-sitter and Vale installation

/docs.update-templates
- Manually sync templates from Git repository
- Use if auto-sync fails or templates outdated
```

---

## 📁 Repository Structure Requirements

Each application repository using AKR documentation must have:

```
YourRepo/
├── .akr-config.json          # AKR configuration (REQUIRED)
├── docs/                      # Documentation output folder
│   ├── components/
│   ├── services/
│   └── architecture/
├── .github/
│   ├── workflows/
│   │   └── validate-documentation.yml  # CI/CD validation
│   └── copilot-instructions.md         # This file (copied to app repo)
└── .vale/                     # Vale prose linting rules
    ├── .vale.ini
    └── styles/
        └── AKR/
```

---

## 🏷️ Tagging Strategy

All documentation files should include YAML front matter with tags:

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
  - "Entity Framework"
business_domain: "Identity Management"
status: "Active"
priority: "High"
last_updated: "2026-01-14"
---
```

**Tag Categories:**
- **feature** - Business features (e.g., "Authentication", "Reporting")
- **component-type** - Technical type (e.g., "UI Component", "API Controller")
- **technology** - Tech stack (e.g., "React", "TypeScript", "C#")
- **business-domain** - Business area (e.g., "Identity", "Payments")
- **status** - Lifecycle state (e.g., "Active", "Deprecated", "Legacy")
- **priority** - Importance (e.g., "Critical", "High", "Medium", "Low")

---

## ✅ Documentation Quality Standards

### Required Sections (varies by template)
- **Overview** - Always required, high-level summary
- **Purpose** - Why this component exists
- **Architecture** - How it's structured (for services)
- **Dependencies** - What it relies on
- **Usage Examples** - How to use it
- **Testing** - How to test it

### Human-Required Sections (❓)
- **Business Context** - Why was this built? What problem does it solve?
- **Architecture Decisions** - Why this approach over alternatives?
- **Troubleshooting** - Common issues and resolutions
- **Future Enhancements** - Planned improvements

### AI-Generated Sections (🤖)
- **Method Signatures** - Extracted from code
- **Parameter Descriptions** - Inferred from code
- **Return Values** - Extracted from code
- **Dependencies** - Analyzed from imports
- **Code Examples** - Generated from usage patterns

---

## 🔍 Code Analysis Capabilities

When generating documentation, leverage Tree-sitter AST parsing to extract:

### For Backend Services (C#, Java, Python)
- **Class structure**: Name, namespace, base classes, interfaces
- **Methods**: Signatures, parameters, return types, access modifiers
- **Dependencies**: Import statements, injected services
- **Design patterns**: Repository, Factory, Singleton, Service
- **Complexity metrics**: Cyclomatic complexity, LOC

### For UI Components (TypeScript, React)
- **Component structure**: Props, state, hooks
- **Event handlers**: User interactions
- **Styling**: CSS modules, styled-components
- **Dependencies**: Imported libraries
- **Accessibility**: ARIA attributes

### For Database Objects (SQL)
- **Schema**: Tables, columns, data types
- **Relationships**: Foreign keys, references
- **Indexes**: Performance optimization
- **Constraints**: Data integrity rules

---

## 🛡️ Validation and Quality Gates

### Vale Prose Linting
Documentation is validated for:
- **Terminology**: Approved vs deprecated terms
- **Spelling**: Technical term whitelist
- **Writing style**: Active voice, readability
- **Mandatory sections**: Template compliance

### GitHub Actions Validation
On every pull request:
- ✅ Check if documentation exists for changed code
- ✅ Validate template structure
- ✅ Verify required sections present
- ✅ Run Vale prose linting
- ✅ Calculate completeness score (0-100%)
- ✅ Block merge if completeness <70% (configurable)

### Completeness Scoring
```
Completeness = (Completed Sections / Total Sections) × 100
- 🤖 AI-generated sections: Count as complete
- ❓ Human-required empty: Count as incomplete
- 👤 Human-written: Count as complete
```

---

## 🔄 Template Inheritance

Teams can extend base templates with custom sections:

### Base Templates (Organization-wide)
Located in `.akr/templates/` - mandatory sections defined by organization

### Team Extensions (Team-specific)
Located in `.akr/templates/team/` - additional sections required by team

**Example:**
```json
{
  "source_pattern": "src/components/**/*.tsx",
  "template": "ui-component",
  "team_template_extension": "team/ui-component-webapp1.md"
}
```

This merges organizational `ui-component.md` + team `ui-component-webapp1.md`

---

## 📊 Metrics and Reporting

Track documentation health with:
- **Coverage**: % of code files with documentation
- **Completeness**: Average completeness score across all docs
- **Freshness**: Time since last update
- **Quality**: Vale lint pass rate

---

## 🚨 Common Pitfalls to Avoid

### ❌ DON'T:
- Generate documentation without analyzing code structure
- Overwrite human-written content during updates
- Skip interview questions for business context
- Use wrong template for component type
- Ignore Vale lint errors
- Generate documentation without YAML front matter tags

### ✅ DO:
- Analyze code with Tree-sitter before generation
- Use transparency markers (🤖 ❓ 👤) consistently
- Preserve all human content during surgical updates
- Select template based on complexity and type
- Include comprehensive usage examples
- Add YAML front matter with appropriate tags
- Answer interview questions thoughtfully
- Review AI-generated content for accuracy

---

## 📚 Reference Documentation

- **Implementation Plan**: `AKR_LOCAL_MCP_IMPLEMENTATION_PLAN.md`
- **Template Manifest**: `.akr/TEMPLATE_MANIFEST.json`
- **AKR Charters**: `.akr/charters/`
- **Example Configs**: `.akr/examples/`

---

## 🆘 Support and Troubleshooting

### MCP Server Not Connecting
1. Check Python version: `python --version` (must be 3.10+)
2. Verify MCP config: `.vscode/mcp.json`
3. Reload VS Code: Ctrl+Shift+P → "Reload Window"
4. Run health check: `/docs.health-check`

### Templates Not Found
1. Check template repository: `~/.akr/templates/`
2. Sync manually: `/docs.update-templates`
3. Verify `.akr-config.json` template path

### Validation Failing
1. Check Vale configuration: `.vale.ini`
2. Verify template structure matches manifest
3. Review GitHub Actions logs
4. Run local validation: `python scripts/validate-docs.py`

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-14  
**Maintained by**: CDS - Team Hawkeye
