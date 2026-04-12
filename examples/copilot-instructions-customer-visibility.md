# AS-PMO-Customer-Visibility - Copilot Instructions

**For:** Documentation generation and AKR onboarding support  
**Project:** AS-PMO-Customer-Visibility (SCO Customer Visibility Platform)  
**Configuration:** `examples/akr-config-customer-visibility.json`

---

## AKR Documentation Workflow

When documenting the AS-PMO-Customer-Visibility application, use the AKR documentation skill as follows:

### 1. Propose Module Groupings

```
/akr-docs groupings
```

This will:
- Analyze the project structure (app/, CusVis/)
- Propose logical module groupings based on component mappings
- Suggest business capability alignment
- Ask for confirmation of groupings before proceeding

**Expected modules:**
- Shipment Tracking (core business logic)
- User Interface Layer (presentation)
- Data Integration (Azure/OTM integration)
- Application Configuration (Django setup)

### 2. Generate Module Documentation

For each approved module:

```
/akr-docs generate [ModuleName]
```

Examples:
```
/akr-docs generate ShipmentTracking
/akr-docs generate UserInterface
/akr-docs generate DataIntegration
/akr-docs generate Configuration
```

This will:
- Extract source files matching component mappings
- Apply the `lean_baseline_service_template_module.md` template
- Generate documentation in the appropriate `docs/` subdirectory
- Insert ❓ transparency markers for required human input

### 3. Resolve Transparency Markers

After generation, resolve marked sections:

```
/akr-docs resolve [filename]
```

Example:
```
/akr-docs resolve docs/modules/shipment-tracking.md
```

This will:
- Identify all ❓ markers in the document
- Guide you through required sections needing completion
- Suggest how to fill in business context, design decisions, and trade-offs
- Validate resolved content against documentation standards

---

## Key Project Context

### Django Application Structure

```
AS-PMO-Customer-Visibility/
├── app/                          # Django app with business logic
│   ├── views.py                  # HTTP request handlers
│   ├── endpoints.py              # RESTful API endpoints
│   ├── forms.py                  # Form validation
│   ├── helpers.py                # Utility functions
│   ├── middlewares.py            # Request/response middleware
│   ├── constants.py              # Configuration constants
│   ├── urls.py                   # App-level routing
│   └── static/, templates/       # [EXCLUDED] Static assets
│
├── CusVis/                       # Django project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Project-level routing
│   ├── azure.py                  # Azure Storage integration
│   ├── wsgi.py                   # WSGI application entry
│   └── asgi.py                   # ASGI application entry
│
├── manage.py                     # [EXCLUDED] Django management
├── requirements.txt              # Python dependencies
└── docs/                         # [OUTPUT] Generated documentation
```

### Excluded Files (Not Documented)

These files are automatically excluded from documentation generation:

- `manage.py` — Django CLI tool
- `settings.py` — Django configuration (internal reference)
- `wsgi.py`, `asgi.py` — Application servers
- `**/static/**`, `**/templates/**` — Client-side assets
- `**/test*.py`, `**/*_test.py` — Test files
- `**/migrations/**` — Database migrations

### Key Dependencies

- **Django** 3.2.3 — Web framework
- **pytest** 6.2.4 + **pytest-django** — Testing
- **Azure Storage Blob** — Cloud storage
- **Azure AD** — Authentication

---

## Module-Specific Guidance

### Shipment Tracking Module

**Files:**
- `app/views.py` — HTTP view handlers for tracking UI
- `app/endpoints.py` — REST API endpoints for shipment queries
- `app/helpers.py` — Core tracking and data transformation logic

**Documentation Focus:**
- How does tracking work across multiple carriers?
- What is the flow from OTM to customer visibility?
- How are cross-dock legs aggregated?
- What tracking statuses are supported?

**Key Questions to Address:**
- ❓ What data structures represent a shipment?
- ❓ How are tracking statuses determined from OTM?
- ❓ What is the polling/sync frequency for updates?
- ❓ How are errors and failures handled?

### User Interface Layer

**Files:**
- `app/forms.py` — User input validation
- `app/middlewares.py` — Request/response processing

**Documentation Focus:**
- What forms does the customer use for tracking?
- What validation rules apply to tracking queries?
- What security middleware is in place?
- How is user session management implemented?

**Key Questions to Address:**
- ❓ What are valid reference number formats?
- ❓ What is the rate limiting policy?
- ❓ How are CORS policies configured?
- ❓ What audit logging is performed?

