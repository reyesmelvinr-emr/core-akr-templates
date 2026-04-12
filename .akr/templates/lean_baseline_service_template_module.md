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

<!-- akr:section id="quick_reference" required=true order=1 authorship="mixed" human_columns="business_outcome,specific_caller,watch_out" -->
## Quick Reference (TL;DR)

**What it does:**  
🤖 [AI: 1-2 sentences describing the module's primary responsibility across all files]  
❓ [HUMAN: Cite the specific business outcome this module enables — do not infer from module name alone]

**When to use it:**  
❓ [HUMAN: Name the actual caller — UI page, background job, or specific API client — do not guess]

**Watch out for:**  
❓ [HUMAN: Cite a specific code path or error scenario — do not infer from module name alone]

---

<!-- akr:section id="module_files" required=true order=2 authorship="ai" -->
## Module Files

| File | Role | Primary Responsibilities |
|------|------|-------------------------|
| 🤖 `[path]/[FileName].cs` | 🤖 [Controller / Service / Repository / DTO] | 🤖 [Brief description of this file's responsibilities] |
| 🤖 `[path]/[FileName].cs` | 🤖 [Service Interface / Implementation] | 🤖 [Brief description] |
| 🤖 `[path]/[FileName].cs` | 🤖 [Repository Interface] | 🤖 [Brief description] |
| 🤖 `[path]/[FileName].cs` | 🤖 [Repository Implementation] | 🤖 [Brief description] |
| 🤖 `[path]/[FileName].cs` | 🤖 [DTO / Models] | 🤖 [Brief description] |

---

<!-- akr:section id="purpose_scope" required=true order=3 authorship="mixed" human_columns="business_purpose,scope_boundaries" -->
## Purpose and Scope

### Business Purpose
❓ [HUMAN: Business purpose — what problem does this module solve? Why did we build it? What business outcome does it enable?]

### Not Responsible For

🤖 [AI: What this module explicitly does NOT do — list other modules/systems that handle out-of-scope concerns]

---

<!-- akr:section id="api_operations" required=true order=4 authorship="ai" -->
## API Operations

Controller action methods and service public methods — the HTTP/service public contract boundary. Repository-layer methods are implementation details; read the source directly.

| Operation | Layer | File | Parameters | Returns | Business Purpose |
|-----------|-------|------|------------|---------|-----------------|
| 🤖 `[ActionMethod]` | Controller | 🤖 `[Controller].cs` | 🤖 [HTTP params + body type] | 🤖 [ActionResult type] | 🤖 [what this endpoint does] |
| 🤖 `[ServiceMethod]` | Service | 🤖 `[Service].cs` | 🤖 [parameter list] | 🤖 [return type] | 🤖 [business purpose] |

---

<!-- akr:section id="how_it_works" required=true order=5 authorship="mixed" human_columns="business_context,failure_impact" -->
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

<!-- akr:section id="integration_context" required=true order=6 authorship="mixed" human_columns="critical,consumer_impact" -->
## Integration Context

<!-- conditional: omit Dependencies heading if no external interface dependencies are visible in listed module files -->
### Dependencies (What This Module Needs)

| Dependency | Purpose | Failure Mode | Critical? |
|------------|---------|--------------|-----------|
| 🤖 `I[DependencyName]` | 🤖 [AI: What it's used for] | 🤖 [AI: What exception or null result occurs] | ❓ [HUMAN: Blocking? Can module degrade gracefully?] |

<!-- conditional: if no actual callers are visible in listed module files, omit this heading and table entirely — do not guess from module name -->
### Consumers (Who Uses This Module)

| Consumer | Use Case | Impact of Failure |
|----------|----------|-------------------|
| 🤖 [Caller name — only if visible in source] | 🤖 [How they use it] | ❓ [HUMAN: User-facing? Background? Blocking?] |

---

<!-- akr:section id="business_rules" required=true order=7 authorship="mixed" human_columns="why_it_exists,since_when" -->
## Business Rules

| Rule | Why It Exists | Since When | Where Enforced |
|------|---------------|------------|----------------|
| 🤖 **BR-[MOD]-001** | 🤖 [AI: Rule description from code] | ❓ [HUMAN: Exact date or sprint — do not estimate] | 🤖 [AI: Service/Validator/DB - where checked?] |
| 🤖 **BR-[MOD]-002** | 🤖 [AI: Rule description from code] | ❓ [HUMAN: Exact date or sprint — do not estimate] | 🤖 [AI: Service/Validator/DB - where checked?] |
| 🤖 **BR-[MOD]-003** | 🤖 [AI: Rule description from code] | ❓ [HUMAN: Exact date or sprint — do not estimate] | 🤖 [AI: Service/Validator/DB - where checked?] |

**Rule ID Format:** BR-[ModuleAbbreviation]-### (e.g., BR-CRS-001 for Course module)

**Enforcement Points** (per rule above):
- `Service`: Enforced in service layer before data operations
- `Validator`: Enforced in FluentValidation validators
- `DB`: Enforced as database constraints (unique, foreign key, check)

---

<!-- conditional: include only if module contains a controller with [Http*] attributes or explicit external DTO contracts visible in listed module files -->
<!-- akr:section id="api_contract" required=false order=8 condition="controller_with_http_attributes" authorship="ai" -->
## API Contract (AI Context)

> 📋 **Interactive Documentation:** `[swagger-url]` (local: `https://localhost:5001/swagger`) — use for testing and request/response examples.
> **Sync Status:** Last verified on ❓ [HUMAN: Date]

### Endpoints
| Method | Route | Purpose | Auth |
|--------|-------|---------|------|
| 🤖 `GET` | 🤖 `[route]` | 🤖 [List/paginated retrieval] | ❓ |
| 🤖 `GET` | 🤖 `[route]/{id}` | 🤖 [Single record retrieval] | ❓ |
| 🤖 `POST` | 🤖 `[route]` | 🤖 [Create] | ❓ |
| 🤖 `PUT` | 🤖 `[route]/{id}` | 🤖 [Update] | ❓ |
| 🤖 `DELETE` | 🤖 `[route]/{id}` | 🤖 [Delete] | ❓ |

---

<!-- akr:section id="data_operations" required=true order=9 authorship="mixed" human_columns="business_context" -->
## Data Operations

### Reads From

| Database Object | Purpose | Business Context |
|-----------------|---------|------------------|
| 🤖 `schema.TableName` | 🤖 [What data is retrieved and why] | ❓ [HUMAN: Why needed? Business rule context] |

---

### Writes To

| Database Object | Purpose | Business Context |
|-----------------|---------|------------------|
| 🤖 `schema.TableName` | 🤖 [What is written and under what condition] | ❓ [HUMAN: What business event triggers this?] |

### Side Effects
🤖 [State any email, event, notification, or queue side effects; or: "No email, event, or queue side effects in this module."]

---

<!-- akr:section id="failure_modes" required=true order=10 authorship="ai" -->
## Failure Modes & Exception Handling

Document only exceptions this module explicitly catches and handles with domain-specific responses. Standard framework exceptions that propagate unchanged to global middleware (e.g., `DbUpdateException` → `ExceptionHandlingMiddleware`) do not belong here.

### Module-Handled Failures

| Exception Type | Trigger | Operation | HTTP Response | Business Impact |
|---|---|---|---|---|
| 🤖 `[ExceptionType]` | 🤖 [What causes it] | 🤖 [Which operation catches it] | 🤖 [HTTP status + body] | 🤖 [Business consequence to caller] |

---

<!-- akr:section id="questions_gaps" required=true order=12 authorship="human" -->
<!-- akr:section id="questions_gaps" required=true order=11 authorship="human" -->
## Questions & Gaps

### AI-Flagged Questions
🤖 [AI will identify unclear logic, magic numbers, assumptions]

### Human-Flagged Questions

❓ [HUMAN: Add questions you have while reviewing]

---


<!-- conditional: include only if doc_output paths for related modules are present in modules.yaml -->
<!-- akr:section id="related_documentation" required=false order=12 authorship="ai" -->
## Related Documentation

**Other Modules:** Link to related module docs (confirmed paths from modules.yaml only):
- `[ModuleName](./[ModuleName]_module_doc.md)`

**Database Tables:** See database documentation:
- `[Table Name](../../database-repo/docs/tables/TableName_doc.md)`



