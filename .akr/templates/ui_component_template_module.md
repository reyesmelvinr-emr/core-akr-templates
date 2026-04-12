---
businessCapability: [PascalCaseCapabilityName]
feature: [FEATURE_ID_US_ID]
layer: UI
project_type: ui-component
status: draft
compliance_mode: pilot
---

# UI Module: [Module Name]

**Module Scope**: Multi-component domain unit  
**Components in Module**: N (see Module Files section below)  
**Primary Domain Noun**: [DomainNoun]  
**Complexity**: [Simple / Medium / Complex]  
**Documentation Level**: 🔶 Baseline (70% complete)

---

<!-- akr:section id="quick_reference" required=true order=1 authorship="mixed" human_columns="accessibility,business_context" -->
## Quick Reference

| | |
|---|---|
| **What it does** | 🤖 _Brief 1-sentence description of module's purpose across all components_ |
| **When to use** | 🤖 _Situations where this module is appropriate_ |
| **When NOT to use** | 🤖 _Alternative components/modules for different scenarios_ |
| **Accessibility** | ❓ _WCAG level (AA/AAA), keyboard nav, screen reader tested?_ |
| **Status** | 🤖 _Stable / Beta / Experimental / Deprecated_ |

**Example usage**:
```tsx
🤖 // Simple copy-paste example of module entry point
import { [PrimaryComponent] } from '@/components/[path]/[PrimaryComponent]';

<[PrimaryComponent]
  propName="value"
  onAction={handleAction}
>
  Content

---

<!-- akr:section id="module_files" required=true order=2 authorship="ai" -->
## Module Files

| File | Type | Role | Primary Responsibilities |
|------|------|------|-------------------------|
| 🤖 `[path]/[ComponentName].tsx` | 🤖 [Page / Container / Presentational] | 🤖 [Primary | Supporting] | 🤖 [Brief description] |
| 🤖 `[path]/[ComponentName].tsx` | 🤖 [Container / Presentational] | 🤖 [Supporting] | 🤖 [Brief description] |
| 🤖 `[path]/[ComponentName].tsx` | 🤖 [Presentational] | 🤖 [Supporting] | 🤖 [Brief description] |
| 🤖 `[path]/hooks/use[Hook].ts` | 🤖 [Custom Hook] | 🤖 [Data/State] | 🤖 [Brief description] |
| 🤖 `[path]/types.ts` | 🤖 [TypeScript types] | 🤖 [Shared Types] | 🤖 [Interfaces, types, constants] |

**Module Grouping Principle:**  
All components in this module are part of the same domain noun ([DomainNoun]) and work together to provide a complete feature. Components are grouped by:
- Domain noun identity (what business entity they operate on)
- Functional cohesion (components that work together stay together)
- Hook/utility sharing (custom hooks for this domain only)
- Type definitions (interfaces unique to this module)

---

<!-- akr:section id="purpose_context" required=true order=3 authorship="mixed" human_columns="business_context" -->
## Purpose & Context

### What This Module Does

🤖 _Detailed description (2-3 sentences):_
- What problem does it solve?
- What is its primary responsibility?
- How does it fit into the larger application?

❓ _Enhance with business context:_
- Why was this module created?
- What business need does it address?
- What user stories does it support?

---

### When to Use This Module

🤖 _List 3-5 use cases:_

**Use this module when:**
- Use case 1 (example: displaying course catalog with filtering)
- Use case 2 (example: user needs to browse and enroll in courses)
- Use case 3 (example: admin needs to manage course listings)

❓ _Enhance with real application examples:_
- Course catalog page (primary use case)
- Admin panel (secondary use case)
- Mobile app (if applicable)

---

### When NOT to Use This Module

🤖 _List alternatives:_

**Don't use this module when:**
- Scenario 1 → Use [AlternativeModule] instead
- Scenario 2 → Use [OtherModule] instead
- Scenario 3 → Build custom solution because...

---

<!-- akr:section id="module_files_detail" required=true order=4 authorship="ai" -->
## Module Files Detail

### Component Hierarchy

```
[PrimaryComponent] (Page/Container)
├── [SupportingComponent1] (Container/Presentational)
│   ├── [ChildComponent1] (Presentational)
│   └── [ChildComponent2] (Presentational)
├── [SupportingComponent2] (Container)
│   └── [ChildComponent3] (Presentational)
└── [UtilityComponent] (Presentational)
```

Hooks attached at page/container level:
- `use[HookName]({ [key params] })` — [one-line purpose]

> Props and component interfaces are in source .tsx files. For non-obvious behavioral implications (prop values that gate conditional rendering, enum-validated constants), note them in Questions & Gaps.

---

<!-- akr:section id="hook_dependency" required=true order=5 authorship="ai" -->
## Hook Dependency

### Custom Hooks in This Module

| Hook | File | Purpose | Used By |
|------|------|---------|---------|
| 🤖 `use[HookName]` | 🤖 `hooks/use[Hook].ts` | 🤖 [Data fetching / state management — one sentence] | 🤖 [Which components call it] |

---

<!-- akr:section id="component_behavior" required=true order=6 authorship="human" -->
## Component Behavior

### User Interactions (Module Level)

| User Action | Primary Component Response | Affected Components | Side Effects |
|------------|--------------------------|-------------------|--------------|
| ❓ Click/Tap | ❓ What happens in primary component | ❓ Which child components update | ❓ State changes, API calls |
| ❓ Scroll | ❓ Module behavior | ❓ Components affected | ❓ Pagination, loading more? |
| ❓ Keyboard | ❓ Navigation within module | ❓ Components receiving focus | ❓ State updates |

---

<!-- akr:section id="data_flow" required=true order=7 authorship="ai" -->
## Data Flow

### API Calls

| Action / Trigger | HTTP Method + Endpoint | Side Effect |
|------------------|------------------------|-------------|
| 🤖 [Module mount / initial load] | 🤖 `GET [endpoint]` | 🤖 [State updated, table/list rendered] |
| 🤖 [User action — e.g., create form submit] | 🤖 `POST [endpoint]` | 🤖 [Resource created, list refetched] |
| 🤖 [User action — e.g., edit form submit] | 🤖 `PUT [endpoint]/{id}` | 🤖 [Resource updated, list refetched] |
| 🤖 [User action — e.g., delete] | 🤖 `DELETE [endpoint]/{id}` | 🤖 [Resource removed, list refetched] |

---

<!-- akr:section id="visual_states" required=true order=8 authorship="human" -->
## Visual States

### States

| State | Description | Visual Appearance | Interaction |
|-------|-------------|-------------------|-------------|
| **Loading** | ❓ Data fetching in progress | ❓ [Loading text or skeleton — where shown] | ❓ [Interactive / not interactive] |
| **Success** | ❓ Data loaded and rendered | ❓ Full content displayed | ❓ All interactive elements active |
| **Error** | ❓ API or validation error | ❓ [Error message/banner location] | ❓ [Retry available? Navigation?] |
| **Empty** | ❓ Valid response with no data | ❓ [Empty state message and CTA] | ❓ [Available actions] |
| ❓ **[Modal/Form variant]** | ❓ [When shown] | ❓ [Overlay / inline] | ❓ [Controls active] |

---

<!-- akr:section id="accessibility" required=true order=9 authorship="human" -->
## Accessibility

- **WCAG Level**: ❓ AA / AAA — NEEDS team confirmation
- **Keyboard navigable**: ❓ [Partial / Full — native `<button>` and `<input>` elements navigable by default]
- **Screen reader tested**: ❓ Not confirmed

### Known Accessibility Gaps

| Gap | Missing Implementation | Impact | Needs |
|-----|------------------------|--------|-------|
| ❓ [e.g., Modal has no `role="dialog"`] | ❓ [`role="dialog"`, `aria-modal`, `aria-labelledby`] | ❓ [Screen readers won't identify as dialog] | Implementation |
| ❓ [e.g., No focus trap in modal] | ❓ [Focus trap on open; return focus to trigger on close] | ❓ [WCAG 2.1 §3.2.5] | Implementation |
| ❓ [e.g., Native `confirm()` for delete] | ❓ [Accessible modal or in-page confirmation] | ❓ [Disruptive to screen reader flow] | Design decision |

---

<!-- akr:section id="testing" required=false order=10 condition="test_files_exist_in_module" authorship="human" -->
## Testing

> If no test file exists for this module, note: `NEEDS: [ModuleName].test.tsx — no page-level tests exist.`

### Test Coverage Summary

| File | Test File | Coverage | Notes |
|------|-----------|----------|-------|
| ❓ `[Component].tsx` | ❓ `[Component].test.tsx` | ❓ [% or "Not measured"] | ❓ [Gaps or confirmed coverage areas] |

---

<!-- akr:section id="known_issues" required=true order=11 authorship="human" -->
## Known Issues

**This module does NOT:**
- ❓ [Limitation 1 — absent business capability and where it lives instead]
- ❓ [Limitation 2 — stub or incomplete handler]
- ❓ [Limitation 3 — known UX gap]

### Open Issues

| Issue | Impact | Workaround | Tracking |
|-------|--------|------------|----------|
| ❓ [Issue description] | ❓ [Who's affected] | ❓ [Temporary fix] | ❓ [Link to ticket] |

---

<!-- akr:section id="questions_gaps" required=true order=12 authorship="human" -->
## Questions & Gaps

### AI-Flagged Questions

🤖 [AI will identify ambiguous UX behavior, missing business context, type contract mismatches, unverifiable ownership observed in source]

### Human-Flagged Questions

❓ [HUMAN: Add questions you have while reviewing — missing business rule context, unclear routing, owners for gaps]

## Documentation Standards

### How to Use This Template

**For AI (Copilot) - First Pass** (10-15 minutes):
1. Gather context: Open all component files + hooks + types
2. Attach files: All .tsx files in module, types.ts, custom hooks
3. Use prompt: "Document this React UI module using ui_component_template_module.md. Map component hierarchy, hooks, types, and interactions."
4. Review and correct output

**For Human - Enhancement** (10-15 minutes):
5. Add visual examples and real-world usage context
6. Document accessibility compliance
7. Add business context from your domain
8. Fill in Questions & Gaps
9. Test keyboard navigation and screen reader
10. Create PR with documentation

**Total Time**: ~20-25 minutes for baseline module documentation

---

### Required Sections (Minimum Viable Documentation)

✅ **Tier 1 - Always include**:
- Module Identification
- Quick Reference
- Module Files (component list)
- Purpose & Context
- Component Hierarchy
- Key component Props APIs
- Visual Examples

---

### Documentation Conventions

**References**:
- Follow **AKR_CHARTER_UI.md** for UI conventions
- Follow **AKR_CHARTER.md** for universal conventions
- Use AI/Human markers: 🤖 (AI-generated), ❓ (human input needed)

---
