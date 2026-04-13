# AS-PMO-Customer-Visibility - AKR Onboarding Guide

**Project:** AS-PMO-Customer-Visibility (Supply Chain Optimization - Customer Visibility)  
**Date Created:** 2026-04-13  
**Status:** Feature Branch Testing  
**Repository:** SCO/AS-PMO-Customer-Visibility

---

## Overview

The AS-PMO-Customer-Visibility application is a Django web application that provides customers with unified shipment tracking across Emerson's Supply Chain Optimization (SCO) cross-dock network. This onboarding guide configures the project for AKR documentation generation and consolidation.

### Project Scope

- **Type:** Backend Web Application (Django)
- **Primary Language:** Python 3.8+
- **Framework:** Django 3.2.3
- **Cloud Integration:** Azure Storage & Azure AD
- **Testing Framework:** pytest, pytest-django, pytest-cov

---

## Configuration Files Created

### 1. AKR Configuration (`akr-config-customer-visibility.json`)

**Location:** `examples/akr-config-customer-visibility.json`

This file defines:
- **Project metadata** — name, type, description, and business domains
- **Documentation patterns** — which Python files to include/exclude
- **Component mappings** — how source files map to documentation modules
- **Team structure** — roles and responsibilities (requires email update)
- **Technology stack** — Django, pytest, Azure services
- **Validation rules** — documentation standards and compliance thresholds

**Key Mappings:**
- `app/views.py` → HTTP request handlers
- `app/endpoints.py` → RESTful API endpoints
- `app/forms.py` → Form validation and input handling
- `app/helpers.py` → Utility functions and business logic
- `app/middlewares.py` → Security and logging middleware
- `CusVis/azure.py` → Azure Storage integration
- `CusVis/settings.py` → Django configuration

### 2. Module Structure (`modules.customer-visibility.yaml`)

**Location:** `examples/modules.customer-visibility.yaml`

Defines logical modules and their business capabilities:
- **Shipment Tracking** — core tracking functionality across carriers
- **User Interface Layer** — customer-facing web interface
- **Data Integration** — OTM and Azure Storage integration
- **Application Configuration** — Django settings and routing

Each module includes:
- Component file references
- Role classifications
- Business capability tags
- KPI tracking points

---

## Quick Start: Generate Documentation

### Step 1: Verify Source Repository Access

Ensure you have access to the SCO repository:

```bash
# Navigate to the customer visibility project
cd "C:\Users\E1481541\OneDrive - Emerson\Documents\CDS - Team Hawkeye\SCO\AS-PMO-Customer-Visibility"

# Verify structure
ls -la app/
ls -la CusVis/
```

Expected files:
- ✅ `app/views.py`
- ✅ `app/endpoints.py`
- ✅ `app/forms.py`
- ✅ `app/helpers.py`
- ✅ `app/middlewares.py`
- ✅ `CusVis/settings.py`
- ✅ `CusVis/azure.py`

### Step 2: Use the AKR Configuration

**In VS Code (core-akr-templates workspace):**

1. Open the AKR documentation skill:
   - Use `/akr-docs groupings` to propose module groupings
   - Use `/akr-docs generate [ModuleName]` to generate documentation for a specific module

2. Reference the configuration files:
   ```
   Configuration file: examples/akr-config-customer-visibility.json
   Module manifest:    examples/modules.customer-visibility.yaml
   ```

3. Expected outputs will be generated in:
   ```
   AS-PMO-Customer-Visibility/docs/
   ```

### Step 3: Testing Documentation Output

After generating documentation, verify:

```bash
# Check documentation structure
find docs/ -name "*.md" -type f | sort

# Validate markdown
vale docs/**/*.md  # Requires Vale linter setup

# View generated artifacts
code docs/modules/
```

---

## Module Documentation Checklist

### Shipment Tracking Module
- [ ] `app/views.py` — HTTP request handlers documented
- [ ] `app/endpoints.py` — API endpoint contracts documented
- [ ] `app/helpers.py` — Business logic and data transformation functions documented

### User Interface Layer
- [ ] `app/forms.py` — Form validation logic documented
- [ ] `app/middlewares.py` — Middleware security and logging documented

