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
</[PrimaryComponent]>
```

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
## Module Files - Detailed Breakdown

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

### [ComponentName].tsx — [Type: Page / Container / Presentational]

**Responsibility**: 🤖 [What this component accomplishes in the module]  
**Dependencies**: 🤖 [Child components it renders, hooks it uses]  
**Consumers**: 🤖 [What components/pages import this]  

**Key Props**:
| Prop | Type | Required | Description |
|------|------|----------|-------------|
| 🤖 `[propName]` | 🤖 `type` | 🤖 Yes/No | 🤖 [purpose] |
| 🤖 `[propName]` | 🤖 `type` | 🤖 Yes/No | 🤖 [purpose] |

---

<!-- akr:section id="hook_dependency" required=true order=5 authorship="ai" -->
## Hook Dependency Graph

### Custom Hooks in This Module

| Hook | File | Purpose | Used By |
|------|------|---------|---------|
| 🤖 `use[HookName]` | 🤖 `hooks/use[Hook].ts` | 🤖 [Data fetching/State management] | 🤖 [Which components call it] |
| 🤖 `use[HookName]` | 🤖 `hooks/use[Hook].ts` | 🤖 [Purpose] | 🤖 [Which components call it] |

### Hook Call Chain

```
[PageComponent]
├─ use[Hook1]()
│  └─ Manages state: [stateKey1], [stateKey2]
│  └─ Calls API: [endpoint]
│
├─ use[Hook2]()
│  └─ Depends on: [stateKey1] from use[Hook1]()
│  └─ Derives: [derivedValue]
│
└─ [ChildComponent]
   └─ use[ChildHook]()
      └─ Depends on: [prop from parent]
```

---

<!-- akr:section id="type_definitions" required=true order=6 authorship="ai" -->
## Type Definitions Cross-Reference

### Module-Specific Types

**File**: `[path]/types.ts`

| Type | Purpose | Used By |
|------|---------|---------|
| 🤖 `[TypeName]` | 🤖 [Data structure for this module] | 🤖 [Which components/hooks use it] |
| 🤖 `[InterfaceName]` | 🤖 [Props interface for component] | 🤖 [Which component] |
| 🤖 `[EnumName]` | 🤖 [Enumeration of values] | 🤖 [Which components/hooks use it] |

### Type Relationships

```typescript
🤖 // Example type relationships
interface [EntityData] {
  id: string;
  name: string;
  [relatedFields]
}

interface [EntityProps] extends React.HTMLAttributes<HTMLDivElement> {
  data: [EntityData];
  onAction: (id: string) => void;
  variant: 'default' | 'compact';
}

type [EntityState] = 'idle' | 'loading' | 'success' | 'error';
```

---

<!-- akr:section id="component_behavior" required=true order=7 authorship="human" -->
## Component Behavior

### User Interactions (Module Level)

| User Action | Primary Component Response | Affected Components | Side Effects |
|------------|--------------------------|-------------------|--------------|
| ❓ Click/Tap | ❓ What happens in primary component | ❓ Which child components update | ❓ State changes, API calls |
| ❓ Scroll | ❓ Module behavior | ❓ Components affected | ❓ Pagination, loading more? |
| ❓ Keyboard | ❓ Navigation within module | ❓ Components receiving focus | ❓ State updates |

---

<!-- akr:section id="data_flow" required=true order=8 authorship="ai" -->
## Data Flow

### Props → State → Render (Module Level)

```
Parent Component
    ↓
[PrimaryComponent] receives props
    ↓
use[Hook]() manages module state
    ↓
Child components receive props from parent
    ↓
All components re-render
    ↓
Updated UI across entire module
```

### API Data Flow

```
Module Mount
    ↓
use[DataHook]() triggers
    ↓
API call to [endpoint]
    ↓
Response received
    ↓
State updated in hook
    ↓
Props updated in components
    ↓
All components re-render with data
```

---

<!-- akr:section id="visual_states" required=true order=9 authorship="human" -->
## Visual States & Variants

❓ _Document all visual states across module components_

### Module Loading State

```
Initial Load
    ↓
[PrimaryComponent] shows skeleton/placeholder
    ↓
Child components display loading indicators
    ↓
Data arrives
    ↓
