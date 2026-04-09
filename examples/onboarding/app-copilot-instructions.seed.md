# AKR Application Repository Guidance

## Purpose

Use AKR skills to produce accurate module documentation aligned to repository standards.

## Required practices

- Keep `.github/copilot-instructions.md` repository-owned.
- Use `/akr-docs groupings` before first module generation.
- Ensure generated docs include required front matter and AKR metadata header.
- Run validation before opening or merging PRs.

## Documentation flow

1. Keep `modules.yaml` current.
2. Generate documentation with `/akr-docs generate [ModuleName]`.
3. Resolve unknowns using `/akr-docs resolve [file]`.
4. Run validation workflow checks and address issues.

## Ownership

Application team owns business intent and source-of-truth module behavior.
