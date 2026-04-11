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

---

## Status-Aware Validation for Consolidation Repositories

Consolidation repositories organize capabilities by lifecycle status (active/archived/new). Validation rules enforce status-specific artifact requirements.

### Status-Aware Completeness Rules

Run capability validation with enforcement of status-aware file contracts:

```bash
python validation/scripts/validate_business_docs.py --status-aware
```

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

Must include 6 required files (excludes enhancement/backlog artifacts):
- `index.md` (may include Azure DevOps work-item links)
- `test-conditions.md`
- `limitations.md`
- `internal_dependencies.md`
- `external_dependencies.md`
- `traceability.md`

Must NOT include:
- `enhancement-test-conditions.md`
- `enhancements.md`
- `backlog.md`

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
2. Verify `enhancement-test-conditions.md` has corresponding test cases for items marked as delivered.
3. Validation reports readiness status without failing; promotion proceeds with user confirmation.

### Test Coverage Validation

For active capabilities:

- `test-conditions.md` must reference scenario IDs defined in `index.md` (validation cross-reference check).
- If `enhancement-test-conditions.md` exists, validate that scenario IDs do not duplicate baseline test IDs.
- Validation warns on missing scenario definitions but does not block.

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
