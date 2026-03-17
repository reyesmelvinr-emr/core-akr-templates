# AKR Database Condensed Instructions

Version: 1.0
Extends: .akr/charters/AKR_CHARTER.md
Source charter: .akr/charters/AKR_CHARTER_DB.md
Audience: Agent Skill Mode B for database object docs

## Scope
Apply these rules to database objects such as tables, views, procedures, functions, and schema-scoped objects. Focus on structure, relationships, usage behavior, constraints, and operational risk.

## Required Front Matter
Database object docs require YAML front matter:

```yaml
---
object_type: table
source: db/schema/object.sql
status: draft
compliance_mode: pilot
feature: FN12345_US678
businessCapability: PascalCaseTagFromRegistry
---
```

Rules:
- object_type and source are mandatory for DB docs.
- feature and businessCapability remain required for traceability consistency.
- status and compliance_mode must reflect lifecycle state.

## Metadata Header Requirements
Insert AKR metadata header before section content:
- Marker: <!-- akr-generated -->
- Required fields: skill, mode, template, steps-completed, generated-at
- Add generation pass fields when section-scoped generation is used.

## Transparency Marker Rules
Use markers consistently:
- 🤖 inferred database behavior.
- ❓ unknown cardinality, lineage, or operational assumptions.
- NEEDS required schema details unavailable in source.
- VERIFY assumptions that need SQL/source confirmation.
- DEFERRED with justification for postponed validation.

## Object Definition Requirements
Object Definition section is mandatory and must include:
- Object name and schema
- Object type (table/view/procedure/function)
- Core structure summary
- Columns/parameters with data type and nullability where applicable

For procedures/functions include parameters and return behavior.

## Relationships And Dependencies Requirements
This section is mandatory and must include:
- Foreign key or dependency links
- Upstream and downstream consumers
- Dependency type (read, write, execute, join, trigger)
- Known coupling risks

If a dependency is uncertain, record it with ❓.

## Usage Patterns Requirements
This section is mandatory and must include:
- Typical read and write usage patterns
- Frequency/criticality notes if known
- Operational scenarios (batch, realtime, reporting, admin)
- Error/failure considerations

## Naming And Convention Checks
Apply condensed naming guidance:
- Tables: PascalCase plural noun
- Views: vw_ prefix
- Procedures: usp_ prefix (avoid sp_)
- Scalar function: fn_ prefix
- Table-valued function: tvf_ prefix
- Primary and foreign key naming must be explicit and consistent

Document deviations and whether intentional.

## Constraint And Index Coverage
When available, include:
- Primary/foreign/unique/check/default constraints
- Indexes tied to key query patterns
- Business-critical constraint rationale

If details are missing, mark as NEEDS or ❓ with follow-up.

## Data Lifecycle And Audit Notes
Capture lifecycle behavior where present:
- Created/updated/deleted tracking columns
- Soft delete strategy if applicable
- Retention/archival behavior
- Migration implications and backward compatibility notes

## Questions And Gaps Rules
Capture unresolved DB questions explicitly:
- Unknown constraint rationale
- Missing relationship context
- Ambiguous ownership of schema changes
- Unverified migration assumptions

Each item must include ❓ and a clear follow-up action.

## Section-Scoped Generation Rules
For pass-based generation:
- Load only relevant DB charter slice per section.
- Carry forward schema facts and unresolved items.
- Avoid full-source reload in late passes unless required override is documented.

## Quality Thresholds
Before completion:
- Object Definition, Relationships and Dependencies, and Usage Patterns all present.
- Front matter is complete and valid.
- Dependencies and operational behavior are explicit.
- Unknowns are marked with approved transparency markers.

## Exclusions
Do not include:
- Change History sections in docs.
- Full DDL dumps when concise object summary is sufficient.
- Non-database implementation detail that belongs in backend/UI docs.

## Reference
Full charter for detailed rules and examples:
- .akr/charters/AKR_CHARTER_DB.md
