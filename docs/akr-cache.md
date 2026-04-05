# AKR Mode Script: CacheManagement

<!-- Loaded on demand by SKILL.md dispatcher. -->
<!-- Handles /akr-docs update-cache and /akr-docs cache-status commands. -->

## Purpose

Manage the developer's local AKR cache at `~/.akr/templates/`.
The cache is a `git clone` of `core-akr-templates` that serves as the PATH B/C
fallback source for mode scripts, templates, and the inline validator.

This script does NOT generate documentation. It only:
1. Reports cache state (`cache-status`)
2. Refreshes the cache from the remote (`update-cache`)

---

## Command: `/akr-docs cache-status`

Report the current state of the local AKR cache without modifying anything.

### Step 1: Check cache existence

```bash
test -d "$HOME/.akr/templates/.git"
```

- If missing → report:
  ```
  ⚠️  AKR cache not found at ~/.akr/templates/
  Run: git clone https://github.com/reyesmelvinr-emr/core-akr-templates ~/.akr/templates
  Or invoke: /akr-docs update-cache
  ```
  Stop here.

### Step 2: Read cache version

Read the `skill-version:` field from `~/.akr/templates/.github/skills/akr-docs/SKILL.md`.

Read the `skill-version:` field from `.github/skills/akr-docs/SKILL.md` in the
current application repository (the distributed copy).

### Step 3: Read cache age

```bash
# Date of last git fetch in the cache clone
stat "$HOME/.akr/templates/.git/FETCH_HEAD" 2>/dev/null || echo "never fetched"
```

On Windows PowerShell:
```powershell
(Get-Item "$env:USERPROFILE\.akr\templates\.git\FETCH_HEAD" -ErrorAction SilentlyContinue).LastWriteTime
```

### Step 4: Report status in chat

```
## AKR Cache Status

Cache path:        ~/.akr/templates/
Cache skill-version: {cache_version}
Distributed skill-version: {distributed_version}
Version match:     {✅ Match | ⚠️  MISMATCH — cache may be stale}
Last refreshed:    {date from FETCH_HEAD, or "never"}
Age:               {N days ago}

{If MISMATCH or age > 30 days}
⚠️  Recommendation: Run /akr-docs update-cache to refresh the cache.
{Else}
✅  Cache is current. No action needed.
```

---

## Command: `/akr-docs update-cache`

Pull the latest `core-akr-templates` into the local cache.

### Step 1: Check cache existence

Same as cache-status Step 1. If cache does not exist, clone it:

```bash
git clone https://github.com/reyesmelvinr-emr/core-akr-templates ~/.akr/templates
```

On Windows PowerShell:
```powershell
git clone https://github.com/reyesmelvinr-emr/core-akr-templates "$env:USERPROFILE\.akr\templates"
```

Report "Cache initialized from remote." and continue to Step 3.

### Step 2: Pull latest changes

```bash
git -C "$HOME/.akr/templates" pull --ff-only
```

On Windows PowerShell:
```powershell
git -C "$env:USERPROFILE\.akr\templates" pull --ff-only
```

- If `--ff-only` fails (diverged history): report:
  ```
  ⚠️  Cache cannot be fast-forwarded. This is unexpected for a read-only clone.
  Run manually: git -C ~/.akr/templates fetch origin && git -C ~/.akr/templates reset --hard origin/master
  ```
  Stop here. Do not auto-reset without user confirmation.

### Step 3: Report what changed

```bash
git -C "$HOME/.akr/templates" log "HEAD@{1}..HEAD" --oneline
```

If the log is empty: "Cache was already up to date."

### Step 4: Read new version

Read updated `skill-version:` from `~/.akr/templates/.github/skills/akr-docs/SKILL.md`.

### Step 5: Compare with distributed version

Read `skill-version:` from `.github/skills/akr-docs/SKILL.md` in the application repo.

### Step 6: Report result in chat

```
## AKR Cache Updated

Cache path:  ~/.akr/templates/
New version: {new_skill_version}

Changes pulled:
{git log lines, or "Already up to date."}

{If new_version != distributed_version}
⚠️  Distributed SKILL.md is still at {distributed_version}.
    The next distribute-skill.yml workflow run will update the application repo.
    Until then, PATH B runs in this repo will use the old distributed scripts.
    Use --remote on your next /akr-docs generate run to bypass the local scripts.

{If new_version == distributed_version}
✅ Cache and distributed version are in sync.
   Next /akr-docs generate run will use PATH A (remote) or current distributed scripts.
```

---

## Cache Age Warning Thresholds

| Age | Behavior |
|---|---|
| < 30 days | No warning |
| 30–60 days | ⚠️ Advisory warning on generate pre-flight |
| > 60 days | ⚠️ Stronger advisory — recommend update before generate run |

These thresholds apply to the `FETCH_HEAD` mtime check in `akr-generate.md` Step 1.
They are warnings only — generation is never blocked by cache age.
