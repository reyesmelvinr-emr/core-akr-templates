# AKR Optimization Migration Guide

> Current-state note: AKR no longer uses git submodules in consuming repositories.
> This guide keeps only the minimum legacy context needed to retire older repos
> while documenting the current runtime-fetch and workspace-distributed model.

## What Changed and Why

### Problem Solved

The previous architecture had three contradictions:

1. **Pinned local standards copies created drift** — older repos kept
  `.akr/templates/` as a locally managed standards source, freezing
  `core-akr-templates` at a past commit and requiring manual refresh work to
  stay current.

2. **`distribute-skill.yml` spread local copies** — vale rules and `.vale.ini`
   were copied into every application repo on every release, creating drift risk
   and defeating the remote-source model.

3. **SKILL.md loaded 3,500+ tokens per invocation** — all three mode workflows,
   the full charter routing table, and all SSG pass definitions loaded into context
   even when only one mode was needed.

### What the New Architecture Does

```
core-akr-templates (GitHub — single source of truth)
├── .github/skills/akr-docs/
│   ├── SKILL.md                  ← thin dispatcher (~400 tokens)
│   ├── SKILL-COMPAT.md
│   └── scripts/
│       ├── akr-groupings.md      ← ProposeGroupings (~600 tokens)
│       ├── akr-generate.md       ← GenerateDocumentation (~800 tokens)
│       ├── akr-resolve.md        ← ResolveUnknowns (~400 tokens)
│       ├── akr-refresh-assets.md ← RefreshAssets
│       ├── akr-score.md          ← Score mode
│       ├── akr_inline_validate.py
│       └── validate_documentation.py
├── .github/skills/akr-interview/
│   ├── SKILL.md
│   └── scripts/
│       └── akr-interview.md
├── .github/skills/akr-capability/
│   ├── SKILL.md
│   ├── SKILL-COMPAT.md
│   └── scripts/
│       └── enhancement-clarify.md
├── .akr/
│   ├── vale-rules/               ← single copy of vale rules (here only)
│   └── scripts/validate_documentation.py
└── copilot-instructions/         ← charter slices (fetched on demand)

application-repo (consumer)
├── .github/skills/akr-docs/
│   ├── SKILL.md                  ← distributed (needed by Copilot locally)
│   ├── SKILL-COMPAT.md           ← distributed
│   └── scripts/                  ← distributed as workspace-local execution assets
│       ├── akr-groupings.md
│       ├── akr-generate.md
│       ├── akr-resolve.md
│       ├── akr-refresh-assets.md
│       ├── akr-score.md
│       ├── akr_inline_validate.py
│       └── validate_documentation.py
├── .github/skills/akr-interview/
│   ├── SKILL.md
│   └── scripts/
│       └── akr-interview.md
├── .github/skills/akr-capability/
│   ├── SKILL.md
│   ├── SKILL-COMPAT.md
│   └── scripts/
│       └── enhancement-clarify.md
├── .github/hooks/                ← distributed (needed locally)
├── .github/copilot-instructions.md ← OWNED BY APPLICATION TEAM — never overwritten
├── modules.yaml                  ← application-specific manifest
└── docs/                         ← generated documentation
```

**Vale rules and `.vale.ini` are no longer distributed. The CI workflow fetches
them at runtime via `git clone --depth 1`.**

---

## Migration Steps for Each Application Repository

### Step 1: Delete locally distributed vale rules

```bash
# Remove the local copies that were distributed by the old workflow
rm -rf validation/vale-rules/
rm -f validation/.vale.ini
git add -A validation/
git commit -m "chore: remove locally distributed vale rules (now fetched at CI runtime)"
```

### Step 2: Update your CI validation workflow

Replace the existing `.github/workflows/validate-documentation.yml` with the
version from this migration package. The key change is:

**Before:**
```yaml
- name: Clone core-akr-templates
  run: git clone https://github.com/org/core-akr-templates ~/.akr/templates

- name: Run Vale linter
  run: |
    VALE_CONFIG=~/.akr/templates/validation/.vale.ini  # ← was pointing to validation/ copy
```

