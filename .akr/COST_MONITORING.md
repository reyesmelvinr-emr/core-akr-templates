# GitHub Actions Cost Monitoring for AKR Documentation

## Overview

This document provides guidance on monitoring and controlling GitHub Actions costs for AKR documentation validation workflows.

## Pricing (January 2026)

### GitHub-Hosted Runners

| Runner Type | Cost per Minute | Free Tier |
|-------------|----------------|-----------|
| **Ubuntu** | $0.008 → $0.005* | 2,000 min/month |
| Windows | $0.016 | 2,000 min/month (2x multiplier) |
| macOS | $0.080 | 2,000 min/month (10x multiplier) |

\* Pricing reduced ~39% in January 2026

### Free Tier Details

- **Free tier:** 2,000 minutes/month for GitHub-hosted runners
- **Usage:** Applies to public repositories and private repositories with GitHub Free, Pro, or Team
- **Organizations:** Free tier shared across all repositories
- **Overflow:** ~$0.005/minute after free tier exhausted

## Cost Estimation

### Per Validation Run

| Step | Duration | Cost |
|------|----------|------|
| Checkout + Setup | ~1 min | $0.005 |
| Vale Installation | ~0.5 min | $0.0025 |
| Template Clone | ~0.5 min | $0.0025 |
| Validation | ~1 min | $0.005 |
| Checks API + Comments | ~0.5 min | $0.0025 |
| **Total per run** | **~3.5 min** | **~$0.0175** |

### Monthly Projections

**Scenario 1: Small Team (5 developers, 20 PRs/month)**
- Runs: 20 PRs × 3.5 min = 70 minutes
- Cost: Within free tier ($0)

**Scenario 2: Medium Team (15 developers, 60 PRs/month)**
- Runs: 60 PRs × 3.5 min = 210 minutes
- Cost: Within free tier ($0)

**Scenario 3: Large Team (30 developers, 150 PRs/month)**
- Runs: 150 PRs × 3.5 min = 525 minutes
- Cost: Within free tier ($0)

**Scenario 4: Very Large Org (100 developers, 500 PRs/month)**
- Runs: 500 PRs × 3.5 min = 1,750 minutes
- Cost: Within free tier ($0)

**Scenario 5: Enterprise Scale (200 developers, 1000 PRs/month)**
- Runs: 1,000 PRs × 3.5 min = 3,500 minutes
- Overage: 3,500 - 2,000 = 1,500 minutes
- Cost: 1,500 × $0.005 = **$7.50/month**

## Monitoring Usage

### 1. GitHub Actions Usage Dashboard

**Organization level:**
1. Go to Organization Settings
2. Billing and plans → Usage this month
3. View Actions minutes used
4. Set up spending limits

**Repository level:**
1. Repository → Insights → Actions
2. View workflow runs and durations

### 2. Automated Usage Tracking

The workflow logs usage metrics after each run:

```json
{
  "workflow_run_id": "12345",
  "repository": "org/repo",
  "branch": "feature-branch",
  "event": "pull_request",
  "duration_minutes": 3,
  "timestamp": "2026-01-14T10:30:00Z",
  "runner": "Linux",
  "validation_results": {
    "vale_errors": 0,
    "akr_errors": 2,
    "akr_warnings": 5,
    "completeness": 0.85
  }
}
```

These metrics are uploaded as artifacts for analysis.

### 3. PowerBI/Excel Dashboard (Optional)

Download usage metrics artifacts and aggregate:

```powershell
# Download artifacts from GitHub API
gh run list --repo org/repo --workflow validate-documentation.yml --json databaseId,conclusion,createdAt

# Aggregate monthly costs
$totalMinutes = (Get-ChildItem usage-metrics-*.json | 
  ForEach-Object { (Get-Content $_ | ConvertFrom-Json).duration_minutes } | 
  Measure-Object -Sum).Sum

$monthlyCost = [Math]::Max(0, ($totalMinutes - 2000) * 0.005)

Write-Host "Total minutes: $totalMinutes"
Write-Host "Monthly cost: `$$monthlyCost"
```

## Cost Optimization Strategies

### 1. Trigger Only on Relevant Changes

```yaml
on:
  pull_request:
    paths:
      - 'docs/**'           # Only docs changes
      - 'src/**/*.{cs,ts}'  # Only source code changes
      - '.akr-config.json'  # Only config changes
