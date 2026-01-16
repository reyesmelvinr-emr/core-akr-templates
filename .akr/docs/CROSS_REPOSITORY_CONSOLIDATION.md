# Cross-Repository Documentation Consolidation

## Overview

This guide explains how to configure and use the cross-repository documentation consolidation system. This system aggregates component-level documentation from multiple repositories (UI, API, Database) to automatically generate high-level feature documentation that shows how components work together.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   UI Repo       │     │   API Repo      │     │   DB Repo       │
│                 │     │                 │     │                 │
│ Component Docs  │     │ Service Docs    │     │ Table Docs      │
│ (with tags)     │     │ (with tags)     │     │ (with tags)     │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Consolidation Service  │
                    │                        │
                    │ - Clones/updates repos │
                    │ - Parses front matter  │
                    │ - Groups by feature    │
                    │ - Maps relationships   │
                    │ - Generates docs       │
                    └────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Feature Documentation │
                    │                        │
                    │ ApplicationEditor.md   │
                    │ UserAuthentication.md  │
                    │ DocumentGeneration.md  │
                    └────────────────────────┘
```

## Prerequisites

1. **Tag Registry**: Central registry defining approved features
   - Location: `core-akr-templates/.akr/tags/tag-registry.json`
   - Must be distributed to all application repositories

2. **Tagged Documentation**: All component docs must include feature tags in front matter
   ```yaml
   ---
   feature: ApplicationEditor
   domain: ApplicationManagement
   layer: UI
   componentType: Component
   ---
   ```

3. **Configuration Files**: Each repository needs `.akr-config.json` with cross-repository settings

## Configuration

### Step 1: Repository Configuration

Each application repository needs an `.akr-config.json` file with cross-repository settings:

```json
{
  "version": "2.0.0",
  "projectInfo": {
    "name": "web-ui",
    "layer": "UI",
    "domains": ["ApplicationManagement", "UserManagement"],
    "repositoryUrl": "https://github.com/your-org/web-ui.git"
  },
  "crossRepository": {
    "enabled": true,
    "consolidationRepo": "https://github.com/your-org/documentation-hub.git",
    "registryUrl": "https://raw.githubusercontent.com/.../tag-registry.json",
    "publishFeatureDocs": true,
    "relatedRepositories": [
      {
        "name": "api-services",
        "url": "https://github.com/your-org/api-services.git",
        "layer": "API",
        "docsPath": "docs/"
      },
      {
        "name": "database",
        "url": "https://github.com/your-org/database.git",
        "layer": "Database",
        "docsPath": "docs/"
      }
    ],
    "syncSchedule": {
      "enabled": true,
      "frequency": "on-push"
    }
  }
}
```

**Configuration Options:**

- `enabled`: Enable cross-repository consolidation
- `consolidationRepo`: Repository that aggregates all documentation
- `registryUrl`: URL to centralized tag registry
- `publishFeatureDocs`: Automatically publish component docs to consolidation repo
- `relatedRepositories`: List of related repos that implement same features
- `syncSchedule`: When to sync with consolidation repo

### Step 2: Consolidation Service Configuration

Create `consolidation-config.json` for the documentation hub repository:

```json
{
  "version": "1.0.0",
  "cacheDir": "./.doc-cache",
  "tagRegistryPath": "../../core-akr-templates/.akr/tags/tag-registry.json",
  "templatePath": "../../core-akr-templates/.akr/templates/feature-consolidated.md",
  "outputDir": "./docs/features",
  
  "repositories": [
    {
      "name": "web-ui",
      "url": "https://github.com/your-org/web-ui.git",
      "branch": "main",
      "layer": "UI",
      "docsPath": "docs/"
    },
    {
      "name": "api-services",
      "url": "https://github.com/your-org/api-services.git",
      "branch": "main",
      "layer": "API",
      "docsPath": "docs/"
    },
    {
      "name": "database",
      "url": "https://github.com/your-org/database.git",
      "branch": "main",
      "layer": "Database",
      "docsPath": "docs/"
    }
  ],
  
  "validation": {
    "requireApprovedTags": true,
    "minComponentsPerFeature": 1,
    "warnOnMissingLayers": true
  }
}
```

## Usage

### Manual Generation

Generate consolidated documentation for all features:

```bash
cd akr-mcp-server/scripts/aggregation
python consolidator.py --config consolidation-config.json
```

Generate documentation for a specific feature:

```bash
python consolidator.py \
  --config consolidation-config.json \
  --feature ApplicationEditor \
  --output docs/features/
```

### Output

The consolidation service generates feature-level documentation that includes:

1. **Overview**: Number of implementing components, last update date
2. **Implementing Components**: Lists UI, API, and Database components with links
3. **Architecture Overview**: Auto-generated Mermaid diagrams showing relationships
4. **API Reference**: Aggregated from API component docs
5. **Data Model**: Entity-relationship diagrams
6. **Security Considerations**: Compiled from all components
7. **Performance Notes**: Aggregated metrics and recommendations
8. **Testing Strategy**: Combined testing approaches
9. **Change History**: Consolidated changelog

### Automated Generation

#### GitHub Actions (Scheduled)

Create `.github/workflows/consolidate-docs.yml`:

```yaml
name: Consolidate Documentation

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

