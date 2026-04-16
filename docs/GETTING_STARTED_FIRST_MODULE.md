# Getting Started: First Module

Date: 2026-04-14
Audience: First-time AKR users running a pilot module flow
Goal: Complete one module from grouping to validated merge path

## Who This Is For

Use this guide if you want the shortest path to first value.

If you need full multi-role onboarding and consolidation paths, use:
- docs/TEAM_STARTUP_ONBOARDING_GUIDE.md

## Four Steps Only

## Step 1 - Prepare VS Code and authentication

1. Install VS Code GitHub and Copilot extensions required by your organization.
2. Sign in and confirm repository access.
3. Open the source repository where module docs will be generated.

## Step 2 - Propose module groupings

Run:

/akr-docs groupings

Outcome:
- Candidate module entries are prepared for review.

## Step 3 - Review and approve modules.yaml entries

1. Open modules.yaml.
2. Confirm module names, file coverage, and ownership intent.
3. Approve only modules ready for generation.

Outcome:
- grouping_status is approved for the first target module.

## Step 4 - Generate and review first module documentation

Run:

/akr-docs generate <ModuleName>

Then:
1. Review generated sections.
2. Resolve unknown markers with the right reviewers.
3. Run existing validation flow before merge.

Outcome:
- First module doc reaches merge-ready quality.

## What To Ignore For Now

To keep first-run simple, ignore these topics in the first cycle:
- Cross-repository consolidation
- Advanced score-mode policy decisions
- Compliance graduation details beyond pilot behavior
- Cache maintenance unless connectivity issues occur

## Definition of Done (First Module)

A first module run is done when:
1. Module entry is approved in modules.yaml.
2. Module documentation is generated and reviewed.
3. Unknowns are either resolved or explicitly tracked.
4. Validation checks pass according to your pilot policy.
5. Documentation is ready for PR merge.

## Minimal Troubleshooting

If generation fails:
1. Re-check module name and grouping approval state.
2. Re-run generation for the same module.
3. Use team reviewer checkpoints to close unresolved sections.

If validation fails:
1. Fix reported missing sections or metadata issues.
2. Re-run validation.
3. Merge only after pilot-required checks are green.