```

**Savings:** Reduce unnecessary runs by ~40-60%

### 2. Use Path Filters

```yaml
- name: Get changed files
  id: changed-files
  uses: tj-actions/changed-files@v41
  with:
    files: |
      docs/**/*.md
      src/**/*.{cs,ts,tsx}
```

Only validate changed files, not entire repository.

**Savings:** Reduce validation time by ~50-70%

### 3. Cancel Redundant Runs

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Cancel previous runs when new commits are pushed.

**Savings:** ~20-30% reduction

### 4. Cache Dependencies

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # Cache pip dependencies
```

**Savings:** ~10-20% faster runs

### 5. Use Self-Hosted Runners (Advanced)

For very large organizations:
- **Cost:** $0 for compute (you provide hardware)
- **Setup:** Requires infrastructure and maintenance
- **Best for:** >10,000 minutes/month usage

## Setting Spending Limits

### Organization Level

1. Go to Organization Settings → Billing and plans
2. Set monthly spending limit:
   ```
   Actions spending limit: $10/month (recommended start)
   ```
3. Enable email alerts at 75%, 90%, 100%

### Repository Level

Configure workflow timeout to prevent runaway costs:

```yaml
jobs:
  validate-documentation:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Max 10 minutes per run
```

## Alerts and Notifications

### 1. GitHub Email Alerts

GitHub automatically sends emails when:
- 75% of free tier consumed
- 90% of free tier consumed
- 100% of free tier consumed
- Spending limit reached

### 2. Custom Slack Notifications

```yaml
- name: Notify on high usage
  if: ${{ steps.duration.outputs.minutes > 5 }}
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{"text": "⚠️ Documentation validation took ${{ steps.duration.outputs.minutes }} minutes"}'
```

### 3. Monthly Cost Reports

Create a scheduled workflow:

```yaml
name: Monthly Cost Report

on:
  schedule:
    - cron: '0 0 1 * *'  # First day of month

jobs:
  cost-report:
    runs-on: ubuntu-latest
    steps:
      - name: Generate report
        run: |
          # Fetch usage data
          gh api /orgs/${{ github.repository_owner }}/settings/billing/actions \
            --jq '.total_minutes_used, .total_paid_minutes_used'
          
          # Send to Slack/Email
```

## Best Practices

### 1. Monitor Quarterly

- Review usage trends every 3 months
- Adjust spending limits as team grows
- Optimize workflows based on actual usage

### 2. Educate Developers

- Show developers how to check workflow status
- Encourage fixing validation errors locally
- Promote pre-commit hooks for early detection

### 3. Track ROI

**Time Saved:**
- Manual documentation validation: 15-20 min/PR
- Automated validation: 3.5 min/PR
- **Savings: 11.5-16.5 min/PR**

**Cost Benefit:**
- Developer time: $125/hr → ~$30/PR saved
- Actions cost: ~$0.02/PR
- **ROI: 1,500:1**

### 4. Use Local Validation

Encourage developers to run validation locally before pushing:

```bash
# Install Vale locally
brew install vale  # macOS
choco install vale # Windows

# Run validation
vale docs/

# Run AKR validation
python scripts/validation/validate_documentation.py docs/
```

**Savings:** Catch issues before triggering CI/CD (~30% reduction)

## Troubleshooting High Costs

### Issue: Workflows running too long

**Solution:**
1. Check for infinite loops or hanging processes
2. Add timeout limits
3. Optimize validation scripts

### Issue: Too many workflow runs

**Solution:**
1. Review trigger conditions
2. Implement concurrency cancellation
3. Use path filters

### Issue: Validating too many files

**Solution:**
1. Only validate changed files
2. Use git diff to detect changes
3. Skip unchanged documentation

## Resources

- [GitHub Actions Pricing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [GitHub Actions Usage Limits](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration)
- [Managing Spending Limits](https://docs.github.com/en/billing/managing-billing-for-github-actions/managing-your-spending-limit-for-github-actions)

---

**Last Updated:** January 14, 2026  
**Pricing as of:** January 2026 (verified)  
**Next Review:** April 2026
