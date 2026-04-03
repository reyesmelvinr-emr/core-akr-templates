# AKR Optimization Migration Guide

## What Changed and Why

### Problem Solved

The previous architecture had three contradictions:

1. **Submodules pinned stale content** — git submodules at `.akr/templates/` froze
   `core-akr-templates` at a past commit, requiring manual `git submodule update`
   to get updates.

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
│   └── scripts/
│       ├── akr-groupings.md      ← ProposeGroupings (~600 tokens)
│       ├── akr-generate.md       ← GenerateDocumentation (~800 tokens)
│       └── akr-resolve.md        ← ResolveUnknowns (~400 tokens)
├── .akr/
│   ├── vale-rules/               ← single copy of vale rules (here only)
│   └── scripts/validate_documentation.py
└── copilot-instructions/         ← charter slices (fetched on demand)

application-repo (consumer)
├── .github/skills/akr-docs/
│   ├── SKILL.md                  ← distributed (needed by Copilot locally)
│   ├── SKILL-COMPAT.md           ← distributed
│   └── scripts/                  ← distributed as PATH B/C fallbacks
│       ├── akr-groupings.md
│       ├── akr-generate.md
│       └── akr-resolve.md
├── .github/hooks/                ← distributed (needed locally)
├── .github/copilot-instructions.md ← OWNED BY APPLICATION TEAM — never overwritten
├── modules.yaml                  ← application-specific manifest
└── docs/                         ← generated documentation
```

**Vale rules and `.vale.ini` are no longer distributed. The CI workflow fetches
them at runtime via `git clone --depth 1`.**

---

## Migration Steps for Each Application Repository

### Step 1: Remove the git submodule

```bash
# In the application repository
git submodule deinit -f .akr/templates
git rm -f .akr/templates
rm -rf .git/modules/.akr/templates
git add .gitmodules
git commit -m "chore: remove core-akr-templates submodule (replaced by runtime fetch)"
```

### Step 2: Delete locally distributed vale rules

```bash
# Remove the local copies that were distributed by the old workflow
rm -rf validation/vale-rules/
rm -f validation/.vale.ini
git add -A validation/
git commit -m "chore: remove locally distributed vale rules (now fetched at CI runtime)"
```

### Step 3: Update your CI validation workflow

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

### Step 4: Update your copilot-instructions.md

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
- Charter files: load from ~/.akr/templates/copilot-instructions/ if local cache exists
```

### Step 5: Merge the updated skill distribution PR

When `core-akr-templates` publishes the next skill release, the updated
`distribute-skill.yml` will open a PR in your repo that:
- Updates `SKILL.md` (thin dispatcher)
- Updates `SKILL-COMPAT.md`
- Adds the three mode scripts under `.github/skills/akr-docs/scripts/`
- Updates hook files
- Does NOT touch `validation/`, `copilot-instructions.md`, or any other file

Review and merge that PR.

---

## Token Budget Comparison

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

**Q: The mode scripts are distributed as PATH B/C fallbacks — doesn't that re-create the local copy problem?**

A: Partially, yes — but only for the script files, which are small (~600–800 tokens
each) and change only when the workflow logic changes, not when charter content
changes. Charter content (the large token consumer) is still fetched on demand
from `core-akr-templates`. The mode scripts are stable structural artifacts;
the charter slices are the volatile content. This is the right split.

**Q: What happens if core-akr-templates is unavailable when CI runs?**

A: The CI workflow will fail at the clone step. This is intentional — a stale
local copy would mask the problem. If uptime is a concern, pin to a specific tag:
```yaml
git clone --branch v1.1.0 --depth 1 https://github.com/org/core-akr-templates ~/.akr/templates
```

**Q: Can I still use the akr-docs skill in Visual Studio (not VS Code)?**

A: Yes. Visual Studio uses PATH B — it reads from `.github/skills/akr-docs/scripts/`
which is distributed. The mode scripts reference charter paths that resolve to the
local cache at `~/.akr/templates/copilot-instructions/` via PATH C.

**Q: My team has custom Vale rules. Where do they go?**

A: Add them to `validation/vale-rules/AKR/` in your application repo. The CI
workflow fetches the base rules from `core-akr-templates` but runs Vale from the
project directory, so your custom rules will be picked up if you configure a
local `.vale.ini` that extends the fetched base config. Document this in your
team's `OUR_STANDARDS.md`.