**After:**
```yaml
- name: Fetch core-akr-templates at runtime
  run: |
    git clone --depth 1 \
      https://github.com/reyesmelvinr-emr/core-akr-templates.git \
      ~/.akr/templates

- name: Run Vale linter
  run: |
    VALE_CONFIG=~/.akr/templates/.akr/.vale.ini  # ← always points to single canonical copy
```

### Step 3: Update your copilot-instructions.md

The AKR section in your application's `.github/copilot-instructions.md` should
be reduced to a thin pointer. Do not replace your team's existing coding conventions.

Add or replace only the AKR block:

```markdown
## AKR Documentation (Do Not Remove)

Use the akr-docs skill for all module documentation tasks.

Invocation:
- /akr-docs groupings          — propose module groupings
- /akr-docs generate [Module]  — generate documentation for approved module
- /akr-docs generate --batch [ModuleA ModuleB ...] — generate docs for an explicit approved module list (max 5; score auto-skipped)
- /akr-docs resolve [file]     — resolve ❓ markers in existing draft

Charter and template content is loaded by the skill at runtime from core-akr-templates.
Do not paste charter content here — it will be loaded on demand to conserve tokens.

Fallback paths (when @github MCP is unavailable):
- Mode scripts: .github/skills/akr-docs/scripts/
- Cached assets: .akr/cache/
```

### Step 4: Merge the updated skill distribution PR

When `core-akr-templates` publishes the next skill release, the updated
`distribute-skill.yml` will open a PR in your repo that:
- Updates `SKILL.md` (thin dispatcher)
- Updates `SKILL-COMPAT.md`
- Syncs mode scripts and validators under `.github/skills/akr-docs/scripts/`
- Adds/updates `.github/skills/akr-interview/SKILL.md` and `scripts/akr-interview.md`
- Adds/updates `.github/skills/akr-capability/SKILL.md`, `SKILL-COMPAT.md`, and `scripts/enhancement-clarify.md`
- Updates hook files
- Does NOT touch `validation/`, `copilot-instructions.md`, or any other file

Review and merge that PR.

---

## Token Budget Comparison

Note: values below are historical migration baselines from the initial thin-dispatcher rollout.
Current script counts have expanded, but the architectural token savings pattern remains the same.

| Scenario | Old token load | New token load | Saving |
|---|---|---|---|
| `/akr-docs groupings` | ~3,500 (full SKILL.md) | ~400 (dispatcher) + ~600 (groupings script) | ~65% |
| `/akr-docs generate Module` | ~3,500 + ~2,500 (charter) | ~400 (dispatcher) + ~800 (generate script) + ~2,500 (charter, one call) | ~17% on generation |
| `/akr-docs generate --batch A B C` | Repeated single-module overhead per run | Shared dispatcher/template/charter fetch path + per-module assembly; one confirmation gate | Lower orchestration overhead across listed modules |
| `/akr-docs resolve file` | ~3,500 (full SKILL.md) | ~400 (dispatcher) + ~400 (resolve script) | ~77% |
| SSG Pass 2–7 | Re-reads charter risk | Charter in forward payload, no re-fetch | Eliminates re-fetch violations |

The biggest gains are on `groupings` and `resolve` which previously loaded the
full SKILL.md including SSG pass definitions they never use.

---

## Frequently Asked Questions

**Q: The mode scripts are distributed as PATH B fallbacks — doesn't that re-create the local copy problem?**

A: Partially, yes — but only for the script files, which are small (~600–800 tokens
each) and change only when the workflow logic changes, not when charter content
changes. Charter content (the large token consumer) is still fetched on demand
from `core-akr-templates`. The mode scripts are stable structural artifacts;
the charter slices are the volatile content. This is the right split.

**Q: Where does the akr-interview skill fit?**

A: `akr-interview` is distributed like other execution assets because it is invoked
locally in application repositories. Governance and compatibility guidance for
interview behavior should be reviewed together with `akr-docs` updates.

