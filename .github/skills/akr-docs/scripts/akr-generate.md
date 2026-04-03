# AKR Mode Script: GenerateDocumentation

<!-- Loaded on demand by SKILL.md dispatcher. Do not load unless /akr-docs generate was invoked. -->

## Purpose

Generate module documentation for a named module whose `grouping_status` is `approved` in `modules.yaml`.

## Pre-flight Checks

1. Read `modules.yaml`. Locate the requested module by name.
2. If `grouping_status: draft` → stop. Respond: "Module grouping is not yet approved. Review `modules.yaml` and set `grouping_status: approved` before generating documentation."
3. If module not found → stop. Respond: "Module not found in modules.yaml. Run `/akr-docs groupings` first."

## Step 1: Infer Project Type and Load Charter Slice

Infer `project_type` from the module file list (do not ask the user):

| Files present | Inferred project_type |
|---|---|
| Controller + Service + Repository + Entity + DTO | `api-backend` |
| Page/View component + sub-components + hooks + types | `ui-component` |
| Orchestration-heavy, no standard CRUD vertical slice | `microservice` |
| Ambiguous or mixed | `general` |

**Load the charter slice for the inferred project_type — this counts as 1 of 2 allowed @github calls:**

| project_type | Charter to fetch |
|---|---|
| `api-backend` | `@github get file core-akr-templates/copilot-instructions/backend-service.instructions.md` |
| `ui-component` | `@github get file core-akr-templates/copilot-instructions/ui-component.instructions.md` |
| `microservice` | `@github get file core-akr-templates/copilot-instructions/backend-service.instructions.md` |
| `general` | `@github get file core-akr-templates/copilot-instructions/backend-service.instructions.md` |

**PATH B / PATH C fallback:** Read from `.akr/templates/copilot-instructions/{charter-file}` locally.

Place the full charter content into the forward payload as a compact summary. Do not re-fetch it in later passes.

## Step 2: Select Template Reference

Do not embed the template. Record its path for reference during section generation.

| project_type | Template path |
|---|---|
| `api-backend` / `microservice` / `general` | `core-akr-templates/templates/lean_baseline_service_template_module.md` |
| `ui-component` | `core-akr-templates/templates/ui_component_template_module.md` |

If you need to verify a specific section format during generation, fetch only the relevant section of the template using a targeted file read — do not load the entire template into context.

## Step 3: Read Module Source Files

Read only the files listed under `files:` for the target module in `modules.yaml`. Do not read files from other modules.

Build a compact **source facts payload** containing:
- File name → role (Controller / Service / Repository / Entity / DTO)
- Public method signatures (name, parameters, return type)
- Notable validation attributes or guard clauses
- Database table references (from DbContext or repository query expressions)
- Exception types thrown
- Dependency injection constructor parameters

Do not carry raw file content forward. Carry structured facts only.

## Step 4: Evaluate Conditional Sections

Before generating, decide which sections to include. Record decisions in the draft front matter under `excluded-sections`.

| Section | Include if |
|---|---|
| API Contract | Module contains a Controller with `[Http*]` attributes |
| Validation Rules | `*Validator.cs`, DTO `[DataAnnotations]`, or explicit guard clauses exist |
| Consumer Map | Actual callers visible in listed module files |
| Related Documentation | Other `doc_output` paths exist in `modules.yaml` |

## Step 5: Generate Documentation

**Default strategy: single-pass.** Generate all required sections in one pass using the source facts payload and charter summary from Steps 1–3.

Use `--use-ssg` flag only when:
- Module has 6+ files with complex inter-file logic
- Context pressure is observed (responses truncating)
- First-pass output fails the quality threshold check

### Single-Pass Output Requirements

Generate sections in this order (template section order):

1. YAML front matter (required fields from charter)
2. AKR metadata header (`<!-- akr-generated ... -->`)
3. Quick Reference (TL;DR)
4. Module Files table
5. Purpose and Scope
6. Operations Map (all public operations across all files)
7. Architecture Overview (text/ASCII only — no Mermaid)
8. Business Rules table (Rule ID, Description, Why It Exists, Since When)
9. Data Operations (Reads, Writes, side effects)
10. API Contract (conditional)
11. Validation Rules (conditional)
12. Consumer Map (conditional)
13. Questions and Gaps
14. Related Documentation (conditional)

### SSG Pass Sequence (only when --use-ssg)

| Pass | Scope | Forward Payload Output |
|---|---|---|
| 1 | Module Files + role mapping + conditional section decisions | File-role map, conditional section list, charter summary |
| 2A | Operations extraction (controller + service) | Operation signatures, input/output contracts |
| 2B | Operations extraction (repository + DTO) — split if context pressure | Repository operations, DTO field list |
| 3 | Architecture Overview + dependency flow | Architecture text, dependency table |
| 4 | Business Rules table | Rules with enforcement points |
| 5 | Data Operations + side effects | Read/write table, side effects |
| 6 | Questions and Gaps + marker normalization | Resolved ❓ list, DEFERRED items |
| 7 | Final assembly + front matter check + metadata header + truncation check | Final document |

**SSG rules:**
- Carry only the forward payload between passes — never re-read source files or the charter after Pass 1.
- If a pass result is truncated, split it (2A/2B pattern) and record the split in metadata.
- Record pass timings when available.

## Step 6: Write Draft Artifact

Write the generated document to `docs/modules/.akr/{ModuleName}_draft.md`.

Add these draft-only front matter fields (they will be stripped before final output):
```yaml
preview-generated-at: {ISO-8601 timestamp}
review-mode: full
generation-strategy: {single-pass | section-scoped}
passes-completed: {list}
```

Surface the draft path in chat and wait for explicit user confirmation before proceeding to Step 7.

## Step 7: Write Final Document

On user confirmation:
1. Strip draft-only front matter fields (`preview-generated-at`, `review-mode`).
2. Set `status: draft` in front matter (never copy module grouping status).
3. Write to the `doc_output` path from `modules.yaml`.
4. Confirm the `<!-- akr-generated -->` metadata header is present at the top of the file body.

## Step 8: Validate

Run the validator:
```bash
python .akr/scripts/validate_documentation.py \
  --file {doc_output_path} \
  --output json \
  --fail-on needs
```

If validator is not available locally, note: "Run CI validation before opening PR. See `.github/workflows/validate-documentation.yml`."

Report the validation summary in chat.

## Source Grounding Rules (apply in every pass)

- **Unmarked** = content directly evidenced by source files in the module file list.
- **🤖** = AI synthesis or inference across multiple files.
- **❓** = missing business intent, dates, or ownership not determinable from source files.
- Do not use ❓ for information the code directly answers.
- Do not invent: auth schemes, consumer names, DB index names, external integrations — unless visible in the listed files.

## Required Front Matter Fields

```yaml
---
businessCapability: PascalCaseFromRegistry
feature: FN#####_US#####
layer: {UI|API|Database|Integration|Infrastructure}
project_type: {api-backend|ui-component|microservice|general}
status: draft
compliance_mode: pilot
---
```

## Quality Threshold (check before writing final)

- [ ] All required sections present in template order
- [ ] Operations Map is complete (every public method in every module file covered)
- [ ] Business Rules table has Why It Exists and Since When columns
- [ ] Data Operations covers all reads, writes, and side effects
- [ ] No silent unknowns (all unknowns marked ❓ or DEFERRED with rationale)
- [ ] No truncated sections
- [ ] `<!-- akr-generated -->` header present
- [ ] Draft-only front matter fields stripped from final output