jobs:
  consolidate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install pyyaml
      
      - name: Run consolidation
        run: |
          python scripts/aggregation/consolidator.py \
            --config consolidation-config.json
      
      - name: Commit updated docs
        run: |
          git config user.name "Documentation Bot"
          git config user.email "docs@company.com"
          git add docs/features/
          git commit -m "chore: update consolidated feature documentation"
          git push
```

#### On-Push Trigger

To regenerate feature docs when component docs change:

```yaml
name: Update Feature Docs

on:
  push:
    paths:
      - 'docs/**/*.md'
    branches:
      - main

jobs:
  notify-consolidation:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger consolidation workflow
        uses: peter-evans/repository-dispatch@v2
        with:
          token: ${{ secrets.PAT }}
          repository: your-org/documentation-hub
          event-type: component-docs-updated
          client-payload: |
            {
              "repository": "${{ github.repository }}",
              "ref": "${{ github.ref }}"
            }
```

## Feature Tag Requirements

For the consolidation service to work correctly, all component documentation must include these required tags in the YAML front matter:

### Required Tags

```yaml
---
feature: ApplicationEditor        # Must match tag registry
domain: ApplicationManagement     # Must match tag registry
layer: UI                        # UI, API, or Database
componentType: Component         # Component, Service, Table, etc.
status: approved                 # draft, review, approved, deprecated
---
```

### Optional Tags

```yaml
---
# ... required tags ...

# Dependencies
dependencies:
  - ApplicationService
  - DocumentRepository

# Relationships
relatedComponents:
  - ApplicationEditorToolbar
  - ApplicationEditorCanvas

# API endpoints (for API layer)
endpoints:
  - GET /api/applications/{id}
  - PUT /api/applications/{id}

# Database operations (for Database layer)
tables:
  - Applications
  - ApplicationVersions
---
```

## Relationship Detection

The consolidation service automatically detects relationships between components:

### 1. Explicit Dependencies

Components can declare dependencies in front matter:

```yaml
---
feature: ApplicationEditor
dependencies:
  - ApplicationService  # API service
  - ApplicationsTable   # Database table
---
```

### 2. Layer-Based Inference

The service automatically infers relationships based on architectural layers:

- **UI → API**: UI components call API services in the same domain
- **API → Database**: API services access database tables in the same domain

### 3. Naming Conventions

Components with similar names are linked:

- `ApplicationEditor` (UI) → `ApplicationService` (API) → `ApplicationsTable` (DB)

## Troubleshooting

### No Components Found

**Problem**: Consolidation service reports 0 components collected.

**Solutions**:
1. Verify `docsPath` in consolidation-config.json matches actual docs location
2. Check that documentation files have YAML front matter
3. Ensure front matter includes required `feature` tag
4. Run tag validation: `python validate_tags.py docs/ --verbose`

### Unapproved Tags Warning

**Problem**: Components use unapproved feature tags.

**Solutions**:
1. Check tag registry for approved features: `.akr/tags/tag-registry.json`
2. Add feature to registry if legitimate
3. Update component docs to use approved feature name
4. Run tag validation to see all issues: `python validate_tags.py --check-all docs/`

### Missing Relationships

**Problem**: Generated feature docs don't show expected component relationships.

**Solutions**:
1. Add explicit dependencies in component front matter
2. Ensure components use same `feature` tag
3. Check that domain names match across layers
4. Review naming conventions for automatic inference

### Stale Documentation

**Problem**: Feature docs not updating with component changes.

**Solutions**:
1. Check consolidation schedule in config
2. Verify GitHub Actions workflow is enabled
3. Manually trigger: `python consolidator.py --config consolidation-config.json`
4. Check cache expiry settings (may need to delete `.doc-cache/`)

## Best Practices

### 1. Consistent Feature Tagging

Use the same feature names across all layers:

```yaml
# UI Component
---
feature: ApplicationEditor
layer: UI
---

# API Service
---
feature: ApplicationEditor  # Same name
layer: API
---

# Database Table
---
feature: ApplicationEditor  # Same name
layer: Database
---
```

### 2. Declare Dependencies

Explicitly declare dependencies for better relationship mapping:

```yaml
---
feature: ApplicationEditor
dependencies:
  - ApplicationService
  - NotificationService
  - ApplicationsTable
---
```

### 3. Regular Consolidation

Run consolidation frequently to keep feature docs up-to-date:

- **Development**: On-push trigger when component docs change
- **Production**: Daily scheduled consolidation

### 4. Review Generated Docs

Generated feature docs include markers for human-required content:

```markdown
## Business Context

👤 **Human Input Required**
Explain why this feature was built and what business problem it solves.
```

Regularly review and fill in these sections.

### 5. Monitor Validation

Check tag validation results to maintain documentation quality:

```bash
python validate_tags.py --check-all docs/ --json > validation-results.json
```

## Next Steps

1. **Set up tag registry**: Follow [Tag Registry Setup Guide](TAG_REGISTRY_SETUP.md)
2. **Configure repositories**: Add `.akr-config.json` to each repository
3. **Tag existing docs**: Add feature tags to component documentation
4. **Run first consolidation**: Generate initial feature documentation
5. **Automate**: Set up GitHub Actions workflows for continuous updates

## Related Documentation

- [Tag Registry Setup](TAG_REGISTRY_SETUP.md)
- [Tag Validation Guide](TAG_VALIDATION_GUIDE.md)
- [Template Customization](TEMPLATE_CUSTOMIZATION.md)
- [GitHub Actions Integration](GITHUB_ACTIONS_INTEGRATION.md)