**Q: Where does the akr-capability skill fit in application repositories?**

A: Application repositories receive only the developer-facing `enhancement-clarify`
mode. The PO/TL-facing `enhancement-review`, `enhancement-review-close`, and
`enhancement-test-generation` modes stay in consolidation repositories because
they operate on capability business artifacts rather than source-repo module docs.

**Q: What happens if core-akr-templates is unavailable when CI runs?**

A: The CI workflow will fail at the clone step. This is intentional — a stale
local copy would mask the problem. If uptime is a concern, pin to a specific tag:
```yaml
git clone --branch v1.1.0 --depth 1 https://github.com/org/core-akr-templates ~/.akr/templates
```

**Q: Can I still use the akr-docs skill in Visual Studio (not VS Code)?**

A: Yes. Visual Studio uses PATH B — it reads from `.github/skills/akr-docs/scripts/`
which is distributed. When cached template or charter assets are available, the
mode scripts use the workspace `.akr/cache/` directory; otherwise they require
live GitHub access for remote fetches.

**Q: What if I still have a repo that was onboarded during the old submodule era?**

A: Retire the legacy `.akr/templates/` checkout as part of that repo's migration PR,
then move the repo to the current model documented here. That cleanup is a
one-time migration task for older consuming repositories, not part of the active
AKR architecture.

**Q: My team has custom Vale rules. Where do they go?**

A: Keep AKR-owned rules in `core-akr-templates/.akr/vale-rules/` only. If an
application repo needs team-specific custom rules, place them in a separate
repo-owned path such as `.akr/vale-rules/custom/` and extend the fetched base
config from a local `.vale.ini`. Do not recreate `validation/vale-rules/` or
`validation/.vale.ini` as AKR-managed duplicates. Document any repo-owned Vale
extensions in your team's `OUR_STANDARDS.md`.

---

## Migration for Consolidation Repositories: Capability Lifecycle Folder Structure

As of April 2026, consolidation repositories now organize capabilities by lifecycle status (active/archived/new) instead of using a flat `docs/business-capabilities/` folder. This section guides consolidation repository owners through the migration.

### What Changed

**Before:**
```
docs/business-capabilities/
  CourseManagement/
    index.md
    test-conditions.md
    enhancement-test-conditions.md
    enhancements.md
    limitations.md
    ...
  EnrollmentManagement/
    index.md
    ...
```

**After:**
```
docs/business-capabilities/
  active/
    CourseManagement/
      index.md
      test-conditions.md
      enhancement-test-conditions.md
      enhancements.md
      backlog.md (new)
      limitations.md
      ...
    EnrollmentManagement/
      ...
  new/
    UserManagement/
      index.md      (may include work-item links)
      test-conditions.md
      limitations.md
      (excludes enhancement/backlog files)
      ...
  archived/
    LegacyFeature/
      index.md
      limitations.md
      (read-mostly baselines; no new enhancement/test artifacts)
      ...
```

### Migration Steps for Consolidation Repositories

#### Step 1: Assign capability status

Work with the Product Owner to assign each capability a status:

- **active**: Used in production; supports active enhancement planning and test updates.
- **new**: Under construction; not yet in production; minimal artifact set.
- **archived**: No longer in use; codebases retained for legacy/audit purposes; historical baseline only.

Document the status assignments in your consolidation repository README or governance docs.

#### Step 2: Create status folders

```bash
cd docs/business-capabilities/
mkdir -p active archived new
```

#### Step 3: Migrate existing capabilities to status folders

For each capability folder:

```bash
# Example: migrate CourseManagement (active)
mv CourseManagement active/

# Example: migrate LegacyFeature (archived)
# First, remove enhancement/test artifacts not applicable to archived capabilities
rm archived/LegacyFeature/enhancement-test-conditions.md
rm archived/LegacyFeature/enhancements.md
# Then move
mv LegacyFeature archived/

# Example: migrate UserManagement (new capability, minimal artifact set)
# Remove files not applicable to new capabilities
rm new/UserManagement/enhancement-test-conditions.md
rm new/UserManagement/enhancements.md
mv UserManagement new/
```

