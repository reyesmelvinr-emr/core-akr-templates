---
businessCapability: {{BusinessCapabilityPascalCase}}
status: draft
audience: ProductOwner, QualityAssuranceTester, TechnicalLead
source_repositories:
  - {{SourceRepositoryA}}
  - {{SourceRepositoryB}}
source_documents:
  - {{SourceDocumentPathA}}
  - {{SourceDocumentPathB}}
generated_by: capability-consolidation
generated_at: {{YYYY-MM-DD}}
---

# {{BusinessCapabilityPascalCase}}

## Capability Summary

{{BusinessCapabilityPascalCase}} governs how the organization manages {{BusinessDomainOutcome}} across the application.

This capability provides one business flow across layers:

- UI behavior: {{UISummary}}
- API behavior: {{APISummary}}
- Data behavior: {{DataSummary}}

Primary business outcome:

- {{PrimaryBusinessOutcome}}

## Business Scope

In scope:

- {{InScopeItem1}}
- {{InScopeItem2}}
- {{InScopeItem3}}

Out of scope:

- {{OutOfScopeItem1}}
- {{OutOfScopeItem2}}
- {{OutOfScopeItem3}}

## End-to-End Behavior (Business View)

```text
{{PrimaryBusinessActor}}
  -> {{Step1}}
  -> {{Step2}}
  -> {{Step3}}
  -> {{Step4}}
  -> {{Step5}}
```

## Consolidated Business Rules

| Rule ID | Rule | Why it matters to the business | Source confidence |
|---|---|---|---|
| BR-{{CapabilityCode}}-001 | {{RuleStatement1}} | {{BusinessReason1}} | Confirmed |
| BR-{{CapabilityCode}}-002 | {{RuleStatement2}} | {{BusinessReason2}} | Confirmed |
| BR-{{CapabilityCode}}-003 | {{RuleStatement3}} | {{BusinessReason3}} | Needs-Review |

## User and Stakeholder Experience

### Product Owner view

- {{POExpectation1}}
- {{POExpectation2}}

### QA tester view

- {{QAExpectation1}}
- {{QAExpectation2}}

### Technical Lead view

- {{TLExpectation1}}
- {{TLExpectation2}}

## Field Dictionary (PO/Business View)

Use this section to describe user-visible fields from the UI screenshot(s) and source module documentation.

### A. Table/List fields

| Field Name | Where user sees it | Business meaning | Why it matters |
|---|---|---|---|
| {{ListField1}} | {{ListLocation1}} | {{ListMeaning1}} | {{ListWhy1}} |
| {{ListField2}} | {{ListLocation2}} | {{ListMeaning2}} | {{ListWhy2}} |

### B. Form fields (Add/Edit)

| Field Name | Business description | Typical PO/business usage |
|---|---|---|
| {{FormField1}} | {{FormDescription1}} | {{FormUsage1}} |
| {{FormField2}} | {{FormDescription2}} | {{FormUsage2}} |

### C. Supporting summary indicators

| Indicator | Business interpretation |
|---|---|
| {{Indicator1}} | {{IndicatorMeaning1}} |
| {{Indicator2}} | {{IndicatorMeaning2}} |

Field governance note:

- Product Owner validates naming standards and allowed taxonomy usage for key fields.
- QA verifies field consistency across create, update, and list flows.

## Operational Scenarios

Detailed step-by-step QA procedures are maintained in `test-conditions.md`.

Reference model used across files:

- `index.md` is the primary source of truth for scenario IDs and scenario descriptions.
- Scenario IDs: `SCN-{{CapabilityCode}}-001` through `SCN-{{CapabilityCode}}-999`
- QA condition IDs in `test-conditions.md` include the related scenario ID.

### SCN-{{CapabilityCode}}-001: {{ScenarioName1}}

Summary:

- {{ScenarioSummary1}}

Expected result:

- {{ScenarioExpected1}}
- Detailed QA steps: see `TC-{{CapabilityCode}}-001` in `test-conditions.md`.

### SCN-{{CapabilityCode}}-002: {{ScenarioName2}}

Summary:

- {{ScenarioSummary2}}

Expected result:

- {{ScenarioExpected2}}
- Detailed QA steps: see `TC-{{CapabilityCode}}-002` in `test-conditions.md`.

### SCN-{{CapabilityCode}}-003: {{ScenarioName3}}

Summary:

- {{ScenarioSummary3}}

Expected result:

- {{ScenarioExpected3}}
- Detailed QA steps: see `TC-{{CapabilityCode}}-003` in `test-conditions.md`.

## Known Constraints and Open Items

| Item | Impact | Owner |
|---|---|---|
| {{Constraint1}} | {{ConstraintImpact1}} | {{ConstraintOwner1}} |
| {{Constraint2}} | {{ConstraintImpact2}} | {{ConstraintOwner2}} |

## Source Evidence

- Backend source: {{BackendSourcePath}}
- UI source: {{UISourcePath}}

## Change Control

Update this document when one or more of the following changes occur:

- Business policy for the capability changes.
- Validation rules change in API contracts.
- UI workflow changes affect operational behavior.
- Data persistence behavior changes affect reporting or traceability.