Smooth transition to content state
```

### Module States

| State | Description | Visual Appearance | Interaction |
|-------|-------------|-------------------|-------------|
| **Loading** | ❓ Data fetching in progress | ❓ Skeleton screens, spinners | ❓ Not interactive |
| **Success** | ❓ Data loaded and rendered | ❓ Full content displayed | ❓ All interactive elements active |
| **Error** | ❓ API or validation error | ❓ Error message, retry button | ❓ User can retry or navigate away |
| **Empty** | ❓ Valid response with no data | ❓ Empty state message, CTA | ❓ User can take action or navigate |

---

<!-- akr:section id="component_architecture" required=true order=10 authorship="mixed" human_columns="consumer_impact" -->
## Component Architecture

### Module Composition

🤖 [AI: Explanation of how the components in this module work together]

**Component Interaction Pattern:**
- [PrimaryComponent] receives data props and user input
- Calls use[Hook]() to manage state and fetch data
- Passes props to child components
- Child components emit events back to parent
- Parent updates state, triggering re-renders

### Dependencies

🤖 _Auto-detect from imports:_

**External dependencies**:
- 🤖 Package 1 (purpose)
- 🤖 Package 2 (purpose)

**Internal dependencies (child components)**:
- 🤖 `ChildComponent1` - Used for [purpose]
- 🤖 `ChildComponent2` - Used for [purpose]

**APIs and services**:
- 🤖 `apiService.[endpoint]` - Used for [purpose]
- 🤖 `[GlobalHook]` - Used for [purpose]

---

### Module Consumers

**This module is used in**:
- 🤖 `[PageName]` - [Context]
- 🤖 `[PageName]` - [Context]
- 🤖 `[ComponentName]` - [Context]

---

<!-- akr:section id="accessibility" required=true order=11 authorship="human" -->
## Accessibility

### WCAG Compliance

❓ _Document accessibility level:_

- ❓ **WCAG Level**: AA / AAA
- ❓ **Keyboard navigable**: Yes / No
- ❓ **Screen reader compatible**: Yes / No / Partial
- ❓ **Color contrast**: Meets 4.5:1 minimum for all components
- ❓ **Focus indicators**: Visible throughout module

### Module Keyboard Navigation

| Key | Action |
|-----|--------|
| ❓ `Tab` | Move focus through module components |
| ❓ `Shift+Tab` | Move focus to previous element |
| ❓ `Enter` | Activate focused button/link |
| ❓ `Space` | Toggle checkbox/radio |
| ❓ `Arrow Up/Down` | Navigate within lists |
| ❓ `Escape` | Close modals/dropdowns in module |

### Screen Reader Behavior

**Module announces**:
```
❓ "[PageTitle], heading level 1"
❓ "[Description], paragraph"
❓ "[ComponentName], button, [state]"
❓ "[ListName], list with [N] items, current item [X]"
```

---

<!-- akr:section id="testing" required=true order=12 authorship="human" -->
## Testing

### Test Structure

```css
[ModuleName].test.tsx
├─ Render tests
│  ├─ Renders with required props
│  ├─ Renders children correctly
│  └─ Handles loading state
├─ Interaction tests
│  ├─ User clicks button → calls onAction callback
│  ├─ User types in input → state updates
│  └─ User navigates keyboard → focus moves
├─ Integration tests
│  ├─ API call triggers on mount
│  ├─ Data displays correctly
│  └─ Error state shows on API failure
└─ Accessibility tests
   ├─ All interactive elements keyboard accessible
   ├─ Screen reader announces all content
   └─ Color contrast meets WCAG AA
```

### Test Coverage Goals

| Category | Target | Current | Notes |
|----------|--------|---------|-------|
| ❓ Statement coverage | 80%+ | ❓ _% | |
| ❓ Branch coverage | 70%+ | ❓ _% | |
| ❓ Function coverage | 80%+ | ❓ _% | |
| ❓ Line coverage | 80%+ | ❓ _% | |

---

<!-- akr:section id="known_issues" required=true order=13 authorship="human" -->
## Known Issues & Limitations

### Module Limitations

❓ _Document what this module does NOT do:_

**This module does NOT**:
- ❓ Limitation 1 (example: Support real-time updates)
- ❓ Limitation 2 (example: Handle offline functionality)
- ❓ Limitation 3 (example: Support mobile-optimized layout without CSS module)

### Known Issues

| Issue | Impact | Workaround | Tracking |
|-------|--------|------------|----------|
| ❓ Issue description | ❓ Who's affected | ❓ Temporary fix | ❓ Link to ticket |

### Browser Support

| Browser | Version | Support | Known Issues |
|---------|---------|---------|--------------|
| ❓ Chrome | 90+ | ✅ Full | None |
| ❓ Firefox | 88+ | ✅ Full | None |
| ❓ Safari | 14+ | ⚠️ Partial | ❓ Issue with... |

---

<!-- akr:section id="performance_considerations" required=true order=14 authorship="human" -->
## Performance Considerations

### Module Performance

- **Initial load time**: ❓ _ms (measure Time to Interactive for module)_
- **Re-render frequency**: ❓ _Low / Medium / High per user interaction_
- **Memory usage**: ❓ _MB for typical usage_
- **Bundle size**: ❓ _KB (gzipped) including all components and hooks_

### Applied Optimizations

✅ **Optimizations in place**:
- ❓ Code splitting - Lazy load with `React.lazy`
- ❓ Memoization - `React.memo` on expensive components
- ❓ Hook memoization - `useCallback`, `useMemo` in custom hooks
- ❓ Virtualization - For large lists ([component name])

### Performance Tips

✅ **DO:**
- ❓ Pass stable callback props (wrap with `useCallback`)
- ❓ Use `key` prop in lists for React reconciliation
- ❓ Memoize expensive props with `useMemo`

❌ **DON'T:**
- ❓ Pass inline arrow functions as props
- ❓ Pass new object/array literals as props
- ❓ Fetch data in render function

---

<!-- akr:section id="questions_gaps" required=true order=15 authorship="human" -->
## Questions & Gaps

### Unanswered Questions

- ❓ Question 1 (example: What's the plan for real-time updates?)
- ❓ Question 2 (example: Should this module support offline mode?)
- ❓ Question 3 (example: Is mobile design approved?)

### Documentation Gaps

- ❓ Gap 1 (example: Missing accessibility testing results)
- ❓ Gap 2 (example: Need performance benchmarks)
- ❓ Gap 3 (example: Mobile responsiveness not fully documented)

### Technical Debt

- ❓ Debt item 1 (example: Should refactor hook logic)
- ❓ Debt item 2 (example: Extract magic numbers to constants)
- ❓ Debt item 3 (example: Add proper error boundaries)

---

<!-- akr:section id="version_history" required=true order=16 authorship="human" -->
## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| ❓ 1.0.0 | YYYY-MM-DD | ❓ Name | Initial documentation |
| ❓ 1.1.0 | YYYY-MM-DD | ❓ Name | Added accessibility section |
| ❓ 2.0.0 | YYYY-MM-DD | ❓ Name | Module restructuring |

---

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
