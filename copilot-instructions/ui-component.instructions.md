# AKR UI Component Condensed Instructions

Version: 2.0
Extends: .akr/charters/AKR_CHARTER.md
Source charter: .akr/charters/AKR_CHARTER_UI.md
Audience: Agent Skill GenerateDocumentation for ui-component modules

## Scope
Apply these rules when generating documentation for UI modules, including pages, reusable components, hooks, and UI utilities. Emphasize business context, confirmed gaps, interaction contracts, and accessibility issues. Do not mirror TypeScript source.

## Content Density Principles
- **Tables over prose**: Prefer structured tables for dense relational info — AI scans tables via semantic chunking; prose requires linear reading.
- **WHY-first**: Sections must lead with business context and interaction intent, not mirror component prop interfaces.
- **Code-mirror = omit**: TypeScript interfaces, hook dependency arrays, and ASCII data flow trees are first-class source artifacts. Do not reproduce them in documentation. Copilot reads source files directly.
- **Target density**: Generated docs should be approximately half the length of current baseline output, achieved by removing code-mirror content — not by compressing human-authored context.

## Required Front Matter
Every UI module document must start with YAML front matter:

```yaml
---
businessCapability: PascalCaseTagFromRegistry
feature: FN12345_US678
layer: UI
project_type: ui-component
status: draft
compliance_mode: pilot
---
```

Rules:
- businessCapability: required PascalCase taxonomy key.
- feature: required work-item format FN#####_US#####.
- layer: required (UI).
- project_type: required (ui-component unless validated otherwise).
- status: governs the generated document's maturity state, not the module grouping approval state.
	For first-generation Mode B output, set status to draft unless document-content approval has already occurred through the documented review flow.
	Do not copy modules.yaml module status directly into document front matter.
- compliance_mode: pilot or production.

## Metadata Header Requirements
Insert an AKR metadata header before body content:
- Marker: <!-- akr-generated -->
- Required fields: skill, mode, template, steps-completed, generated-at
- For section-scoped generation: generation-strategy, passes-completed, pass-timings-seconds, total-generation-seconds

## Transparency Marker Rules
Mandatory marker usage:
- 🤖 for AI-inferred behavior or UX assumptions.
- ❓ for unknown interactions, business intent, or state transitions.
- NEEDS for required but missing data.
- VERIFY for contracts that need source confirmation.
- DEFERRED only with explicit reason and owner path.

Markers must be inline and specific to the affected statement.

## Component Inventory Rules
Document all files listed in the module:
- Component/page/hook/utility file path
- Type (page, presentational component, container, hook, utility)
- Responsibility summary

Do not omit files from modules.yaml.

## Props And Contract Rules
## Component Hierarchy Rules
Document the structural composition of the module as a text/ASCII tree showing:
- Page or container root
- Child component tree with types (Container/Presentational)
- Hook attachment points at the root level

Do NOT generate per-component prop tables, exported function breakdowns, or TypeScript interface reproductions. Props interfaces are first-class source artifacts readable in .tsx files.

Exception: if a prop has a non-obvious behavioral implication that cannot be inferred from its name and type, note it in Questions & Gaps.

## State And Variant Rules
Document state behavior and visual variants:
- Default/empty/loading/error/disabled states
- Variant families (primary, secondary, etc.)
- Conditional rendering branches
- Derived state dependencies and transitions

If transitions are uncertain, mark with ❓.

## Component Hierarchy Diagram Rules
Provide text hierarchy of composition and ownership:
- Page or container root
- Child component tree
- Hook attachment points
- Data and callback flow direction

Do not use Mermaid. Use concise text/ASCII notation.

## Hook Dependency Graph Rules
## Hook Dependency Rules
Provide a summary table of custom hooks in the module: Hook | File | Purpose (one sentence) | Used By.

Do NOT generate hook call chain diagrams, ASCII dependency trees, or re-render sensitivity / memoization tables. These are derivable from source code imports and hook dependency arrays.

## Accessibility Requirements
## Accessibility Requirements
Document confirmed accessibility status and gaps only.

Include:
- **WCAG Level**: AA/AAA, or ❓ if not yet audited
- **Known Gaps table**: Gap | Missing Implementation | Impact | Needs — one row per confirmed missing implementation (e.g., missing `role="dialog"`, no focus trap, no aria-label)

Do NOT generate:
- Inferred keyboard navigation tables with per-key entries (Tab, Shift+Tab, Enter, Space, Escape) — these are standard browser behavior for native elements
- AI-synthesized screen reader announcement lists — these require actual testing, not inspection

If source shows no a11y gaps: state "No confirmed a11y gaps identified from source — NEEDS team audit for full WCAG validation."

## Data And Side Effects Rules
## Data And Side Effects Rules
Document UI-triggered API calls as a table: Action/Trigger | HTTP Method + Endpoint | Side Effect.

Do NOT generate ASCII data flow diagrams (Props→State→Render or Module Mount→Hook→API). These are code-traceable. The table format provides search-friendly, AI-scannable lookup.

Coverage must include all primary user actions: mount fetches, form submissions, and explicit CRUD triggers.

## Questions And Gaps Rules
Capture unresolved areas:
- Ambiguous UX behavior
- Missing business rule context
- Unknown accessibility intent
- Unclear ownership of components/hooks

Each unresolved item must include ❓ plus a concrete follow-up prompt.

## Section-Scoped Generation Rules
## Visual States Rules
Document module-level visual states in a table: State | Description | Visual Appearance | Interaction.
Cover all render branches: loading, success, error, empty, and any modal/form variants. Use ❓ for unconfirmed appearance details.

Do NOT generate ASCII loading flow diagrams. The States table captures the same information in a format AI can scan directly.

## Section-Scoped Generation Rules
Apply pass-based section generation discipline:
- Load only relevant charter slice for each section.
- Carry forward validated facts, not full raw context.
- Avoid full-context reload in late passes.
- Record split passes (2A/2B) in metadata if used.

## Quality Thresholds
Before completion:
- Required sections present and coherent.
- Full module file coverage in Module Files table.
- Component hierarchy diagram present in Module Files Detail.
- Component Behavior table covers all primary user actions.
- Data flow documented as API Calls table.
- Accessibility section present with WCAG level and any evidenced implementation gaps.
- No silent unknowns — all gaps explicitly marked.

## Exclusions
Do not include:
- Change History sections (Git is source of truth).
- Verbose style-token dumps with no behavioral value.
- Backend/service internals beyond dependency references.
- Per-component prop tables and TypeScript interface reproductions — props are readable from source .tsx files.
- Hook call chain ASCII diagrams and re-render sensitivity tables — derivable from source imports and hook dependency arrays.
- Type Definitions sections — TypeScript interfaces are first-class source artifacts; type contract gaps belong in Questions & Gaps.
- Component Architecture sections — composition and dependency details are captured by Module Files and Component Behavior.
- Performance Considerations sections — performance metrics require measurement, not inferred placeholders.
- Version History sections (Git is source of truth).
- Inferred keyboard navigation tables and AI-synthesized screen reader announcement lists — accessibility must be evidenced or confirmed as a gap, not synthesized.

## Reference
Full charter for rationale and examples:
- .akr/charters/AKR_CHARTER_UI.md
