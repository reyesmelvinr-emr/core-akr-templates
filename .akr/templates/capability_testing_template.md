# Test Conditions - {{BusinessCapabilityPascalCase}}

This file contains detailed QA-maintained procedures for the operational scenarios listed in `index.md`.

Scenario cross-reference:

- `SCN-{{CapabilityCode}}-001` -> `TC-{{CapabilityCode}}-001`
- `SCN-{{CapabilityCode}}-002` -> `TC-{{CapabilityCode}}-002`
- `SCN-{{CapabilityCode}}-003` -> `TC-{{CapabilityCode}}-003`

| Condition ID | Scenario ID | Scenario | Preconditions | Expected Outcome | Priority |
|---|---|---|---|---|---|
| TC-{{CapabilityCode}}-001 | SCN-{{CapabilityCode}}-001 | {{ScenarioName1}} | {{Precondition1}} | {{ExpectedOutcome1}} | High |
| TC-{{CapabilityCode}}-002 | SCN-{{CapabilityCode}}-002 | {{ScenarioName2}} | {{Precondition2}} | {{ExpectedOutcome2}} | High |
| TC-{{CapabilityCode}}-003 | SCN-{{CapabilityCode}}-003 | {{ScenarioName3}} | {{Precondition3}} | {{ExpectedOutcome3}} | High |

## Detailed Test Steps

### TC-{{CapabilityCode}}-001 (SCN-{{CapabilityCode}}-001)

1. {{Step1_1}}
2. {{Step1_2}}
3. {{Step1_3}}
4. {{Step1_4}}
5. {{Step1_5}}

Additional validation checks:

- {{Check1_1}}
- {{Check1_2}}
- {{Check1_3}}

### TC-{{CapabilityCode}}-002 (SCN-{{CapabilityCode}}-002)

1. {{Step2_1}}
2. {{Step2_2}}
3. {{Step2_3}}
4. {{Step2_4}}
5. {{Step2_5}}

Additional validation checks:

- {{Check2_1}}
- {{Check2_2}}
- {{Check2_3}}

### TC-{{CapabilityCode}}-003 (SCN-{{CapabilityCode}}-003)

1. {{Step3_1}}
2. {{Step3_2}}
3. {{Step3_3}}
4. {{Step3_4}}
5. {{Step3_5}}

Additional validation checks:

- {{Check3_1}}
- {{Check3_2}}
- {{Check3_3}}

## Extended Coverage Conditions

Add conditions for non-core risk areas and keep ID continuity.

Example IDs:

- `TC-{{CapabilityCode}}-004` field boundary validation
- `TC-{{CapabilityCode}}-005` pagination/default behavior
- `TC-{{CapabilityCode}}-006` accessibility and error communication

### TC-{{CapabilityCode}}-004 (SCN-{{CapabilityCode}}-004)

1. {{Step4_1}}
2. {{Step4_2}}
3. {{Step4_3}}

Additional validation checks:

- {{Check4_1}}
- {{Check4_2}}

### TC-{{CapabilityCode}}-005 (SCN-{{CapabilityCode}}-005)

1. {{Step5_1}}
2. {{Step5_2}}
3. {{Step5_3}}

Additional validation checks:

- {{Check5_1}}
- {{Check5_2}}

### TC-{{CapabilityCode}}-006 (SCN-{{CapabilityCode}}-006)

1. {{Step6_1}}
2. {{Step6_2}}
3. {{Step6_3}}

Additional validation checks:

- {{Check6_1}}
- {{Check6_2}}

## Initial QA Focus Areas

- Duplicate identifier conflicts in create and update flows.
- Field validation boundaries (required fields, length, range, formatting).
- Defaulting or normalization behavior for invalid user/system inputs.
- Delete behavior and dependency impact validation.
- Create/edit modal or form workflow behavior.
- Accessibility checks for modal semantics, focus management, and error communication.

## Maintenance Rules

- `index.md` remains the canonical source for scenario IDs and descriptions.
- `test-conditions.md` contains executable QA detail linked to those scenario IDs.
- Every condition must reference a scenario ID.
- When adding a new scenario in `index.md`, add a corresponding condition ID here.
