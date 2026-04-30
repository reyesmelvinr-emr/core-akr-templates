# AKR PoC Limitations and Mitigations

Date: 2026-04-27
Status: Active — pilot phase
Audience: Management reviewers, Technical Lead, Product Owner

This document catalogues the known constraints accepted for the AKR Phase 1 pilot and the mitigations in place for each. Limitations are expected in a pilot; the confidence signal for management is the presence of explicit mitigations and repeatable human checkpoints, not the absence of constraints.

---

## L1 — AI Retrieval Is Non-Deterministic

**Description:** GitHub Copilot retrieval is relevance-ranked and non-deterministic at the file level. The same prompt may retrieve different source files across sessions, and relevant files may be missed even when they exist in the indexed repository.

**Impact:** Generated module documentation may reference different evidence sets across runs. Sections with low source coverage may be incomplete or require more unknown markers than expected.

**Mitigation:**
- Human-in-the-loop review is mandatory before merge. Developers fact-check implementation-grounded content; Product Owners validate business narrative and acceptance context.
- Unknown markers (`❓`) are surfaced explicitly in generated output and must be resolved or explicitly tracked before merge — they are never hidden.
- Validation-first merge behavior blocks documents with unresolved markers above the compliance threshold.

---

## L2 — Instruction Compliance Is Probabilistic

**Description:** Copilot compliance with AKR skill instructions (section presence, format, marker usage) is probabilistic. No run is guaranteed to produce a fully compliant output on the first pass.

**Impact:** Generated documents may require one or more resolve cycles before reaching merge-ready quality. Teams should plan for a review-and-resolve loop per module.

**Mitigation:**
- The `akr-docs resolve` mode (Mode C) exists specifically to close unknown markers interactively.
- Validation script enforces structural compliance before merge. Non-compliant documents are blocked, not silently accepted.
- Pilot `compliance_mode: pilot` applies a relaxed threshold intentionally, giving teams room to build the review pattern without perfection pressure.

---

## L3 — Copilot Space Provisioned but Testing Blocked by Indexing Issues

**Description:** The AKR Copilot Space (multi-repository retrieval environment combining backend, UI, and business documentation) has been created, but testing was halted due to Copilot Space indexing issues.

**Impact:** Cross-repository capability query validation in the Space is delayed until indexing stabilizes. Teams continue using the IDE skill (`akr-docs`) for pilot execution.

**Mitigation:**
- The IDE skill workflow remains the primary Phase 1 path and is fully functional while Space indexing is unstable.
- Space setup documentation (`docs/AKR_SPACE_BOOTSTRAP.md`, `docs/AKR_SPACE_INSTRUCTION.md`) remains the source of truth for readiness checks and operating guidance.
- Space testing resumes after indexing health is confirmed by the standards owner.

---

## L4 — QA Testing Activities Are Out of POC Scope

**Description:** QA team execution activities (formal end-to-end QA validation cycles and broader QA regression testing) are not included in this PoC scope.

**Impact:** PoC outcomes emphasize documentation workflow reliability and governance behavior, not full QA validation coverage.

**Mitigation:**
- Human-in-the-loop checkpoints remain in scope for Technical Lead, Product Owner, and Developer roles.
- QA-focused test execution is deferred to the post-PoC phase and tracked as follow-on activity once PoC acceptance criteria are met.

---

## L5 — Python Monorepo Example Added (Mitigated)

**Description:** The Python all-layers monorepo example is now available at `examples/modules.python-web-monorepo.yaml`.

**Impact:** Python teams now have a concrete monorepo modules manifest reference and no longer need to bootstrap from API-only module examples.

**Mitigation:**
- `examples/modules.python-web-monorepo.yaml` provides a baseline for mixed API/UI/shared/infrastructure Python monorepo grouping.
- `examples/akr-config-monorepo.json` remains the configuration starting point for path mappings and package-level docs output.
- `README.md` now links both Python API and Python monorepo module examples.

---

## L6 — Evaluation Cases Not Yet Executed

**Description:** The evaluation case matrix (`docs/references/AKR_EVAL_CASES.md`) defines 10 comparison scenarios for baseline Copilot vs AKR Space behavior but has not been run against live pilot output.

**Impact:** Quantitative accuracy metrics (mode declaration rate, capability declaration rate, conflict detection rate) are targets only at this stage.

**Mitigation:**
- Eval cases are ready to run once the Space is provisioned (see L3).
- Phase 1 success criteria (see `docs/AKR_MANAGEMENT_REVIEW_PILOT_PACKAGE.md` section 5) are process-based and do not depend on eval case completion for the initial pilot milestone.

---

## Summary Table

| ID | Limitation | Phase blocked | Mitigation strength |
|---|---|---|---|
| L1 | Non-deterministic retrieval | None — HITL compensates | High |
| L2 | Probabilistic instruction compliance | None — validation blocks bad merges | High |
| L3 | Space indexing instability after provisioning | Space query validation | Medium — IDE skill covers Phase 1 |
| L4 | QA testing activities out of scope | QA execution and regression validation | Medium — deferred post-PoC |
| L5 | Python monorepo example availability gap | None — mitigated with baseline example | Low |
| L6 | Eval cases not yet run | Post-Space provisioning | Medium — process metrics cover Phase 1 |
