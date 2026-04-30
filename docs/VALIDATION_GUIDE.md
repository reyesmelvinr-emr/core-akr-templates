# Validation Guide

## Compliance Mode Graduation

A project may graduate from `pilot` to `production` compliance mode when all criteria are met:

1. Zero unresolved required `❓` markers for four consecutive weeks.
2. No documented write-bypass events in the same interval.
3. Technical lead approval recorded in project tracking.
4. `modules.yaml` updated to `compliance_mode: production`.
5. Change logged in repository tracking records.

## Emergency Rollback Procedure

If production validation causes an urgent release risk:

1. Incident owner requests temporary rollback authority from technical lead.
2. Run validator with `--fail-on never` only for approved hotfix scope.
3. Document rationale, owner, and expiry time in tracker.
4. Open remediation task to restore normal enforcement.
5. Target hotfix SLA: restore standard fail mode within 24 hours.

## Org-Wide Disable Mechanism

For systemic incidents only:

1. Standards owner approves temporary org-wide disable.
2. CI workflow updated in a dedicated emergency PR.
3. All affected repos notified with expected re-enable window.
4. Post-incident review required before reactivation.

## Local Hook Fallback

If hooks are unsupported in an execution surface, run manual validation before opening a PR:

```bash
python .akr/scripts/validate_documentation.py --changed-files "<space-separated file list>" --fail-on needs
```

If no changed-file list is available:

```bash
python .akr/scripts/validate_documentation.py --all docs/modules --fail-on needs
```

## Batch Generate Validation Behavior

When using `/akr-docs generate --batch ModuleA ModuleB ...`, validation behavior remains module-scoped:

1. Each listed module is generated independently with its own stage timings.
2. A single confirmation gate appears after draft generation completes for all listed modules.
3. Final promotion can proceed for successful modules even if other listed modules failed generation.
4. Inline validation runs per produced module document.
5. Semantic scoring (Step 11 auto-score) is skipped by default in batch mode.

Recommended follow-up for batch runs:
- Resolve validation failures module-by-module.
- Run `/akr-docs score [ModuleName]` only for modules that need score metadata before PR.

## Governance Communication Baseline (May 2026)

To reduce duplicate remediation work, teams should classify incoming findings using these dispositions:

- **Already implemented**: behavior exists and is verified in current repository assets.
- **Addressed in current release**: implemented as part of the active remediation tranche.
- **Deferred with rationale**: not implemented yet; tracked with ownership and revisit criteria.

### Assessment-Disposition Mapping

| Assessment item | Disposition | Governance communication anchor |
|---|---|---|
| `validate_business_docs.py` path mismatch | Already implemented | Script exists at `validation/scripts/validate_business_docs.py`; status-aware usage documented in this guide |
| `agentStop.json` one-liner maintenance risk | Addressed in current release | Hook now delegates to `.github/hooks/scripts/validate-docs.sh` |
| Python grouping gaps (signals, middleware, commands, admin, async tasks) | Addressed in current release | Grouping guidance updated in `.github/skills/akr-docs/scripts/akr-groupings.md` and backend instructions |
| `TEMPLATE_MANIFEST.json` placeholder metadata | Addressed in current release | Governance template entries now have non-zero estimates and explicit mandatory sections |
| Missing Python monorepo module example | Addressed in current release | Added `examples/modules.python-web-monorepo.yaml`; README cross-references updated |
| `AKR_CHARTER_UI.md` size/usability concern | Deferred with rationale | Keep current charter as canonical source during pilot; evaluate split/index approach in next documentation tranche |
| `modules.yaml` file cap (`maxItems: 8`) concern | Deferred with rationale | Keep enforced cap in pilot for context discipline; monitor and revisit post-pilot with evidence |
| Consolidation workflow dependency on multi-root workspace | Deferred with rationale | Keep current workflow model; onboarding docs continue to describe required workspace topology |
| `eval-results.json` vs `evals/benchmark.json` clarity | Addressed in current release | Added `evals/README.md` with artifact purpose matrix and data flow |
| standards version floor not enforced | Already implemented | Enforced in `.akr/schemas/modules-schema.json` and `.akr/scripts/validate_documentation.py` |

### Communication Requirement for New Assessments

When a new finding is logged, include in the PR or issue description:

1. Disposition (`already implemented`, `addressed`, `deferred`).
2. Proof reference (file path and, when relevant, command or test).
3. Owner and target milestone for deferred items.
4. Validation impact (`blocker`, `warning-only`, or `informational`).

---

## Status-Aware Validation for Consolidation Repositories

