---
businessCapability: [PascalCaseCapabilityName]
feature: [FEATURE_ID_US_ID]
layer: [API / Domain / Infrastructure]
project_type: api-backend
status: draft
compliance_mode: pilot
---

# Module: [Module Name]

**Module Scope**: Multi-file domain unit  
**Files in Module**: N (see Module Files section below)  
**Primary Domain Noun**: [DomainNoun]  
**Complexity**: [Simple / Medium / Complex]  
**Documentation Level**: 🔶 Baseline (70% complete)

---

## Quick Reference (TL;DR)

**What it does:**  
🤖 [AI: 1-2 sentences describing the module's primary responsibility across all files]  
❓ [HUMAN: Add business value - why does this module exist?]

**When to use it:**  
❓ [HUMAN: What scenarios trigger use of this module? Web UI? API? Background jobs?]

**Watch out for:**  
❓ [HUMAN: Critical gotcha or common mistake when using this module]

---

## Module Files

| File | Role | Primary Responsibilities |
|------|------|-------------------------|
| 🤖 `[path]/[FileName].cs` | 🤖 [Controller / Service / Repository / DTO] | 🤖 [Brief description of this file's responsibilities] |
| 🤖 `[path]/[FileName].cs` | 🤖 [Service Interface / Implementation] | 🤖 [Brief description] |
| 🤖 `[path]/[FileName].cs` | 🤖 [Repository Interface] | 🤖 [Brief description] |
| 🤖 `[path]/[FileName].cs` | 🤖 [Repository Implementation] | 🤖 [Brief description] |
| 🤖 `[path]/[FileName].cs` | 🤖 [DTO / Models] | 🤖 [Brief description] |

---

## What & Why

### Purpose

**Technical:**  
🤖 [AI: Technical description of what this module does]

**Business:**  
❓ [HUMAN: Business purpose - what problem does this module solve? Why did we build it?]

### Capabilities

🤖 [AI: Bullet list of what the module can do, spanning all files]

### Not Responsible For

🤖 [AI: What this module explicitly does NOT do]  
❓ [HUMAN: Clarify scope boundaries - what's handled elsewhere?]

---

## Module Files - Detailed Breakdown

### [FileName].cs — [Role]

**Responsibility**: 🤖 [AI: What this file accomplishes]  
**Dependencies**: 🤖 [AI: What this file depends on]  
**Consumers**: 🤖 [AI: What depends on this file]  

**Key Methods**:
| Method | Parameters | Returns | Purpose |
|--------|-----------|---------|---------|
| 🤖 `[MethodName]` | 🤖 [list] | 🤖 [type] | 🤖 [brief purpose] |

---

## Operations Map

This section covers ALL operations across ALL files in the module. Operations are grouped by public surface (API endpoints, service methods) that consumers interact with.

### Public Operations

| Operation | File | Parameters | Returns | Business Purpose |
|-----------|------|------------|---------|-----------------|
| 🤖 `[MethodName]` | 🤖 `[FileName].cs` | 🤖 [parameter list] | 🤖 [return type] | 🤖 [business purpose] |
| 🤖 `[MethodName]` | 🤖 `[FileName].cs` | 🤖 [parameter list] | 🤖 [return type] | 🤖 [business purpose] |

### Internal Operations (for module completeness)

| Operation | File | Purpose | Called By |
|-----------|------|---------|-----------|
| 🤖 `[PrivateMethod]` | 🤖 `[FileName].cs` | 🤖 [purpose] | 🤖 [which public operation calls it] |
| 🤖 `[PrivateMethod]` | 🤖 `[FileName].cs` | 🤖 [purpose] | 🤖 [which public operation calls it] |

---

## How It Works

### Primary Operation: [Main Method Name]

**Purpose:**  
🤖 [AI: What this method accomplishes]  
❓ [HUMAN: Business context - why do we need this operation?]

**Input:**  
🤖 [AI: Parameters and types]

**Output:**  
🤖 [AI: Return type and success/failure scenarios]

**Step-by-Step Flow (Across All Module Files):**

```
┌──────────────────────────────────────────────────────────────┐
│ Step 1: [Action] - [FileName].cs                            │
│  What  → 🤖 [AI: Technical action taken]                     │
│  Why   → ❓ [HUMAN: Business reason for this step]           │
│  Error → 🤖 [AI: What errors can occur]                      │
│         ❓ [HUMAN: Business impact of error]                 │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 2: [Action] - [FileName].cs                            │
│  What  → 🤖 [AI: Technical action taken]                     │
│  Why   → ❓ [HUMAN: Business reason for this step]           │
│  Error → 🤖 [AI: What errors can occur]                      │
│         ❓ [HUMAN: Business impact of error]                 │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 3: [Action] - [FileName].cs                            │
│  What  → 🤖 [AI: Technical action taken]                     │
│  Why   → ❓ [HUMAN: Business reason for this step]           │
│  Error → 🤖 [AI: What errors can occur]                      │
│         ❓ [HUMAN: Business impact of error]                 │
└──────────────────────────────────────────────────────────────┘
                          ↓
                    [SUCCESS] or [FAILURE]
```

**Success Path:**  
🤖 [AI: What happens on successful completion]

**Failure Paths:**  
🤖 [AI: What errors can occur and when]  
❓ [HUMAN: Business implications of each failure]

---

## Architecture Overview

### Full-Stack Module Architecture

```
┌─────────────────────────────────────┐
│ API Layer - Entry Point             │
│ [Controller Name]                   │
│ └─ Receives HTTP requests           │
│ └─ Validates input parameters       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Service Layer - Business Logic      │
│ [ServiceInterface]                  │
│ ├─ Defines contract                 │
│ └─ [ServiceImplementation]          │
│    └─ Enforces business rules       │
│    └─ Orchestrates operations       │
│    └─ Handles error scenarios       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Repository Layer - Data Abstraction │
│ [RepositoryInterface]               │
│ ├─ Defines data contract            │
│ └─ [EfRepositoryImplementation]     │
│    └─ Queries database              │
│    └─ Maps ORM entities to DTOs     │
│    └─ Handles database errors       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Data Layer - Persistence            │
│ [DatabaseTable]                     │
│ └─ Stores entity data               │
│ └─ Enforces constraints             │
└─────────────────────────────────────┘
```

### Module Composition

🤖 [AI: Explanation of how the files in this module work together]

---

## Business Rules

| Rule | Why It Exists | Since When | Where Enforced |
|------|---------------|------------|----------------|
| 🤖 **BR-[MOD]-001** | 🤖 [AI: Rule description from code] | ❓ [HUMAN: When added] | 🤖 [AI: Service/Validator/DB - where checked?] |
| 🤖 **BR-[MOD]-002** | 🤖 [AI: Rule description from code] | ❓ [HUMAN: When added] | 🤖 [AI: Service/Validator/DB - where checked?] |
| 🤖 **BR-[MOD]-003** | 🤖 [AI: Rule description from code] | ❓ [HUMAN: When added] | 🤖 [AI: Service/Validator/DB - where checked?] |

**Rule ID Format:** BR-[ModuleAbbreviation]-### (e.g., BR-CRS-001 for Course module)

**Enforcement Points** (per rule above):
- `Service`: Enforced in service layer before data operations
- `Validator`: Enforced in FluentValidation validators
- `DB`: Enforced as database constraints (unique, foreign key, check)

---

## Architecture

### Where This Module Fits in the System

```
┌────────────────────────────────────────┐
│ API Gateway / HTTP Entry Point         │
└────────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────┐
│ THIS MODULE ([ModuleName])             │
│ ► Entry: [ControllerName]              │
│ ► Business: [ServiceInterface]         │
│ ► Data: [RepositoryInterface]          │
│ ► Persistence: [DatabaseTable]         │
└────────────────────────────────────────┘
                   ↓
┌────────────────────────────────────────┐
│ Related Modules (Dependencies)         │
│ ├─ [Module A] - for [purpose]         │
│ └─ [Module B] - for [purpose]         │
└────────────────────────────────────────┘
```

### Dependencies (What This Module Needs)

| Dependency | Purpose | Failure Mode | Critical? |
|------------|---------|--------------|-----------|
| 🤖 `I[DependencyName]` | 🤖 [AI: What it's used for] | 🤖 [AI: What exception occurs] | ❓ [HUMAN: Blocking? Can module degrade?] |
| 🤖 `I[DependencyName]` | 🤖 [AI: What it's used for] | 🤖 [AI: What exception occurs] | ❓ [HUMAN: Fallback available?] |

### Consumers (Who Uses This Module)

| Consumer | Use Case | Impact of Failure |
|----------|----------|-------------------|
| 🤖 [Controller/Service name] | 🤖 [AI: How they use it] | ❓ [HUMAN: User-facing? Background?] |
| 🤖 [Controller/Service name] | 🤖 [AI: How they use it] | ❓ [HUMAN: What breaks if this fails?] |

---

## API Contract (AI Context)

> 📋 **Interactive Documentation:** [API Portal - [ModuleName]](https://apim.gateway.emerson.com/...) — use for testing
> 
> **Purpose:** This section provides AI assistants (Copilot) with API context for this module.
> **Sync Status:** Last verified on ❓ [HUMAN: Date]

### Endpoints

🤖 [AI: Extract from ApiRoutes.cs and controller [Http*] attributes - module-specific endpoints only]

| Method | Route | Purpose | Auth |
|--------|-------|---------|------|
| 🤖 `GET` | 🤖 `/v1/[resource]` | 🤖 Get all | 🤖 Yes |
| 🤖 `GET` | 🤖 `/v1/[resource]/{id}` | 🤖 Get by ID | 🤖 Yes |
| 🤖 `POST` | 🤖 `/v1/[resource]` | 🤖 Create | 🤖 Yes |
| 🤖 `PUT` | 🤖 `/v1/[resource]/{id}` | 🤖 Update | 🤖 Yes |
| 🤖 `DELETE` | 🤖 `/v1/[resource]/{id}` | 🤖 Delete | 🤖 Yes |

### Request Example

🤖 [AI: Generate realistic examples from DTOs]

```json
{
  "propertyName": "🤖 [AI: Realistic value based on property domain semantics]",
  "propertyId": "🤖 [AI: Smart value, respecting type and constraints]",
  "isActive": true
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| 🤖 `propertyName` | 🤖 `string` | 🤖 Yes | 🤖 [AI: Business purpose of field] |
| 🤖 `propertyId` | 🤖 `int` | 🤖 Yes | 🤖 [AI: Business purpose of field] |
| 🤖 `isActive` | 🤖 `bool` | 🤖 No | 🤖 [AI: Default behavior and purpose] |

### Success Response Example (200)

🤖 [AI: Generate from response DTO]

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "propertyName": "value",
  "createdDate": "2024-01-01T00:00:00Z"
}
```

### Error Response Example

🤖 [AI: Extract from error model classes]

```json
{
  "statusCode": 400,
  "message": "Validation failed.",
  "validationErrors": [
    { "fieldName": "propertyName", "message": "Required" }
  ]
}
```

---

## Validation Rules

🤖 [AI: Extract from *Validator.cs FluentValidation classes]

| Property | Rule | Error Message |
|----------|------|---------------|
| 🤖 `[Property]` | 🤖 `NotEmpty()` | 🤖 "[Property] is required" |
| 🤖 `[Property]` | 🤖 `MaximumLength(N)` | 🤖 "Cannot exceed N characters" |

❓ [HUMAN: Add business rationale for non-obvious validation rules]

---

## Data Operations

### Reads From

| Database Object | Purpose | Business Context | Performance Notes |
|-----------------|---------|------------------|-------------------|
| 🤖 `schema.TableName` | 🤖 [What data retrieved, which columns] | ❓ [HUMAN: Why needed? Business rule context] | 🤖 [AI: Query pattern, indexes, optimization hints] |

---

### Writes To

| Database Object | Purpose | Business Context | Performance Notes |
|-----------------|---------|------------------|-------------------|
| 🤖 `schema.TableName` | 🤖 [Which columns modified by this module] | ❓ [HUMAN: What business event triggers this?] | 🤖 [AI: Transaction scope] ❓ [HUMAN: High volume? Indexing needs?] |

---

## Failure Modes & Exception Handling

### Common Failure Scenarios

| Exception Type | Trigger | Operation | Impact | Mitigation |
|---|---|---|---|---|
| 🤖 `InvalidOperationException` | 🤖 [What causes it] | 🤖 [Which operation fails] | 🤖 [Business consequence] | 🤖 [How module handles it] |
| 🤖 `DbUpdateException` | 🤖 [DB constraint violated] | 🤖 [Which write operation fails] | 🤖 [Data not persisted] | 🤖 [Retry? Rollback? User message?] |

---

## Questions & Gaps

### AI-Flagged Questions

🤖 [AI will identify unclear logic, magic numbers, assumptions]

### Human-Flagged Questions

❓ [HUMAN: Add questions you have while reviewing]

---

## Maintenance Checklist

**When making code changes to this module:**

- [ ] Update this documentation if behavior changes
- [ ] Update Operations Map if operations added/removed
- [ ] Update Module Files if new files added to module
- [ ] Update business rules table if validation logic changes
- [ ] Update flow diagram if steps added/removed
- [ ] Update "Questions & Gaps" if resolving unknowns

---

## Related Documentation

**Other Modules:** Link to related module docs:
- `[ModuleName](./[ModuleName]_module_doc.md)`

**Database Tables:** See database documentation:
- `[Table Name](../../database-repo/docs/tables/TableName_doc.md)`

**API Endpoints:** See API Reference Database: [Link to your API docs system]

---

## Change History

**Module evolution is tracked in Git**, not in this document.

```bash
# View all changes to this documentation file
git log docs/modules/[ModuleName]_module_doc.md

# View changes with diffs
git log -p docs/modules/[ModuleName]_module_doc.md

# Search for specific business rule or feature
git log --grep="BR-[MOD]" docs/modules/[ModuleName]_module_doc.md
git log --grep="FN#####" docs/modules/[ModuleName]_module_doc.md
```


