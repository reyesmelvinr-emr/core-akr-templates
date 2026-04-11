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

## How Application Teams Use AKR

1. Onboard repository scaffolds from [examples/onboarding](examples/onboarding).
2. Install distributed skill bundles through [.github/workflows/distribute-skill.yml](.github/workflows/distribute-skill.yml).
3. Run the akr-docs workflow:
  - /akr-docs groupings
  - /akr-docs generate <ModuleName>
  - /akr-docs resolve <ModuleDocFile>
  - /akr-docs cache-status
  - /akr-docs update-cache
4. Validate documentation in CI using [.akr/workflows/validate-documentation.yml](.akr/workflows/validate-documentation.yml) and [docs/VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md).


Use `cache-status` and `update-cache` to maintain repository-local fallback assets in `.akr/cache/` when remote GitHub access is unstable.

## Governance, Compliance, and Human-in-the-Loop

AKR treats governance and review accountability as built-in workflow behavior.

- Governance
  - Versioned standards and schema contracts are maintained centrally in this repository.
  - Distribution workflows propagate execution assets without duplicating policy ownership.

- Compliance
  - Compliance mode supports progressive adoption from pilot to production.
  - Validation behavior and escalation paths are defined in [docs/VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md).

- Human-in-the-loop
  - Technical leads, developers, product owners, and QA roles have explicit review responsibilities.
  - Role mapping and closure expectations are defined in [docs/DEVELOPER_REFERENCE.md](docs/DEVELOPER_REFERENCE.md).

## Migration and Drift Prevention


Use [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) for the current runtime-fetch and workspace-distributed execution model. CI runners fetch canonical assets at runtime, while application repositories receive only the distributed skill and hook bundle needed for local execution.

## Maintainer Workflows

- Skill distribution: [.github/workflows/distribute-skill.yml](.github/workflows/distribute-skill.yml)
- Onboarding bundle distribution: [.github/workflows/distribute-onboarding-bundle.yml](.github/workflows/distribute-onboarding-bundle.yml)
- Registered repositories:
  - [.github/registered-repos.yaml](.github/registered-repos.yaml)
  - [.github/registered-business-repos.yaml](.github/registered-business-repos.yaml)