Consolidation repositories organize capabilities by lifecycle status (active/archived/new). Validation rules enforce status-specific artifact requirements.

### Status-Aware Completeness Rules

Run capability validation with enforcement of status-aware file contracts:

```bash
python validation/scripts/validate_business_docs.py --status-aware
```

The script is maintained in this repository at `validation/scripts/validate_business_docs.py` and supports `--workspace-root`, `--capability-path`, `--fail-on`, `--report-format`, and `--verbose`.

This validates:

#### Active capabilities

Must include all 9 required files:
- `index.md`
- `test-conditions.md`
- `enhancement-test-conditions.md`
- `enhancements.md`
- `backlog.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

Validation failure: CRITICAL — consolidation writes are blocked.

#### New capabilities

Must include 5 required files (excludes enhancement/backlog/traceability artifacts):
- `index.md` (may include Azure DevOps work-item links)
- `test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`

Must NOT include:
- `enhancement-test-conditions.md`
- `enhancements.md`
- `backlog.md`
- `traceability.md`

Validation failure: WARNING — file presence warnings are reported; consolidation writes may proceed if other criteria met.

#### Archived capabilities

Must include 5 required files (read-mostly historical baseline):
- `index.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

Must NOT include active enhancement or test artifacts:
- `enhancement-test-conditions.md`
- `enhancements.md`
- `backlog.md`
- `test-conditions.md` (not required; may exist for reference)

Validation failure: WARNING — archived capabilities are not blockers for consolidation writes.

### Metadata Validation by Status

All capabilities (regardless of status) must have valid front matter:

```yaml
businessCapability: <ApprovedValue>  # Must match tag-registry.json
feature: FN#####_US#####            # Required traceability format
layer: Business                     # For consolidation outputs
project_type: business-consolidation
status: draft|approved              # Document maturity, not capability lifecycle
compliance_mode: pilot|production
```

### Cross-Status Link Validation

If a new capability's `index.md` includes Azure DevOps work-item links:

- Links must be resolvable (valid work-item URLs).
- Linked work items should reference the related `businessCapability` in title or description.
- Validation warns but does not fail if links are broken (data freshness).

### Promotion Readiness Validation

Before running `capability-promote` on an active capability:

1. Verify `enhancements.md` has at least one entry with non-empty `Delivery Reference`.
2. Verify `enhancement-test-conditions.md` has corresponding planned test cases for items marked as delivered.
3. Verify the PO/TL can explicitly answer whether testing is complete for each delivered item. In the current proof-of-concept this is a human confirmation step, not an artifact-derived validation.
4. Validation reports readiness status without failing; promotion proceeds with user confirmation and may continue with deferred test-merge notes when testing execution is out of scope.

### Test Coverage Validation

For active capabilities:

- `test-conditions.md` must reference scenario IDs defined in `index.md` (validation cross-reference check).
- If `enhancement-test-conditions.md` exists, validate that enhancement test IDs use only `BTC-*`, `TTC-*`, or `RTC-*` prefixes and do not reuse baseline `TC-*` identifiers.
- Validation warns on missing scenario definitions but does not block.

### New Capability Clarify Dependency Validation (POC)

For `capability-define-clarify` flows:

- `internal_dependencies.md` entries are valid only when target capability status is `active` or `new`.
- `active` targets are verification candidates (interface check).
- `new` targets are assumption candidates (must be confirmed in clarify output).
- Any other status should be treated as a blocker to proceed.

### First-Run Suggested Additions Governance (POC)

When first-run consolidation emits a Suggested Additions Report, PO/TL must choose one governance action:

1. Accept all
2. Reject all
3. Manual selective update

Validation/reporting should treat any other action wording as non-standard and prompt explicit correction.

### Running Validation in CI

In your consolidation repository's CI workflow:

```yaml
- name: Validate capability artifacts (status-aware)
  run: |
    python validation/scripts/validate_business_docs.py \
      --status-aware \
      --fail-on production \
      --report-format json > validation-report.json

- name: Report validation failures
  if: failure()
  run: |
    echo "Validation Report:"
    cat validation-report.json
    exit 1
```

### Debugging Status-Aware Validation

To validate a specific capability:

```bash
python validation/scripts/validate_business_docs.py \
  --capability-path docs/business-capabilities/active/CourseManagement \
  --status-aware \
  --verbose
```

Validation output includes:
- Required files present/missing by status.
- Front-matter validity.
- Cross-reference checks (scenario IDs, work-item links).
- Metadata alignment with registry and templates.
