# capability-relationship-mapping

## Purpose

Produce a textual relationship map for a selected capability across layers and dependencies.

## Inputs

- Existing capability artifacts in consolidation repository
- Source module documentation references
- Internal and external dependency evidence

## Required metadata checks

Validate metadata using `SKILL.md` section **Required Metadata and Governance**.
Do not write output if any metadata check fails; report failures with `❓`.

## Required checks

- Distinguish internal vs external dependencies.
- Keep explanation business-readable for PO/QA/TL audiences.
- Use text/ASCII only (no Mermaid).

## Outputs

- Cross-layer relationship summary
- Dependency impact map
- Integration risk notes and open gaps