#### Step 4: Normalize artifact sets by status

**For each active capability**, ensure all 9 files are present:
- `index.md`, `test-conditions.md`, `enhancement-test-conditions.md`, `enhancements.md`, `backlog.md` (new — create if missing), `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md`

If `backlog.md` is missing, initialize it from `capability_backlog_template.md` in `core-akr-templates/.akr/templates/`.

**For each new capability**, retain only 5 files:
- `index.md`, `test-conditions.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`
- Remove `enhancement-test-conditions.md`, `enhancements.md`, `backlog.md`, `traceability.md` if present.

**For each archived capability**, retain only 5 files:
- `index.md`, `limitations.md`, `internal_dependencies.md`, `external_dependencies.md`, `traceability.md`
- Remove all others.

#### Step 5: Update templates

Ensure canonical templates in `.akr/templates/` include the new `capability_backlog_template.md`:
- `business_capability_template.md`
- `capability_testing_template.md`
- `capability_enhancement_testing_template.md`
- `capability_enhancements_template.md`
- `capability_backlog_template.md` (new)
- `capability_limitations_template.md`
- `capability_internal_dependencies_template.md`
- `capability_external_dependencies_template.md`
- `traceability-template.md`

#### Step 6: Update CODEOWNERS

If your `.github/CODEOWNERS` file has rules for `docs/business-capabilities/`, update them to the new paths:

**Before:**
```
/docs/business-capabilities/ @ProductOwner @TechnicalLead
```

**After:**
```
/docs/business-capabilities/active/ @ProductOwner @TechnicalLead
/docs/business-capabilities/new/ @ProductOwner @TechnicalLead
/docs/business-capabilities/archived/ @ProductOwner
```

You may want stricter review requirements for active capabilities and lighter review for new/archived.

#### Step 7: Test and validate

Run your consolidation repository's validation scripts to confirm status-aware completeness:

```bash
# Example: your validation script should now enforce status-aware completeness
python validation/scripts/validate_business_docs.py --status-aware
```

Validation should confirm:
- Active capabilities have all 9 files.
- New capabilities have exactly 5 files (no enhancement/backlog/traceability artifacts).
- Archived capabilities have exactly 5 files (no active artifacts).
- No ".md" files exist at the `business-capabilities/` level (all organized by status).

#### Step 8: Commit and announce

Once migration is complete:

```bash
git add -A docs/business-capabilities/
git commit -m "chore: reorganize capabilities by lifecycle status (active/archived/new)"
git push origin <your-branch>
```

Create a PR and include migration summary:
- Count of capabilities by status.
- Any removed files and rationale (e.g., "removed enhancement-test-conditions.md from new capabilities per status-aware contract").
- Validation output showing status-aware completeness checks passed.

### Migration FAQ

**Q: What if I have a capability that's partially active (e.g., some features active, others being developed)?**

A: Assign it `active` status if the majority of its business value is in production and actively managed. If it's primarily under construction, treat it as `new`. The Product Owner and Technical Lead should decide together based on the current production usage and planned timeline.

**Q: What happens to old enhancement items in my enhancements.md?**

A: For active capabilities, keep them and update their status. For new capabilities being migrated, move them to `backlog.md` if they're planned future work, or delete if they're obsolete. Archive retired items in a separate historical document if audit trail is needed.

**Q: Can I merge active and new capabilities later?**

A: Yes. When a new capability reaches production, change its status to active, add back the enhancement/backlog/test artifacts, and move the folder from `new/` to `active/`. Announce the transition in your consolidation repository release notes.

**Q: Do I need to re-run capability-consolidation after migration?**

A: Not immediately, unless artifact paths have changed. Once your status-aware capability-consolidation skill is deployed from `core-akr-templates`, running it will automatically place outputs in status-aware paths. At that point, subsequent consolidation runs will use the new paths natively.
