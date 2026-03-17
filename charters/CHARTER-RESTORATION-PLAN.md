# Charter Restoration Plan

**Maintained by:** Standards Team
**Last Updated:** [Date of Phase 0 completion]
**Related:** Phase 0 Deliverable - Charter Compression

## Purpose

This document records what was removed from each condensed charter during
Phase 0 compression, in what order it should be restored as context windows
grow, and what conditions trigger a restoration review.

It exists so future maintainers can restore charter fidelity without
reconstructing removal decisions from memory.

## Restoration Priority Order

| Priority | Content Category | Charter | Source Section | Approx Tokens | Restore When Condition |
|---|---|---|---|---|---|
| 1st | Worked examples (per section) | Backend | AKR_CHARTER_BACKEND.md §[N] | ~800 | Per-pass budget supports +800 tokens reliably |
| 1st | Worked examples (per section) | UI | AKR_CHARTER_UI.md §[N] | ~800 | Same condition |
| 2nd | Explanatory rationale for rules | Backend | §[N] | ~1,200 | Per-pass budget supports +2,000 tokens total |
| 2nd | Explanatory rationale for rules | UI | §[N] | ~1,200 | Same condition |
| 3rd | Multi-section pass consolidation | All | N/A (structural) | N/A | Full charter per section reliably in one pass |
| Final | Single-pass full charter loading | All | Entire charter | ~11,000 | 30K+ token single-pass confirmed |

## Trigger Conditions for Restoration Review

A restoration review is triggered when ANY of the following are observed:

- Model context window capacity confirmed at >=50K tokens effective for structured output
  (evidence: benchmark.json SSG avg-total-seconds drops below 600 seconds for large modules)
- New model release with documented context handling improvements >50% capacity increase
- SKILL-COMPAT.md "Future Enhancement Paths" dynamic resource hydration row becomes actionable
- SSG avg-total-seconds for standard modules consistently below 600 seconds (10 minutes)

## Restoration Process

1. Identify which content category to restore (use priority order above)
2. Author a new version of the relevant condensed charter with the restored content
3. Re-run tokenizer check (tiktoken GPT-4 encoder + GPT-4o encoder)
4. Run full eval suite (evals/cases/) against new charter
5. If pass rates hold or improve: merge; bump standards_version minor version
6. Update this document: mark restored category as "RESTORED in v[version]"

## Current Status

| Content Category | Charter | Status | Version Restored |
|---|---|---|---|
| Worked examples | Backend | Removed in v1.0.0 | - |
| Worked examples | UI | Removed in v1.0.0 | - |
| Explanatory rationale | Backend | Removed in v1.0.0 | - |
| Explanatory rationale | UI | Removed in v1.0.0 | - |
