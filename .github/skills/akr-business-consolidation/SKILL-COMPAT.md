# SKILL-COMPAT Matrix

Skill: akr-business-consolidation
Version: v1.0.0
Last updated: 2026-04-10

## Model Compatibility Matrix
| Model | Pass Rate | Known Issues | Workaround |
|---|---|---|---|
| claude-sonnet-4-6 | TBD | TBD | Use explicit mode invocation and validate required artifact set |
| gpt-5.4 | TBD | TBD | Validate outputs with repository validation scripts before PR |

## Invocation Surface Matrix
| Surface | Supported | Notes |
|---|---|---|
| coding-agent | Yes | Preferred for deterministic multi-file updates |
| custom-agent | Yes | Use explicit mode naming |

## Governance Notes

- Consolidation outputs are business-facing and should avoid implementation-level narrative.
- Preserve repository-owned `.github/copilot-instructions.md`.
- Registry alignment is mandatory before writes.
