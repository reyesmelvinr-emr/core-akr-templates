# Core AKR Templates Repository

Centralized templates, standards, and skill assets for AKR documentation workflows.

## Overview

core-akr-templates is the standards repository for documenting application codebases and aligning documentation with business context. It provides reusable templates, governance contracts, validation rules, and distributed Copilot skill assets so teams can produce documentation that stays useful over time.

This repository is designed to support:

- Practical module-level documentation close to code
- Cross-repo feature consolidation for business visibility
- Governance and compliance controls that scale
- Human-in-the-loop review where accountability is required



## Start Here

New to AKR? Start with the team startup guide:

- [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](docs/TEAM_STARTUP_ONBOARDING_GUIDE.md) — Step-by-step setup for Technical PO/TL, Non-Technical PO, and Source Repo Developer roles. Covers both local-workspace and source-evidence consolidation modes.

High-level assessment documents:

- [docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md](docs/AKR_SOLUTION_FEATURES_AND_FUNCTIONALITY.md)
- [docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md](docs/AKR_ARCHITECTURE_MODEL_AND_GOVERNANCE.md)
- [docs/AKR_SKILLS_DISTRIBUTION_APPLICATION_VS_CONSOLIDATION.md](docs/AKR_SKILLS_DISTRIBUTION_APPLICATION_VS_CONSOLIDATION.md)


## Repository At a Glance

- [.akr](.akr)
  - Canonical templates, schemas, validation scripts, standards, and Vale rules
- [copilot-instructions](copilot-instructions)
  - Condensed charter guidance used by AKR workflows
- [.github/skills](.github/skills)
  - Distributed skill assets such as akr-docs and akr-interview
- [examples/onboarding](examples/onboarding)
  - Onboarding seeds for consuming repositories
- [templates](templates)
  - Historical and compatibility templates retained for transition support
- [planning/implementation_plans](planning/implementation_plans)
  - Program phases, gates, and execution plans

## How Teams Use AKR

AKR supports two team types: source (application) teams that produce module-level documentation, and business consolidation teams that aggregate documentation into capability artifacts. Both team types have distinct skill surfaces, onboarding workflows, and configuration.

Full step-by-step setup for all roles — Technical PO/TL, Non-Technical PO, and Source Repo Developer — is in [docs/TEAM_STARTUP_ONBOARDING_GUIDE.md](docs/TEAM_STARTUP_ONBOARDING_GUIDE.md).

Key distribution entry points:

- Application teams: run `distribute-onboarding-bundle.yml` once per repo, then `distribute-skill.yml` to install the `akr-docs` and `akr-interview` skill bundles.
- Consolidation teams: run `distribute-business-skill.yml` to install the `akr-business-consolidation` skill bundle and the `sync-source-evidence.yml` workflow.

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


