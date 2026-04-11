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
