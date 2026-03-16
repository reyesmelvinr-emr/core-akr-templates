---
businessCapability: [BUSINESS_CAPABILITY_PASCALCASE]
feature: [FN12345_US678]
domain: [DOMAIN]
layer: UI
component: [Component Name]
status: deployed
version: 1.0
componentType: UIComponent
priority: P1
lastUpdated: YYYY-MM-DD
---

# Component Documentation: [Component Name]

**File**: `src/components/[path]/[ComponentName].tsx`  
**Type**: [Presentational | Container | Page | Composite | HOC]  
**Complexity**: [Simple | Medium | Complex]  
**Author**: [Developer Name]

---

## Quick Reference

| | |
|---|---|
| **What it does** | 🤖 _Brief 1-sentence description of component's purpose_ |
| **When to use** | 🤖 _Situations where this component is appropriate_ |
| **When NOT to use** | 🤖 _Alternative components for different scenarios_ |
| **Accessibility** | ❓ _WCAG level (AA/AAA), keyboard nav, screen reader tested?_ |
| **Status** | 🤖 _Stable / Beta / Experimental / Deprecated_ |

**Example usage**:
```tsx
🤖 // Simple copy-paste example
import { ComponentName } from '@/components/[path]/ComponentName';

<ComponentName
  propName="value"
  onAction={handleAction}
>
  Content
</ComponentName>
```

---

## Purpose & Context

### What This Component Does

🤖 _Detailed description (2-3 sentences):_
- What problem does it solve?
- What is its primary responsibility?
- How does it fit into the larger application?

❓ _Enhance with business context:_
- Why was this component created?
- What business need does it address?
- What user story does it support?

---

### When to Use This Component

🤖 _List 3-5 use cases:_

**Use this component when:**
- Use case 1 (example: displaying a list of selectable items)
- Use case 2 (example: user needs to filter by category)
- Use case 3 (example: data should be paginated)

❓ _Enhance with real application examples:_
- Course catalog page (filtering courses by category)
- Admin panel (user management table)
- Dashboard (enrollment statistics cards)

---

### When NOT to Use This Component

🤖 _List alternatives:_

**Don't use this component when:**
- Scenario 1 → Use [AlternativeComponent] instead
- Scenario 2 → Use [OtherComponent] instead
- Scenario 3 → Build custom solution because...

---

## Props API

🤖 _Generate from TypeScript props interface_

### Props Table

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| 🤖 `propName` | `string` | Yes | - | Purpose of this prop |
| 🤖 `variant` | `'primary' \| 'secondary'` | No | `'primary'` | Visual style variant |
| 🤖 `loading` | `boolean` | No | `false` | Shows loading state |
| 🤖 `onAction` | `(param: Type) => void` | No | - | Callback when action occurs |
| 🤖 `children` | `React.ReactNode` | Yes/No | - | Component content |
| 🤖 `className` | `string` | No | `''` | Additional CSS classes |

❓ _Add for each complex prop:_

### Complex Props Details

#### `propName` (if complex type)

❓ _Explain non-obvious behavior:_
- What values are valid?
- What happens when value changes?
- Are there performance implications?
- Examples of common values

**Example**:
```tsx
❓ // Example showing complex prop usage
<ComponentName
  complexProp={{
    field1: 'value',
    field2: 123,
    nestedObj: { ... }
  }}
/>
```

---

#### `variant` (if component has variants)

🤖 _Auto-generate from variant type union_

| Variant | Visual Appearance | Use Case |
|---------|-------------------|----------|
| 🤖 `primary` | Blue background, white text | Main call-to-action |
| 🤖 `secondary` | White background, blue border | Secondary actions |
| 🤖 `danger` | Red background, white text | Destructive actions |

❓ _Add design rationale:_
- Why these specific variants?
- Are there design system mappings?
- Which variant should be default for most cases?

---

### Extended HTML Attributes

🤖 _If component extends native HTML element:_

This component extends `React.[ElementType]HTMLAttributes<HTML[ElementType]Element>`, which means **all standard HTML [element] attributes are supported**:

```tsx
<ComponentName
  customProp="value"        // Custom prop
  onClick={handleClick}     // Standard HTML prop
  className="my-class"      // Standard className
  aria-label="Description"  // ARIA attribute
  data-testid="test-id"     // Data attribute
/>
```

**Common HTML attributes**:
- 🤖 List relevant HTML attributes for this element type
- 🤖 Include type information
- 🤖 Note required vs optional