### Data Integration Module

**Files:**
- `CusVis/azure.py` — Azure Storage integration
- `app/constants.py` — Configuration constants

**Documentation Focus:**
- How is shipment data persisted in Azure?
- What are the storage account patterns?
- What constants control tracking behavior?
- How is data refreshed from OTM?

**Key Questions to Address:**
- ❓ What is the data schema in Azure Storage?
- ❓ How are cache refresh cycles configured?
- ❓ What status codes and reason codes are defined?
- ❓ What is the data retention policy?

### Configuration Module

**Files:**
- `CusVis/settings.py` — Django settings
- `CusVis/urls.py` — Project-level routing
- `app/urls.py` — App-level routing

**Documentation Focus:**
- What are the key Django settings for this app?
- How are Azure services configured?
- What is the URL routing structure?
- What middleware stack is active?

**Key Questions to Address:**
- ❓ What environment variables control behavior?
- ❓ How are Azure credentials managed (MSI/connection strings)?
- ❓ What are the top-level URL patterns?
- ❓ What is the middleware processing order?

---

## Business Context

### High-Level Purpose

Emerson's Supply Chain Optimization (SCO) program controls transportation routing and carrier selection. Shipments may transit through multiple carriers and cross-dock facilities. Customers previously only received information for one leg of their shipment. This application provides **unified, end-to-end tracking** from origin to final destination.

### Business Domains

- **supply-chain-optimization** — Part of SCO program
- **customer-visibility** — Customer-facing tracking
- **shipment-tracking** — Real-time shipment monitoring

### Success Metrics

- Real-time visibility across all carriers
- Support for multi-leg shipments (cross-docks)
- Unified status reporting to customers
- Reduced customer inquiries about shipment status

---

## Documentation Standards

All module documentation must include:

| Section | Required | Purpose |
|---|---|---|
| Overview | ✅ | What does this module do? |
| Responsibilities | ✅ | What business functions does it handle? |
| Key Entities | ✅ | What data structures or domain models? |
| External Integrations | ✅ | What external systems does it interact with? |
| Known Limitations | ✅ | What is not supported or out of scope? |
| Security Considerations | ✅ | What security measures are in place? |
| Performance Characteristics | ⚠️ | Scalability, caching, and performance notes |
| Future Enhancements | ⚠️ | Planned improvements or refactoring |

**Legend:** ✅ Required | ⚠️ Recommended | ❌ Not applicable

---

## Validation & Quality Assurance

### Before Committing Documentation

1. **Resolve all ❓ markers** — No transparency markers should remain
2. **Run Vale linting** — Check grammar and style
3. **Verify code references** — Ensure all code snippets are accurate
4. **Validate business context** — Confirm descriptions align with team understanding
5. **Check business capability tags** — All modules must be tagged with approved capabilities

### Completeness Threshold

Documentation must be **≥75% complete** before merge approval.

Use:
```
/akr-docs score [filename]
```

To assess current completion percentage.

---

## Cross-Repository Linking (Future)

When this module is merged to main, it can be linked in consolidation workflows:

```json
{
  "crossRepository": [
    {
      "type": "UI",
      "layer": "UI",
      "repository_name": "customer-visibility-ui",
      "description": "React.js frontend for shipment tracking"
    }
  ]
}
```

This enables:
- Tracing features across backend API and frontend UI
- Unified impact analysis for business capability changes
- Cross-repository documentation validation

---

## Support & Troubleshooting

### Documentation Not Generating?

- Verify file paths in `akr-config-customer-visibility.json` component mappings
- Ensure Python source files contain docstrings or comments
- Check that files aren't in the exclude patterns

### Template Not Found?

- Verify `lean_baseline_service_template_module.md` exists in core-akr-templates
- Check template path references in component mappings
- Ensure template inheritance is configured correctly

### Questions About Business Logic?

- Refer to `SCO/AS-PMO-Customer-Visibility/README.md`
- Check project design documentation in customer-visibility.fpr
- Ask technical lead or product owner from the team contacts

---

## References

- **Project:** `SCO/AS-PMO-Customer-Visibility`
- **Configuration:** `examples/akr-config-customer-visibility.json`
- **Module Manifest:** `examples/modules.customer-visibility.yaml`
- **Onboarding Guide:** `examples/ONBOARDING_CUSTOMER_VISIBILITY.md`
- **AKR Reference:** `docs/DEVELOPER_REFERENCE.md`
- **Validation Guide:** `docs/VALIDATION_GUIDE.md`
