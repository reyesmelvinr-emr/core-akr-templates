# Developer Reference

## HITL Role Alignment

This table aligns `humanInput.defaultRole` from `.akr/schemas/akr-config-schema.json` with expected human-in-the-loop responsibilities.

| defaultRole | HITL Level | Responsibility |
|---|---|---|
| technical_lead | Level 1 + Level 2 architecture | Validate module boundaries, architecture flow, and cross-module consistency |
| developer | Level 2 content completion | Resolve `❓` markers, verify business rules, and complete implementation-grounded sections |
| product_owner | Consolidation narrative | Refine feature narrative and business intent for cross-repo outputs |
| qa_tester | Validation and evidence review | Validate testability statements and compliance evidence quality |
| scrum_master | Process facilitation | Track unresolved items and ensure closure ownership |
| general | Fallback role | Use when no explicit role mapping is available |

## Template "Who Provides It" Vocabulary

Use these canonical role labels in all templates and generated docs:

- `technical_lead`
- `developer`
- `product_owner`
- `qa_tester`
- `scrum_master`
- `general`

Avoid mixed aliases such as "tech lead" or "PO" in structured role fields.

## priorityFilter Integration Plan (v1.1)

`humanInput.priorityFilter` is already defined in schema. Validator behavior should evolve as:

- `critical`: fail only on unresolved `❓` marked as critical.
- `important`: fail on unresolved required `❓` (current baseline behavior).
- `optional`: emit warnings only.

Until validator v1.1 lands, teams should treat unresolved required `❓` as blocking for production-mode docs.
