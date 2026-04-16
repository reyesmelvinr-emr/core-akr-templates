# GitHub Actions Cost Monitoring for AKR Documentation

## Overview

This document provides current guidance for monitoring and controlling GitHub Actions costs for AKR documentation validation workflows.

The guidance below was refreshed against the current GitHub billing and Actions documentation in April 2026. The earlier January 2026 assumptions in this file were partially outdated.

## Current Billing Model (April 2026)

### Standard GitHub-Hosted Runner Rates

For AKR documentation validation, the relevant default runner is usually standard `ubuntu-latest`, which maps to a Linux 2-core x64 hosted runner.

| Runner Type | SKU | Current Cost per Minute | Notes |
|-------------|-----|-------------------------|-------|
| Linux 1-core (x64) | `actions_linux_slim` | $0.002 | Not the typical default for AKR validation |
| **Linux 2-core (x64)** | `actions_linux` | **$0.006** | Typical `ubuntu-latest` standard runner |
| Linux 2-core (arm64) | `actions_linux_arm` | $0.005 | Lower-cost ARM option where compatible |
| Windows 2-core (x64) | `actions_windows` | $0.010 | Higher cost than Linux |
| macOS 3-core or 4-core | `actions_macos` | $0.062 | Very high cost; avoid for doc validation |

### Important Billing Notes

- GitHub rounds each job's usage up to the nearest whole minute.
- Standard GitHub-hosted runners are free for public repositories.
- Self-hosted runners do not consume GitHub-hosted runner minutes.
- Larger runners are always billed separately, even for public repositories, and included minutes do not apply to them.
- Usage is billed to the repository owner, not the person who triggered the workflow.

### Included Minutes and Storage by Plan

For private repositories, included usage depends on the owner account plan.

| Plan | Included Storage | Included Standard Runner Minutes per Month | Included Cache Storage per Repository |
|------|------------------|--------------------------------------------|---------------------------------------|
| GitHub Free | 500 MB | 2,000 | 10 GB |
| GitHub Pro | 1 GB | 3,000 | 10 GB |
| GitHub Free for organizations | 500 MB | 2,000 | 10 GB |
| GitHub Team | 2 GB | 3,000 | 10 GB |
| GitHub Enterprise Cloud | 50 GB | 50,000 | 10 GB |

### Storage Notes

- Included Actions storage is shared with GitHub Packages.
- Storage billing accrues hourly over the billing cycle, not just from the current amount stored at the end of the month.
- Deleting artifacts reduces future storage accrual, but it does not erase storage already accrued earlier in the same billing cycle.
- Additional cache storage is billed at $0.07 per GiB per month when usage exceeds the included amount.

## AKR Cost Estimate

### Assumptions for This Repository Pattern

- Workflow: `validate-documentation.yml`
- Runner: standard `ubuntu-latest`
- Expected runtime: about 3.5 minutes wall-clock
- Billing model: one job, rounded up to 4 billed minutes
- Cost basis after included minutes are exhausted: 4 minutes x $0.006 = $0.024 per run

### Per Validation Run

| Metric | Estimate |
|--------|----------|
| Observed runtime | ~3.5 minutes |
| Billed runtime | 4 minutes |
| Estimated paid cost on Linux 2-core | **$0.024 per run** |

This cost only applies after the included monthly minutes have been exhausted for a private repository owner. For public repositories using standard runners, the cost remains $0.

### Monthly Projections

| Scenario | PR Runs per Month | Estimated Billed Minutes | GitHub Free Org Cost | GitHub Team or Pro Cost |
|----------|-------------------|--------------------------|----------------------|-------------------------|
| Small team | 20 | 80 | $0 | $0 |
| Medium team | 60 | 240 | $0 | $0 |
| Large team | 150 | 600 | $0 | $0 |
| Very large org | 500 | 2,000 | $0 | $0 |
| Enterprise-scale private repo | 1,000 | 4,000 | **$12.00** | **$6.00** |

Formula used for paid Linux overage:

```text
max(0, billed_minutes - included_minutes) x 0.006
```

## Monitoring Usage

### 1. Budgets and Billing

GitHub's current control surface is `Budgets and alerts`, not the older `spending limits` wording.

**Organization or enterprise level:**
1. Open the organization or enterprise account.
2. Go to `Billing & Licensing`.
3. Open `Budgets and alerts`.
4. Create a product-level budget for `Actions`.
5. Set alerts at 75%, 90%, and 100%.
6. Optionally enable `Stop usage when budget limit is reached`.

**Important:** Avoid overlapping blocking budgets at both product and SKU scope unless that is intentional. GitHub applies usage to all applicable budgets, and any exhausted blocking budget can stop further usage.

### 2. Included Usage Alerts

GitHub can send included-usage email alerts when the account reaches:

- 90% of included usage
- 100% of included usage

These are separate from budget alerts.

### 3. GitHub Actions Metrics

For organizations, GitHub now provides dedicated Actions metrics views under `Insights`.

You can analyze usage by:

- Workflow
- Job
- Repository
- Runtime OS
- Runner type

You can also export usage data to CSV.

Important detail: the usage metrics view shows raw minutes consumed and does not apply billing multipliers or convert usage into dollar spend. It is useful for trend analysis, but billing still needs to be interpreted against runner pricing.

### 4. Repository-Level Checks

At repository level, use the Actions tab and workflow history to inspect:

- Run frequency
- Typical duration
- Retries and failures
- Whether redundant runs are being canceled

## Automated Usage Tracking

If you want workflow-level internal tracking, log cost-oriented metadata after each run and upload it as a short-retention artifact.

Example payload:

```json
{
  "workflow_run_id": "12345",
  "repository": "org/repo",
  "branch": "feature-branch",
  "event": "pull_request",
  "runner": "Linux 2-core x64",
  "duration_minutes_observed": 3.5,
  "duration_minutes_billed": 4,
  "estimated_runner_cost_usd": 0.024,
  "timestamp": "2026-04-16T10:30:00Z",
  "validation_results": {
    "vale_errors": 0,
    "akr_errors": 2,
    "akr_warnings": 5,
    "completeness": 0.85
  }
}
```

Use a short artifact retention window so usage metrics do not create unnecessary storage accrual.

### Power BI or Excel Aggregation

```powershell
# Aggregate previously downloaded usage metric artifacts
$runs = Get-ChildItem usage-metrics-*.json |
  ForEach-Object { Get-Content $_ | ConvertFrom-Json }

$totalBilledMinutes = ($runs | Measure-Object -Property duration_minutes_billed -Sum).Sum
$includedMinutes = 2000
$runnerRate = 0.006
$monthlyCost = [Math]::Max(0, ($totalBilledMinutes - $includedMinutes) * $runnerRate)

Write-Host "Total billed minutes: $totalBilledMinutes"
Write-Host "Estimated monthly runner cost: `$$monthlyCost"
```

Adjust `$includedMinutes` to `3000` for GitHub Pro or Team, or `50000` for GitHub Enterprise Cloud.

## Cost Optimization Strategies

### 1. Trigger Only on Relevant Changes

```yaml
on:
  pull_request:
    paths:
      - 'docs/**'
      - '.akr/**'
      - '.github/workflows/validate-documentation.yml'
      - '.akr-config.json'
```

This prevents documentation validation from running on unrelated code-only changes.

### 2. Validate Only Changed Files

Use changed-file filtering so the workflow validates only the affected docs instead of the whole repository when possible.

**Expected impact:** lower runtime and fewer unnecessary comments.

### 3. Cancel Redundant Runs

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

This is still one of the simplest ways to cut waste on busy pull requests.

### 4. Cache Dependencies Carefully

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

Caching can reduce runtime, but remember that cache storage is metered beyond the included 10 GB per repository.

### 5. Keep Artifact Retention Short

```yaml
- name: Upload usage metrics
  uses: actions/upload-artifact@v4
  with:
    name: usage-metrics
    path: usage-metrics.json
    retention-days: 7
```

Because storage accrues hourly, low-value artifacts should not be retained for long periods.

### 6. Avoid Larger Runners for Documentation Jobs

Documentation validation rarely needs larger runners. They are always billable and cannot use included minutes.

### 7. Consider Self-Hosted Runners Only at Higher Scale

Self-hosted runners avoid GitHub-hosted minute charges, but they shift cost and operational burden to your infrastructure. This is typically only worth the complexity at sustained higher usage.

## Budgets and Alerts

### Recommended Starting Budget

For an organization adopting AKR validation on private repositories, a reasonable initial Actions budget is:

```text
$10 to $25 per month at the organization level
```

That is more than enough for typical documentation validation workloads unless many repositories are sharing the same quota and frequently exceeding included minutes.

### Alert Configuration

Use both of these:

- Budget alerts at 75%, 90%, and 100%
- Included usage alerts at 90% and 100%

### Workflow Safety Guardrail

```yaml
jobs:
  validate-documentation:
    runs-on: ubuntu-latest
    timeout-minutes: 10
```

This protects against hanging or unexpectedly slow validation runs.

## Best Practices

### 1. Review Usage Trends Quarterly

- Check org-level Actions usage metrics every quarter.
- Review the top workflows and repositories by minute consumption.
- Revisit budgets as adoption grows.

### 2. Keep Validation Local-First

Encourage developers to catch issues before pushing.

```bash
# Install Vale locally
brew install vale
choco install vale

# Run Vale locally
vale docs/

# Run AKR structural validation locally
python .akr/scripts/validate_documentation.py --output json

# Run business-doc validation locally, if applicable
python validation/scripts/validate_business_docs.py --status-aware
```

### 3. Track ROI Using Billed Minutes

Manual documentation review time is still materially more expensive than Actions runtime. Even at $0.024 per paid run on Linux, the automation cost is usually trivial compared to developer review time.

## Troubleshooting High Costs

### Issue: Workflows cost more than expected

**Check:**
1. Whether the repository is private rather than public.
2. Whether the workflow is using a larger runner.
3. Whether repeated pushes are creating redundant runs.
4. Whether a single 3.1 to 3.9 minute job is being rounded to 4 billed minutes.

### Issue: Budget alerts fire before the billing page looks high

**Check:**
1. Whether multiple repositories share the same owner budget.
2. Whether overlapping budgets exist at product and SKU scopes.
3. Whether usage metrics are being interpreted as raw minutes instead of billed spend.

### Issue: Storage costs rise unexpectedly

**Check:**
1. Artifact retention days.
2. Cache growth beyond the included 10 GB per repository.
3. Whether old usage-metrics artifacts are being kept too long.

## Resources

- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)
- [Billing and usage for GitHub Actions](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [Setting up budgets to control spending on metered products](https://docs.github.com/en/billing/how-tos/set-up-budgets)
- [Viewing GitHub Actions metrics for your organization](https://docs.github.com/en/enterprise-cloud@latest/organizations/collaborating-with-groups-in-organizations/viewing-github-actions-metrics-for-your-organization)
- [GitHub pricing calculator](https://github.com/pricing/calculator?feature=actions)

---

**Last Updated:** April 16, 2026  
**Pricing Verified:** April 2026  
**Next Review:** July 2026
