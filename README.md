# Core AKR Templates Repository

Centralized templates, standards, and skill assets for AKR documentation workflows.

## Overview

core-akr-templates is the standards repository for documenting application codebases and aligning documentation with business context. It provides reusable templates, governance contracts, validation rules, and distributed Copilot skill assets so teams can produce documentation that stays useful over time.

This repository is designed to support:

- Practical module-level documentation close to code
- Cross-repo feature consolidation for business visibility
- Governance and compliance controls that scale
- Human-in-the-loop review where accountability is required

## Documentation Retrieval Strategy

Documentation in this repository is organized into three tiers to optimize Copilot retrieval, team onboarding speed, and context efficiency:

- **Core Include Set** (always loaded for Copilot): README.md, charter templates, and copilot-instructions. Ensures AI agents can answer module documentation and generation queries without secondary lookups.
- **Conditional/Secondary** (loaded when governance, architecture, compliance, or onboarding questions arise): TEAM_STARTUP_ONBOARDING_GUIDE.md, VALIDATION_GUIDE.md, AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md, DEVELOPER_REFERENCE.md, MIGRATION_GUIDE.md.
- **Reference/Optional** (linked for deep dives, strategic context, or historical reference): AKR_AI_CODEBASE_UNDERSTANDING_FEEDBACK.md, planning and workshop materials, skill distribution details.

**For Copilot/AI Retrieval:** The repository's Core Include Set is optimized for Copilot chat interactions. When Copilot agents answer questions about module documentation, template generation, or governance workflows, they pull from the Core set by default. Request Secondary or Reference documents explicitly if you need governance policy deep dives or historical context.

## Start Here

New to AKR? Start with the team startup guide:

- [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](docs/TEAM_STARTUP_ONBOARDING_GUIDE.md) — Step-by-step setup for Technical PO/TL, Non-Technical PO, and Source Repo Developer roles. Covers both local-workspace and source-evidence consolidation modes.

High-level assessment documents:

- [docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md](docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md)
- [docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md](docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md)
- [docs/AKR_SKILLS_DISTRIBUTION_APPLICATION_VS_CONSOLIDATION.md](docs/AKR_SKILLS_DISTRIBUTION_APPLICATION_VS_CONSOLIDATION.md)


## Repository At a Glance

### Core (Always Loaded for Copilot)
- [copilot-instructions](copilot-instructions) — Condensed charter guidance used by AKR workflows for both backend and UI modules
- [.akr/charters](.akr/charters) — Canonical charter templates that define module documentation standards

### Conditional (Load on Onboarding/Governance/Architecture/Compliance Questions)
- [.akr](.akr) — Complete templates, schemas, validation scripts, standards, and Vale rules
- [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](docs/TEAM_STARTUP_ONBOARDING_GUIDE.md) — Role-based setup paths for all team types; primarily needed during initial onboarding
- [docs/VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md) — Compliance gates, review escalation, and quality checks
- [docs/DEVELOPER_REFERENCE.md](docs/DEVELOPER_REFERENCE.md) — HITL role alignment and review responsibilities
- [docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md](docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md) — Governance model and standards alignment
- [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) — Runtime and workspace execution models

### Reference/Optional (Strategic Context and Distribution Details)
- [.github/skills](.github/skills) — Distributed skill assets such as akr-docs and akr-interview
- [.github/workflows](.github/workflows) — Skill and bundle distribution automation
- [examples/onboarding](examples/onboarding) — Onboarding seeds for consuming repositories
- [docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md](docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md) — Feature overview and vision
- [docs/AKR_SKILLS_DISTRIBUTION_APPLICATION_VS_CONSOLIDATION.md](docs/AKR_SKILLS_DISTRIBUTION_APPLICATION_VS_CONSOLIDATION.md) — Skill strategy and distribution patterns


## How Teams Use AKR

### Core Workflow (All Teams)

1. **Onboarding** — Run `distribute-onboarding-bundle.yml` once per repository to seed local configuration and role context.
2. **Module Documentation** — Use the `akr-docs` skill to generate module-level documentation aligned with AKR templates and business context.
3. **Review and Governance** — Apply validation rules and HITL review gates via `compliance_mode` (pilot → production).

Full step-by-step setup for Technical PO/TL, Non-Technical PO, and Source Repo Developer roles is in [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](docs/TEAM_STARTUP_ONBOARDING_GUIDE.md).

### Application Teams (Source Repositories)

Run the core workflow above, then:
- Execute `distribute-skill.yml` to install the `akr-docs` and `akr-interview` skill bundles.
- Generate and maintain module documentation in the `docs/modules/` directory using the `akr-docs` skill.

### Consolidation Teams (Business Aggregation)

Run the core workflow, then:
- Execute `distribute-business-skill.yml` to install the `akr-business-consolidation` skill bundle.
- Use the `sync-source-evidence.yml` workflow to pull and aggregate source module documentation into capability artifacts.
- For advanced governance questions, consult [docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md](docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md).

## Governance, Compliance, and Human-in-the-Loop

AKR treats governance and review accountability as built-in workflow behavior. Versioned standards are maintained centrally here and distributed without duplicating policy ownership. Compliance mode supports progressive adoption from pilot to production.

- Validation rules and escalation paths: [docs/VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md)
- HITL role alignment and review responsibilities: [docs/DEVELOPER_REFERENCE.md](docs/DEVELOPER_REFERENCE.md)
- Governance gates and joint PO/TL approval model: [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](docs/TEAM_STARTUP_ONBOARDING_GUIDE.md)

## Migration and Drift Prevention


Use [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) for the current runtime-fetch and workspace-distributed execution model. CI runners fetch canonical assets at runtime, while application repositories receive only the distributed skill and hook bundle needed for local execution.

## Maintainer Workflows

- Skill distribution (application repos): [.github/workflows/distribute-skill.yml](.github/workflows/distribute-skill.yml)
- Skill distribution (consolidation repos): [.github/workflows/distribute-business-skill.yml](.github/workflows/distribute-business-skill.yml)
- Onboarding bundle distribution: [.github/workflows/distribute-onboarding-bundle.yml](.github/workflows/distribute-onboarding-bundle.yml)
- Registered repositories:
  - [.github/registered-repos.yaml](.github/registered-repos.yaml) — application repos
  - [.github/registered-business-repos.yaml](.github/registered-business-repos.yaml) — consolidation repos


