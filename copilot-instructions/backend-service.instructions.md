# AKR Backend Service Condensed Instructions

Version: 2.0
Extends: .akr/charters/AKR_CHARTER.md
Source charter: .akr/charters/AKR_CHARTER_BACKEND.md
Audience: Agent Skill GenerateDocumentation for api-backend modules

## Scope
Apply these rules when generating module documentation for backend service modules. Focus on service-layer behavior, orchestration, and business rules. Do not treat controller-only details as the primary documentation target.

## Content Density Principles
- **Tables over prose**: Prefer structured tables for dense relational info — AI scans tables via semantic chunking; prose requires linear reading.
- **WHY-first**: Sections must lead with business context, not mirror code structure.
- **Code-mirror = omit**: Do not document what reading the source file already answers directly. Copilot reads source files; the doc adds value by capturing intent, constraints, and context that code does not express.
- **Target density**: Generated docs should be approximately half the length of current baseline output, achieved by removing code-mirror content — not by compressing human-authored context.

## Required Front Matter
Every module document must begin with YAML front matter containing all fields below:

```yaml
---
businessCapability: PascalCaseTagFromRegistry
feature: FN12345_US678
layer: API
project_type: api-backend
status: draft
compliance_mode: pilot
---
```

Rules:
- businessCapability: required PascalCase key from tag-registry.
- feature: required work-item tag in FN#####_US##### format.
- layer: required and must match module layer.
- project_type: required, expected api-backend.
- status: governs the generated document's maturity state, not the module grouping approval state.
- for first-generation Mode B output, set status to draft unless document-content approval has already occurred through the documented review flow.
- do not copy `modules.yaml` module status directly into document front matter.
- compliance_mode: pilot or production.

## Metadata Header Requirements
Before section content, include an AKR metadata header block:

- Header marker: <!-- akr-generated -->
- Required fields: skill, mode, template, steps-completed, generated-at
- For section-scoped generation include: generation-strategy, passes-completed, pass-timings-seconds, total-generation-seconds

## Transparency Marker Rules
Use markers consistently and do not omit them:
- Prefer unmarked factual statements for content directly evidenced by the listed module source files.
- 🤖 for AI synthesis or inference across multiple files — not for single-source facts.
- ❓ for missing business context, intent, dates, or ownership — see Unknowns Discipline for detailed ❓ placement rules.
- NEEDS for required data pending completion.
- VERIFY for assumptions requiring confirmation.
- DEFERRED only with explicit justification text.

Placement rules:
- Markers must appear inline in the affected sentence/table row.
- Do not leave unresolved ambiguity without a marker.
- If a section cannot be completed from source, add explicit ❓ entries and continue.

## Module Files Rules
Document every file in modules.yaml for the target module.
Include:
- File path
- Role (Controller, Service, Repository, DTO, Validator, Mapper, etc.)
- Responsibility summary

Validation expectation:
- No module file may be omitted.
- Shared files outside module should be listed as dependencies, not module files.

## Operations Map Rules
## API Operations Rules
Cover the HTTP/service public contract boundary — controller action methods and service public methods only.
Include:
- Operation/method name
- Layer (Controller or Service)
- Owning file/class
- Input parameters and types
- Return type
- Business purpose

Do NOT include:
- Repository-layer method rows — implementation details readable from source
- Private/internal helper methods

Coverage rules:
- Include all controller action methods (HTTP entry points)
- Include all service public methods (the testable contract boundary)
- Include validation guard paths that alter the flow (e.g., returns 409 or 404 early)

## Architecture Overview Rules
## Integration Context Rules
Document module dependencies and callers. Do NOT generate a layered ASCII diagram — the Controller→Service→Repository→DB stack is standard and readable from source.

Include:
- **Dependencies table**: Dependency | Purpose | Failure Mode | Critical?
- **Consumers table**: what calls this module and for what purpose

If no external interface dependencies or callers are visible in module source files, omit this section entirely (do not guess from module name).

## Business Rules Requirements
Business Rules section is mandatory. Use a table with these columns:
- Rule ID
- Rule Description
- Why It Exists
- Since When

Rule guidance:
- Rule ID format: BR-[MODULE]-###
- Describe enforceable logic, not UI behavior.
- Include constraints, eligibility checks, thresholds, and policy gates.
- If date is unknown, set Since When to ❓ with context.

## Data Operations Requirements
## Data Operations Requirements
Document all reads and writes caused by module behavior using a 3-column table: Database Object | Purpose | Business Context.
Do NOT include a Performance Notes column — query patterns, indexes, and transaction scope are readable from repository source and database docs.

Coverage rules:
- Include indirect writes (events, audit rows, cache invalidations) when present.
- Include side effects (emails, notifications, queue messages).
- If no indirect writes exist, state: "No email, event, or queue side effects in this module."

## Questions And Gaps Rules
## Failure Modes Rules
Document only business-significant and module-handled failure scenarios (maximum 2–3 rows).

Do NOT include:
- Standard framework exceptions that propagate unchanged to global middleware (e.g., `DbUpdateException` → `ExceptionHandlingMiddleware`)
- Generic HTTP infrastructure exceptions

Include only exceptions the module explicitly catches and handles with domain-specific responses (e.g., `InvalidOperationException` → HTTP 409 Conflict).

## Questions And Gaps Rules
- Unknown business rule intent
- Missing lifecycle dates
- Ambiguous ownership or dependency behavior
- Missing source references

Each unresolved item must use ❓ and include next action/owner if known.

## Section-Scoped Generation Rules
SSG pass discipline is governed by SKILL.md §SSG rules. This file does not restate workflow steps.

## Grounding Rules
All factual claims must be directly traceable to files listed in modules.yaml for this module.
- Do not infer authorization schemes, persistence constraints, index names, or cross-module dependencies unless they appear in the listed module files.
- Do not claim a consumer, caller, or external integration exists unless it is visible in the listed files.
- Prefer concise factual statements over expansive narrative. If the source does not support a statement, mark it ❓ or omit it.

## Readability Floor
Generated documentation must be readable by a non-implementing reviewer.
- Include a Quick Reference (TL;DR) that a Product Owner or QA reviewer can understand without reading the rest of the document.
- Include one end-to-end operational flow narrative if the source supports it.

## Unknowns Discipline
- Use ❓ for missing business intent, missing lifecycle dates, and unverifiable ownership.
- Do not use ❓ for information directly observable in the module source files. If the code answers the question, state the answer without a marker.
- If an entire section cannot be evidenced from listed files, open with NEEDS [reason] rather than generating speculative content. Do not combine ❓ and NEEDS as a compound marker.

## Quality Thresholds
Minimum quality checks before completion:
- All required sections present.
- 100 percent module file coverage in Module Files table.
- API Operations covers all controller action methods and service public methods.
- Business Rules table contains Why It Exists and Since When columns.
- Data Operations covers all business-significant reads and writes (3 columns: Database Object, Purpose, Business Context).
- Marker usage is explicit for all unknowns.

## Exclusions
Do not add these as primary content in module docs:
- Change History sections (Git is the source of truth).
- Long speculative roadmap details.
- Database object deep schema detail (link DB docs instead).
- Validation Rules sections — DataAnnotations and FluentValidation constraints are visible in source DTOs and validators; document non-obvious constraint business rationale in the Business Rules "Why It Exists" column instead.
- Full-stack ASCII layered architecture diagrams — use Integration Context tables only.
- Repository-layer method rows in API Operations — repository signatures are implementation details.

## Reference
Full charter for detailed rationale and examples:
- .akr/charters/AKR_CHARTER_BACKEND.md
