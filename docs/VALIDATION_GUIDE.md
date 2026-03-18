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