See [MDN Reference](https://developer.mozilla.org/docs/Web/HTML/Element/[element]) for complete list.

---

## Visual States & Variants

❓ _Document all visual states (if applicable)_

### Visual States

| State | Description | Visual Appearance | Interaction |
|-------|-------------|-------------------|-------------|
| **Default** | ❓ Normal resting state | ❓ Describe appearance | ❓ User can interact |
| **Hover** | ❓ Mouse over component | ❓ Describe hover effect | ❓ Shows pointer cursor |
| **Active** | ❓ Component being activated | ❓ Describe active state | ❓ Momentary during click |
| **Disabled** | ❓ Component cannot be used | ❓ Grayed out, reduced opacity | ❓ Not interactive |
| **Loading** | ❓ Async operation in progress | ❓ Shows spinner/skeleton | ❓ Not interactive |
| **Error** | ❓ Validation or runtime error | ❓ Red border, error icon | ❓ Shows error message |
| **Focus** | ❓ Keyboard navigation focus | ❓ Outline or border highlight | ❓ Keyboard accessible |

❓ _Screenshot references (if available):_
- Link to Figma designs
- Link to Storybook stories
- Reference screenshot files

---

## Component Behavior

### User Interactions

❓ _Document interaction patterns:_

| User Action | Component Response | Side Effects |
|-------------|-------------------|--------------|
| ❓ Click/Tap | ❓ What happens | ❓ State changes, API calls, navigation |
| ❓ Hover | ❓ Visual feedback | ❓ Tooltip, highlight, etc. |
| ❓ Keyboard (Enter/Space) | ❓ Activation behavior | ❓ Same as click or different? |
| ❓ Drag | ❓ Drag behavior (if applicable) | ❓ Reordering, moving, etc. |
| ❓ Right-click | ❓ Context menu (if applicable) | ❓ Actions available |

---

### State Management

🤖 _Auto-detect from component implementation:_

**State mode**: [Controlled | Uncontrolled | Hybrid]

#### Controlled Mode (if applicable)

❓ _Explain controlled behavior:_

Pass `value` and `onChange` to control state externally:

```tsx
❓ // Example of controlled usage
const [value, setValue] = useState('');

<ComponentName
  value={value}
  onChange={setValue}
/>
```

**When to use controlled mode**:
- ❓ Form validation required
- ❓ Derived state needed
- ❓ Complex state logic

#### Uncontrolled Mode (if applicable)

❓ _Explain uncontrolled behavior:_

Pass `defaultValue` (or neither) for internal state management:

```tsx
❓ // Example of uncontrolled usage
<ComponentName
  defaultValue="initial value"
  onBlur={(value) => console.log(value)}
/>
```

**When to use uncontrolled mode**:
- ❓ Simple forms
- ❓ Performance-critical scenarios
- ❓ Need ref access

---

### Side Effects

❓ _Document observable side effects:_

**This component may trigger**:
- ❓ API calls to: [endpoint names]
- ❓ Navigation to: [routes]
- ❓ Local storage updates: [keys]
- ❓ Global state changes: [state slices]
- ❓ Analytics events: [event names]
- ❓ Notifications/toasts
- ❓ Modal dialogs

---

## Styling & Theming

### CSS Modules

🤖 _Auto-detect from component imports:_

**Stylesheet**: `[ComponentName].module.css`  
**Approach**: CSS Modules (scoped styles)

#### CSS Classes

| Class Name | Purpose | Applied When |
|------------|---------|--------------|
| 🤖 `.component` | Base styles | Always |
| 🤖 `.variant-primary` | Primary variant | `variant="primary"` |
| 🤖 `.variant-secondary` | Secondary variant | `variant="secondary"` |
| 🤖 `.loading` | Loading state | `loading={true}` |
| 🤖 `.disabled` | Disabled state | `disabled={true}` |

---

### Design Tokens

❓ _If using design system:_

| Token | CSS Variable | Value | Usage |
|-------|-------------|-------|-------|
| ❓ Primary color | `--color-primary-500` | `#007bff` | Background |
| ❓ Text color | `--color-neutral-900` | `#1a1a1a` | Text |
| ❓ Border radius | `--radius-md` | `4px` | Corners |
| ❓ Spacing | `--space-3` | `12px` | Padding |

**Design System**: [Link to design system documentation]  
**Figma**: [Link to Figma component spec]

---

### Customization

❓ _Document how to customize appearance:_

#### Method 1: Props

```tsx
❓ // Use built-in props
<ComponentName
  variant="secondary"
  size="large"
  className="my-custom-class"
/>
```

#### Method 2: CSS Modules Override

```css
❓ /* MyComponent.module.css */
.myCustomClass {
  /* Override specific properties */
  background-color: var(--my-brand-color);
}
```

```tsx
❓ // Apply custom class
<ComponentName className={styles.myCustomClass} />
```

#### Method 3: Style Props (if supported)

```tsx
❓ // Inline style overrides
<ComponentName
  style={{ backgroundColor: '#custom' }}
/>
```

❓ _Note: Document which customization methods are recommended vs discouraged_

---

## Accessibility

### WCAG Compliance

❓ _Document accessibility level:_

- ❓ **WCAG Level**: AA / AAA
- ❓ **Keyboard navigable**: Yes / No
- ❓ **Screen reader compatible**: Yes / No / Partial
- ❓ **Color contrast**: Meets 4.5:1 minimum / 7:1 enhanced
- ❓ **Focus indicators**: Visible / Needs improvement

---

### ARIA Attributes

🤖 _Auto-detect from component implementation:_

| Attribute | When Applied | Purpose |
|-----------|--------------|---------|
| 🤖 `aria-label` | When no text children | Provides accessible name |
| 🤖 `aria-busy` | When `loading={true}` | Announces loading state |
| 🤖 `aria-disabled` | When `disabled={true}` | Announces disabled state |
| 🤖 `aria-expanded` | Collapsible components | Announces open/closed state |
| 🤖 `aria-controls` | Interactive components | Links to controlled element |
| 🤖 `aria-describedby` | With descriptions | Links to description text |

---

### Keyboard Support

❓ _Document keyboard navigation:_

| Key | Action |
|-----|--------|
| ❓ `Tab` | Move focus to component |
| ❓ `Shift+Tab` | Move focus to previous element |
| ❓ `Enter` | Activate component (primary action) |
| ❓ `Space` | Activate component (toggle for checkboxes) |
| ❓ `Escape` | Close/cancel (modals, dropdowns) |
| ❓ `Arrow keys` | Navigate within component (lists, menus) |

---

### Screen Reader Behavior

❓ _Test and document screen reader experience:_

**Default state announces**:
```
❓ "[Component name], [role], [state]"
Example: "Save, button"
Example: "Course title, heading level 2"
```

**Interactive state announces**:
```
❓ "[Label], [role], [state/value]"
Example: "Save, button, busy" (loading state)
Example: "Email, text field, required, invalid entry" (form validation)
```

❓ **Tested with**:
- [ ] NVDA (Windows)
- [ ] JAWS (Windows)
- [ ] VoiceOver (macOS)
- [ ] VoiceOver (iOS)
- [ ] TalkBack (Android)

---

### Accessibility Guidelines

❓ _Document dos and don'ts:_

✅ **DO:**
- ❓ Guideline 1 (example: Always provide `aria-label` for icon-only buttons)
- ❓ Guideline 2 (example: Ensure 4.5:1 color contrast ratio)
- ❓ Guideline 3 (example: Provide loading state feedback)

❌ **DON'T:**
- ❓ Anti-pattern 1 (example: Use `<div>` instead of `<button>`)
- ❓ Anti-pattern 2 (example: Omit `aria-label` on icon buttons)
- ❓ Anti-pattern 3 (example: Disable without explaining why)

---

## Usage Examples

❓ _Provide 3-5 real-world examples:_

### Example 1: Basic Usage

❓ _Most common use case_

```tsx
❓ // Description of scenario
import { ComponentName } from '@/components/[path]/ComponentName';

function MyComponent() {
  return (
    <ComponentName
      prop1="value"
      prop2={123}
    >
      Content
    </ComponentName>
  );
}
```

**Renders**: ❓ _Description of visual output_

---

### Example 2: With State Management

❓ _Controlled component example_

```tsx
❓ // Description of scenario
function StatefulExample() {
  const [value, setValue] = useState('');
  
  const handleChange = (newValue: string) => {
    setValue(newValue);
    console.log('Value changed:', newValue);
  };
  
  return (
    <ComponentName
      value={value}
      onChange={handleChange}
    />
  );
}
```

**Behavior**: ❓ _Describe what happens when user interacts_

---

### Example 3: With API Integration

❓ _Async data fetching example_

```tsx
❓ // Description of scenario
function AsyncExample() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchData()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  if (error) return <ErrorState error={error} />;
  
  return (
    <ComponentName
      data={data}
      loading={loading}
    />
  );
}
```

**Behavior**: ❓ _Describe loading → success → error flow_

---

### Example 4: Composition Pattern

❓ _If component supports composition_

```tsx
❓ // Description of compound component usage
<ComponentName>
  <ComponentName.Header>
    Header content
  </ComponentName.Header>
  <ComponentName.Body>
    Body content
  </ComponentName.Body>
  <ComponentName.Footer>
    Footer content
  </ComponentName.Footer>
</ComponentName>
```

**Benefits**: ❓ _Why use composition over props_

---

### Example 5: Advanced Usage

❓ _Complex scenario or edge case_

```tsx
❓ // Description of advanced pattern
function AdvancedExample() {
  // Complex logic
  
  return (
    <ComponentName
      // Advanced prop configuration
    >
      {/* Complex children */}
    </ComponentName>
  );
}
```

---

## Component Architecture

### Dependencies

🤖 _Auto-detect from imports:_

**External dependencies**:
- 🤖 Package 1 (purpose)
- 🤖 Package 2 (purpose)

**Internal dependencies (child components)**:
- 🤖 `ChildComponent1` - Used for [purpose]
- 🤖 `ChildComponent2` - Used for [purpose]

**Utilities/Services**:
- 🤖 `utility1` - Used for [purpose]
- 🤖 `apiService` - Used for [purpose]

❓ _Add for non-obvious dependencies:_
- Why is this dependency needed?
- Are there alternatives?
- Is it performance-critical?

---

### Consumers (Where This Component Is Used)

🤖 _If tool can detect usage:_

**Used in**:
- 🤖 `PageComponent1` - [Context]
- 🤖 `PageComponent2` - [Context]
- 🤖 `ParentComponent` - [Context]

❓ _Manually add critical usage contexts:_
- Course catalog page (main use case)
- Admin panel (secondary use case)
- Dashboard (if applicable)

---

### Related Components

❓ _Document component relationships:_

**Similar components** (alternative choices):
- ❓ `SimilarComponent1` - Use when [scenario]
- ❓ `SimilarComponent2` - Use when [scenario]

**Complementary components** (often used together):
- ❓ `ComplementComponent1` - Typically used with this component for [purpose]
- ❓ `ComplementComponent2` - Enhances this component by [purpose]

**Parent components** (containers):
- ❓ `ContainerComponent` - Wraps this component to provide [context/data]

---

## Data Flow

❓ _Document data flow (if complex):_

### Props → State → Render

```
❓ ASCII diagram showing data flow:

User Input
    ↓
onChange handler
    ↓
Parent state update (setValue)
    ↓
value prop changes
    ↓
Component re-renders
    ↓
Updated UI
```

### API Data Flow

```
❓ Diagram showing API integration:

Component Mount
    ↓
useEffect triggers
    ↓
API call (fetchData)
    ↓
Response received
    ↓
setState with data
    ↓
Component re-renders with data
```

---

## Performance Considerations

❓ _Document performance characteristics:_

### Rendering Performance

- **Typical render time**: ❓ _<5ms, <10ms, <50ms (measure with React DevTools Profiler)_
- **Re-render frequency**: ❓ _Low / Medium / High_
- **Memoization**: ❓ _React.memo applied? useMemo? useCallback?_
- **Bundle size**: ❓ _X KB (gzipped) - measure with bundle analyzer_

---

### Optimization Techniques

❓ _Document optimizations applied:_

**Applied optimizations**:
- ✅ ❓ `React.memo` - Prevents re-renders when props unchanged
- ✅ ❓ `useCallback` - Memoizes event handlers
- ✅ ❓ `useMemo` - Memoizes expensive computations
- ✅ ❓ Code splitting - Lazy loaded with `React.lazy`
- ✅ ❓ Virtualization - For large lists (react-window)

**Why optimized**:
- ❓ Component renders frequently (in list of 100+ items)
- ❓ Expensive computations (data transformations, filtering)
- ❓ Large bundle size (chart library, rich text editor)

---

### Performance Tips

❓ _Guidance for consumers:_

✅ **DO:**
- ❓ Pass stable `onClick` handlers (wrap with `useCallback`)
- ❓ Use `key` prop in lists for React reconciliation
- ❓ Memoize expensive props with `useMemo`

❌ **DON'T:**
- ❓ Pass inline arrow functions as props (creates new function every render)
- ❓ Pass new object/array literals as props (creates new reference every render)

**Example**:
```tsx
❓ // ❌ Bad: Creates new function every render
<ComponentName onClick={() => handleClick(id)} />

❓ // ✅ Good: Stable reference
const handleClick = useCallback(() => handleClick(id), [id]);
<ComponentName onClick={handleClick} />
```

---

## Error Handling

### Error Boundaries

❓ _Document error boundary usage:_

**Recommended error boundary**:
```tsx
❓ // Wrap component in error boundary
<ErrorBoundary fallback={<ErrorFallback />}>
  <ComponentName />
</ErrorBoundary>
```

---

### Error States

❓ _Document error handling:_

| Error Type | User Experience | Developer Action |
|------------|-----------------|------------------|
| ❓ **Network Error** | "Failed to load. Try again." with retry button | Logged to console, user can retry |
| ❓ **Validation Error** | Red border, error message below input | Error displayed inline |
| ❓ **API Error** | Error toast notification | Error logged to monitoring |
| ❓ **Render Error** | Error boundary shows fallback | Caught by boundary, reported to Sentry |

---

### Error Recovery

❓ _Document recovery mechanisms:_

- **Automatic retry**: ❓ _API calls retry 3 times with exponential backoff_
- **Manual retry**: ❓ _User can click "Try again" button_
- **Fallback UI**: ❓ _Error boundary shows generic message_
- **Error logging**: ❓ _Errors sent to Sentry/Application Insights_

---

## Testing

### Test Coverage

🤖 _Auto-detect if tests exist:_

- **Test file**: `[ComponentName].test.tsx`
- **Framework**: ❓ Vitest / Jest / React Testing Library
- **Coverage**: ❓ _X% (aim for 80%+)_

---

### Test Cases

❓ _Document test scenarios:_

| Scenario | Test | Expected Result |
|----------|------|-----------------|
| ❓ **Render** | Renders with props | Component visible in DOM |
| ❓ **Interaction** | User clicks button | `onClick` handler called |
| ❓ **States** | All visual states | Correct CSS classes applied |
| ❓ **Validation** | Invalid input | Error message displayed |
| ❓ **Accessibility** | Keyboard navigation | Focus moves correctly |
| ❓ **API Integration** | Mock API response | Data rendered correctly |

---

### Running Tests

```bash
❓ # Run all tests
npm test

❓ # Run this component's tests only
npm test ComponentName

❓ # Run with coverage
npm test -- --coverage

❓ # Run in watch mode
npm test -- --watch
```

---

### Mocking

❓ _Document mocking requirements:_

```tsx
❓ // Mock child components
vi.mock('@/components/ChildComponent', () => ({
  ChildComponent: ({ children }: any) => <div data-testid="mock-child">{children}</div>
}));

❓ // Mock API calls
vi.mock('@/services/api', () => ({
  fetchData: vi.fn(() => Promise.resolve(mockData))
}));

❓ // Mock hooks
vi.mock('@/hooks/useCustomHook', () => ({
  useCustomHook: () => ({ data: mockData, loading: false })
}));
```

---

### Visual Regression Tests

❓ _If using Storybook/Chromatic:_

- **Storybook stories**: `[ComponentName].stories.tsx`
- **Chromatic snapshots**: ❓ Enabled / Disabled
- **Coverage**: ❓ All variants, states, sizes

---

## Known Issues & Limitations

❓ _Document known problems:_

### Known Issues

| Issue | Impact | Workaround | Tracking |
|-------|--------|------------|----------|
| ❓ Issue description | ❓ Who's affected | ❓ Temporary fix | ❓ Link to ticket |

### Browser Compatibility

❓ _Document browser support:_

| Browser | Version | Support Level | Known Issues |
|---------|---------|---------------|--------------|
| ❓ Chrome | 90+ | ✅ Full | None |
| ❓ Firefox | 88+ | ✅ Full | None |
| ❓ Safari | 14+ | ⚠️ Partial | ❓ Issue with... |
| ❓ Edge | 90+ | ✅ Full | None |
| ❓ IE 11 | - | ❌ Not supported | N/A |

### Limitations

❓ _Document component limitations:_

**This component does NOT**:
- ❓ Limitation 1 (example: Does not support nested lists)
- ❓ Limitation 2 (example: Cannot render more than 1000 items)
- ❓ Limitation 3 (example: No built-in search functionality)

**Planned enhancements**:
- ❓ Feature 1 (example: Add virtualization for large lists) - Ticket #123
- ❓ Feature 2 (example: Support custom renderers) - Ticket #456

---

## Migration Guide

❓ _If component replaces older version:_

### Migrating from v1.x to v2.0

**Breaking changes**:
1. ❓ Change description
   ```tsx
   ❓ // Before (v1.x)
   <ComponentName oldProp="value" />
   
   ❓ // After (v2.0)
   <ComponentName newProp="value" />
   ```

2. ❓ Change description
3. ❓ Change description

**Deprecated props** (still work but will be removed in v3.0):
- ❓ `oldProp` → Use `newProp` instead

**Migration script**:
```bash
❓ # Automated codemod to update imports and props
npx @company/codemod migrate-component-v2
```

---

## Questions & Gaps

❓ _Use this section during documentation creation to track unknowns:_

### Unanswered Questions

- ❓ Question 1 (example: What's the maximum number of items this can handle?)
- ❓ Question 2 (example: Is this component used in mobile app?)
- ❓ Question 3 (example: Who designed this component?)

### Documentation Gaps

- ❓ Gap 1 (example: Missing visual examples for all variants)
- ❓ Gap 2 (example: Need to test with screen readers)
- ❓ Gap 3 (example: Performance benchmarks not measured yet)

### Technical Debt

- ❓ Debt item 1 (example: Should refactor to use composition pattern)
- ❓ Debt item 2 (example: Add proper TypeScript generics)
- ❓ Debt item 3 (example: Extract magic numbers to constants)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| ❓ 1.0.0 | YYYY-MM-DD | ❓ Name | Initial documentation |
| ❓ 1.1.0 | YYYY-MM-DD | ❓ Name | Added accessibility section |
| ❓ 2.0.0 | YYYY-MM-DD | ❓ Name | Breaking changes (see Migration Guide) |

---

## Documentation Standards

### How to Use This Template

**For AI (Copilot) - First Pass** (10-15 minutes):
1. Gather context: Open component file + props interface + usage examples
2. Attach files to Copilot: Component.tsx, parent components, related components
3. Use prompt: "Document this React component using ui_component_template.md. Focus on props API, visual states, and examples."
4. Review AI output, correct obvious errors

**For Human - Enhancement** (10-15 minutes):
5. Add visual examples (screenshots or detailed descriptions)
6. Document accessibility (test with screen reader if possible)
7. Add real-world usage context from your application
8. Fill in Questions & Gaps section
9. **Add feature tags** to Tags & Metadata section
10. Review with team, create PR

**Total Time**: ~20-25 minutes for baseline documentation

---

### Required Sections (Minimum Viable Documentation)

✅ **Tier 1 - Always include**:
- Component Identification (name, file, type)
- Quick Reference
- Purpose & Context (what, when, when not)
- Props API (table with all props)
- Visual Examples (at least 1 example)

---

### Documentation Conventions

**References**:
- Follow **AKR_CHARTER_UI.md** for UI-specific conventions
- Follow **AKR_CHARTER.md** for universal conventions
- Use AI/Human markers: 🤖 (AI-generated content), ❓ (requires human input)

**Cross-repository linking**:
- Backend API: `../../api-repo/docs/endpoints/[endpoint].md`
- Database: `../../database-repo/docs/tables/[Table]_doc.md`
- Design System: `https://design-system.company.com/components/[component]`

**Maintenance**:
- Update documentation when component changes (breaking changes, new props)
- Include in PR: "Updates [ComponentName]_doc.md with new props"
- Review documentation during code reviews

---

## Related Documentation

**Charters**:
- [AKR_CHARTER.md](./AKR_CHARTER.md) - Universal documentation principles
- [AKR_CHARTER_UI.md](./AKR_CHARTER_UI.md) - UI component conventions

**Templates**:
- [minimal_ui_component_template.md](./minimal_ui_component_template.md) - For simple components (10 min)
- [standard_ui_component_template.md](./standard_ui_component_template.md) - For complex components (45 min)

**Guides**:
- [UI_Documentation_Developer_Guide.md](./UI_Documentation_Developer_Guide.md) - How-to guide for developers

**Architecture**:
- [Frontend Architecture](../architecture/current/02-frontend-architecture.md)

---

**UI Component Template - End of Document**