### Data Integration
- [ ] `CusVis/azure.py` — Azure Storage integration pattern documented
- [ ] `app/constants.py` — Status codes and configuration constants documented

### Configuration
- [ ] `CusVis/settings.py` — Django settings and initialization documented
- [ ] `CusVis/urls.py` — Project-level URL routing structure documented
- [ ] `app/urls.py` — App-level endpoint routing documented

---

## Team Configuration

**Current Role Assignments (update as needed):**

| Role | Email | Responsibility |
|---|---|---|
| **Technical Lead** | `team-lead@emerson.com` | Validate architecture and module boundaries |
| **Developers** | `developer1@emerson.com`<br>`developer2@emerson.com` | Resolve documentation markers, implement details |
| **Product Owner** | `po@emerson.com` | Refine business narrative and feature descriptions |
| **QA/Testing** | `qa@emerson.com` | Validate testability and compliance evidence |
| **Scrum Master** | `scrum-master@emerson.com` | Track unresolved items and ensure closure |

**Update these emails in `akr-config-customer-visibility.json` to match your team.**

---

## Validation & Compliance

The configuration enforces:

| Setting | Value | Purpose |
|---|---|---|
| `required_sections` | `true` | All required documentation sections must be present |
| `transparency_markers` | `true` | ❓ markers in docs must be resolved before commit |
| `completeness_threshold` | `75%` | Documentation must reach 75% completeness for compliance |
| `vale_linting` | `true` | Style and grammar validation via Vale |
| `compliance_mode` | `pilot` | Pilot mode allows flexibility during initial rollout |

---

## Consolidation & Cross-Repository Linking

This configuration supports AKR consolidation workflows, enabling:

1. **Business Capability Grouping** — Link documentation to approved business capabilities
2. **Cross-Repository References** — Link UI documentation to this API documentation
3. **Unified Impact Analysis** — Trace features across multiple repositories
4. **Documentation Inheritance** — Share and extend module templates

### Business Capabilities Defined

- **ShipmentTracking** — Real-time visibility across SCO cross-dock network
- **CustomerVisibility** — Customer-facing web platform
- **DataIntegration** — OTM and cloud storage integration

---

## Technology Stack & Dependencies

```plaintext
Backend Framework:     Django 3.2.3
Language Runtime:      Python 3.8+
Cloud Services:        Azure Storage Blob, Azure AD Authentication
Testing Suite:         pytest 6.2.4, pytest-django 4.4.0, pytest-cov 2.12.1
Code Quality:          pylint 2.8.2, Coverage 5.5
Documentation:         AKR templates, Markdown, Vale linting
```

**See:** `requirements.txt` in the customer visibility project for full dependency list.

---

## Next Steps

1. **Run documentation generation** using `/akr-docs generate [Module]`
2. **Review generated documentation** in `docs/modules/`
3. **Resolve transparency markers** marked with ❓
4. **Validate against AKR standards** using validation scripts
5. **Commit documentation** to feature branch
6. **Create pull request** to core-akr-templates for review and consolidation testing

---

## Troubleshooting

### Documentation Not Generating?

- Verify file paths in component mappings match actual project structure
- Ensure Python files are not in the exclude patterns
- Check that template references exist in core-akr-templates

### Validation Errors?

- Run `/akr-docs resolve [filename]` to address ❓ markers
- Ensure all required sections from templates are present
- Check Vale linting rules in `.akr/.vale.ini`

### Need Help?

Refer to:
- `docs/DEVELOPER_REFERENCE.md` — Role alignment and HITL guidance
- `docs/TEAM_STARTUP_ONBOARDING_GUIDE.md` — Team setup and workflow
- `docs/VALIDATION_GUIDE.md` — Documentation quality standards

---

## References

- **Project Repository:** `SCO/AS-PMO-Customer-Visibility`
- **AKR Templates:** `core-akr-templates`
- **Configuration Files:** `examples/akr-config-customer-visibility.json`, `examples/modules.customer-visibility.yaml`
- **Feature Branch:** `feature/onboard-customer-visibility`
