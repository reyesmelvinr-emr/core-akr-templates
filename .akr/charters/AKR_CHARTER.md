# Application Knowledge Repo (AKR) Charter

**Version**: 2.0  
**Last Updated**: 2025-11-17  
**Authority**: System-wide (applies to all teams and projects)  
**Maintained By**: Architecture Team / Tech Leads

---

## Purpose

The **Application Knowledge Repo (AKR)** is a **framework** for capturing, organizing, and maintaining knowledge about applications. This Charter defines the universal principles, conventions, and standards that apply across all documentation types and all teams.

**What the AKR provides**:
- Shared understanding of system architecture and behavior
- Context for new developers joining the team
- Historical record of decisions and evolution (via Git)
- Foundation for cross-team consistency

**What the AKR is NOT**:
- A compliance checkbox exercise
- Exhaustive documentation of every detail
- A replacement for code comments or API docs
- Static documentation that never changes

---

## Core Principles

### 1. Lean by Default

**Principle**: Start with minimal documentation, add detail as knowledge accumulates.

**Why**: Upfront comprehensive documentation is often speculative and becomes outdated. Better to document what we know now and expand as we learn.

**Practice**:
- Essential sections only at creation (what, why, how)
- Add optional sections when real experience reveals they're valuable
- Don't document "future plans" - document current reality
- Avoid placeholder text like "TBD" or "To be determined"

**Example**:
```
Day 1: Document basic structure, purpose, key behaviors
Month 3: Add "Known Limitations" after production issues discovered
Month 6: Add "External Integrations" section after mobile app integration
```

---

### 2. Flexible to Context

**Principle**: Templates are starting points, not rigid contracts. Customize to reality.

**Why**: Different tables/components have different complexity. A lookup table needs less documentation than a business-critical transactional table.

**Practice**:
- Required sections: minimum viable documentation
- Recommended sections: include if applicable
- Optional sections: add when they provide value
- Custom sections: encouraged when context demands it

**Example**:
```
Simple utility function: 30 lines (minimal)
Complex business service: 300 lines (comprehensive, custom sections)
Both are acceptable if they serve their purpose
```

---

### 3. Evolutionary

**Principle**: Documentation grows as knowledge and systems evolve.

**Why**: We don't know everything on Day 1. Production teaches us limitations, integrations emerge, requirements change.

**Practice**:
- Update docs when implementation changes
- Add sections when new context emerges
- Don't force completeness upfront
- Git history shows evolution (don't duplicate in docs)

**Example**:
```
Initial: Basic component/object documentation
+ 3 months: Add performance notes (learned from production)
+ 6 months: Add external integration notes (new mobile app)
+ 1 year: Add migration notes (preparing for refactoring)
```

---

### 4. Tool-Assisted, Human-Verified

**Principle**: Use automation (LLMs, scripts) to accelerate, but humans verify accuracy.

**Why**: Tools can generate structure and infer context, but can't know business rules or make judgment calls.

**Practice**:
- LLMs generate first drafts (50-70% complete)
- Scripts ensure consistent structure
- Developers add business context tools can't infer
- Tech Leads review for accuracy and value
- Human judgment is final quality gate

**Example**:
```
1. LLM generates doc from code (structure, inferred descriptions)
2. Developer adds: business context, integrations, limitations
3. Tech Lead reviews: Is this useful? Is this accurate?
4. Approved → Merge
```

---

### 5. Git-Integrated

**Principle**: Git is the authoritative source for history and versioning.

**Why**: Git provides better tooling for history than embedded changelogs. Don't duplicate what Git does well.

**Practice**:
- Git commits show what changed and when
- Feature tags in commit messages link to work items
- Git blame shows who wrote each section
- Git diff shows evolution between versions
- Documentation files do NOT include "Change History" sections

**Example**:
```
Git commit: "docs: add external integration note (FN99999_US145)"
Git log: Shows all changes to file over time
Git blame: Shows who documented each section
```

---

## Universal Conventions

### Feature Tag Convention

**Format**: `FN#####_US#####`

**Components**:
- `FN#####` = Feature number from Azure Boards
- `US#####` = User Story number

**Purpose**: Links documentation changes to work items for traceability.

**Usage in Git Commits**:
**Examples**:
```bash
Format: docs: [action] [object] - [description] (FN#####_US#####)

Examples:
git commit -m "docs: add CourseService documentation (FN99999_US002)"
git commit -m "docs: update Button component - add OAuth (FN99999_US145)"
git commit -m "docs: clarify enrollment business rules (FN99999_US089)"
```

**Usage in Documentation** (optional):
```markdown
## Notes
This table was created as part of FN99999_US002 to support employee training tracking.
```

**Flexibility**: 
- Teams can extend to task level if needed: `FN#####_US#####_T###`
- Format may evolve based on team needs
- Consistency within project > perfect convention

---

### File Naming Conventions

**Format**: `[ObjectName]_doc.md`

**Examples**:
- Database: `Courses_doc.md`, `Users_doc.md`
- Backend: `EnrollmentService_doc.md`, `CourseService_doc.md`
- UI: `Button_doc.md`, `CourseCard_doc.md`
- Domains: `authentication_domain.md`, `user-management_domain.md`

**Rules**:
- Use PascalCase for object names (matches code/schema)
- Suffix with `_doc.md` to distinguish from other files
- No spaces in filenames (use underscores or hyphens)
- Lowercase for domain docs (filesystem friendly)

**Directory Structure**:
```
docs/
├── database/
│   ├── tables/
│   │   ├── Courses_doc.md
│   │   └── Users_doc.md
│   └── views/
│       └── vw_ActiveCourses_doc.md
├── services/
│   ├── EnrollmentService_doc.md
│   └── CourseService_doc.md
├── components/
│   ├── Button_doc.md
│   └── CourseCard_doc.md
└── domains/
    ├── authentication_domain.md
    └── user-management_domain.md
```

---

### Git Commit Message Format

**Standard Format**:
```
docs: [action] [object] - [description] (FN#####_US#####)
```

**Actions**:
- `add` - Creating new documentation
- `update` - Modifying existing documentation
- `clarify` - Improving clarity without adding new info
- `fix` - Correcting errors
- `remove` - Deleting deprecated documentation

**Examples**:
```bash
docs: add EnrollmentService documentation (FN99999_US002)
docs: update Button component - add accessibility notes (FN99999_US124)
docs: clarify enrollment business rules (FN99999_US089)
docs: fix typo in CourseService description
docs: remove deprecated PaymentService documentation
```

**Commit Body** (optional but recommended):
```bash
git commit -m "docs: update CourseService - add external integration (FN99999_US145)" -m "
Mobile app now calls CourseService directly for catalog display.
Added External Integrations section with performance notes.
"
```

---

### Change History: NOT Included in Docs

**Principle**: Git is the authoritative source for change history.

**Applies to**: All documentation types (database, backend, UI, domains)

**Rationale**:
- Git commit messages contain: what changed, when, who, why
- Git log provides complete timeline
- Git blame shows line-by-line evolution
- Git tags mark significant milestones
- Embedding history in docs creates redundancy and maintenance burden

**To view change history**:
```bash
# View all changes to a documentation file
git log docs/services/EnrollmentService_doc.md

# View changes with diffs
git log -p docs/components/Button_doc.md

# Search for specific feature
git log --grep="FN99999_US089"

# See what changed between versions
git diff v1.0..v2.0 docs/

# Find when a specific line was added
git blame docs/services/EnrollmentService_doc.md
```

**Exception**: Domain documentation MAY include high-level milestones if it helps business understanding:
```markdown
## Evolution Milestones
- **2025-10**: Initial authentication system (password only)
- **2025-11**: Added OAuth 2.0 support (Google, Microsoft)
- **2026-01**: Added MFA support (authenticator apps)
```

---

## Tool Integration

### Philosophy: Tool-Agnostic, Outcome-Focused

**Principle**: The AKR framework is **tool-agnostic**. We define standards for documentation quality and consistency, not which tools produce it.

**Why**: AI tooling evolves rapidly. Today's solutions may be outdated in months. Focus on outcomes, not tools.

**Current State (2025-11)**:
- Primary: LLM prompt-based generation (Copilot, Claude, ChatGPT)
- Emerging: Script-based automation (Python, PowerShell)
- Future: Agentic AI, IDE integrations, custom toolchains

**Evolution Path**:
```
Phase 1 (Current): Manual prompts → LLM → Human review
Phase 2 (Near-term): Scripts/templates → Batch generation → Human review
Phase 3 (Future): Agentic AI → Autonomous documentation → Human approval
Phase 4 (Emerging): IDE-integrated → Real-time suggestions → Incremental updates
```

---

### Universal Tool Requirements

**Any tool (current or future) used for AKR documentation must**:

1. ✅ **Follow AKR Charter conventions**
   - Feature tag format (FN#####_US#####)
   - File naming conventions ([ObjectName]_doc.md)
   - No "Change History" sections (Git is source of truth)
   - Technology-specific conventions (from DB/Backend/UI charters)

2. ✅ **Produce tier-appropriate structure**
   - Essential (Tier 1) sections always present
   - Recommended (Tier 2) sections when applicable
   - Optional (Tier 3) sections marked for human decision

3. ✅ **Enable human verification**
   - Clear markers for AI-generated vs. human-added content
   - Uncertainty flagged (e.g., `[verify: ...]`)
   - No hallucinated or speculative content
   - Readable output format (Markdown)

4. ✅ **Integrate with workflow**
   - Compatible with Git version control
   - Supports incremental updates (not just initial generation)
   - Respects technology-specific charters
   - Works within team's development environment

---

### Current Tool Guidance (2025-11)

#### LLM Prompt-Based Generation

**Tools**: GitHub Copilot, Claude, ChatGPT, other LLMs

**Standard Prompt Template**:
```
Follow the principles in AKR_CHARTER.md and use template at [specific_template.md].

Key requirements from AKR Charter:
- Be concise (explain what and why, not implementation details)
- Start lean, mark sections for human enhancement
- Follow feature tag convention: FN#####_US#####
- Do not create "Change History" section (Git is source of truth)
- Reference technology-specific charter: [AKR_CHARTER_DB.md | AKR_CHARTER_BACKEND.md | AKR_CHARTER_UI.md]

Context:
[Provide schema/code/component here]

Generate documentation following the template.
```

**Content Guidelines**:
- **Purpose**: 1-3 sentences explaining what and why
- **Descriptions**: 5-20 words per item (clear but concise)
- **Business rules**: Use BR-OBJECTNAME-### format
- **Mark uncertainty**: Use `[verify: ...]` for uncertain items
- **Avoid speculation**: Don't document future plans, document current reality

**LLM Output Expectations**:
- 50-70% complete documentation (structure + inferred content)
- Requires human enhancement (business context, custom sections)
- Accuracy verification needed (LLMs can hallucinate)
- First draft quality (not final)

**Developer Responsibilities**:
- Review LLM output for accuracy
- Add business context LLM can't know
- Add custom sections as needed
- Verify technical details
- Remove AI-generated placeholder text

---

#### Script-Based Generation

**Tools**: Python scripts, PowerShell scripts, custom toolchains

**Script Requirements**:
- Read AKR_CHARTER.md for conventions (feature tags, file naming, etc.)
- Apply technology-specific charter rules (DB, Backend, UI)
- Generate AKR-compliant structure (no Change History sections)
- Produce clean first drafts requiring human enhancement
- Support batch processing for multiple objects

**Script Output Expectations**:
- Consistent structure across all generated docs
- Technology-specific conventions applied
- Placeholder text clearly marked for human input
- No speculative content

**Integration Points**:
- CI/CD pipelines (automated doc generation on schema changes)
- Pre-commit hooks (documentation validation)
- IDE extensions (in-editor documentation assistance)

---

### Future Tool Evolution

#### Agentic AI (Anticipated)

**Characteristics**:
- Autonomous documentation generation and updates
- Multi-step reasoning (analyze code → infer context → generate docs)
- Self-validation against AKR Charter
- Incremental updates based on code changes

**Integration Requirements**:
- Must request human approval before committing documentation
- Must flag uncertainty and business logic gaps
- Must trace documentation to code/schema changes
- Must respect Git workflow (PRs, feature tags)

**Example Workflow**:
```
1. Agent detects schema change (new column added)
2. Agent generates documentation update
3. Agent creates PR with feature tag
4. Human reviews and approves/rejects
5. Documentation merged on approval
```

---

#### IDE-Integrated Tools (Emerging)

**Characteristics**:
- Real-time documentation suggestions
- Inline documentation editing
- Context-aware templates
- Live validation against AKR Charter

**Integration Requirements**:
- Non-intrusive (suggestions, not forced changes)
- Works with existing file structure (docs/ folder)
- Compatible with team's IDE (VS Code, Visual Studio, IntelliJ, etc.)
- Respects technology-specific charters

**Example Use Cases**:
- Hover over table/class → See AKR documentation
- Add new method → Suggest documentation template
- Modify schema → Flag outdated documentation
- Commit code → Validate documentation completeness

---

#### Custom Toolchains (Team-Specific)

**Teams may build custom tools** tailored to their workflow:
- Database schema parsers → Auto-generate table documentation
- API spec parsers → Auto-generate endpoint documentation
- Component analyzers → Auto-generate UI component docs
- Migration tools → Update documentation during refactoring

**Requirements**:
- Must follow AKR Charter conventions
- Must integrate with Git workflow
- Must produce human-readable output
- Must be maintainable by team

**Example**:
```bash
# Custom script: Generate docs from database schema
./tools/generate-table-docs.py --schema production --output docs/tables/

# Output: Courses_doc.md, Users_doc.md, etc. (AKR-compliant)
# Developer reviews, enhances, commits with feature tag
```

---

### Tool Selection Guidance

**For teams starting with AKR**:
1. **Phase 1**: Start with manual LLM prompts (lowest barrier to entry)
2. **Phase 2**: Add scripts for repetitive tasks (batch generation, validation)
3. **Phase 3**: Adopt emerging tools as they mature (agentic AI, IDE integrations)
4. **Phase 4**: Build custom tooling if needed (team-specific workflows)

**Evaluation Criteria for New Tools**:
- ✅ Does it follow AKR Charter conventions?
- ✅ Does it integrate with our Git workflow?
- ✅ Does it require human verification?
- ✅ Is it maintainable by our team?
- ✅ Does it improve quality or reduce effort?

**Red Flags**:
- ❌ Forces tool-specific format (not AKR-compliant)
- ❌ Bypasses human review (autonomous commits without approval)
- ❌ Generates speculative content (hallucinations, future plans)
- ❌ Vendor lock-in (proprietary formats, can't migrate)

---

### Updating This Section

**This "Tool Integration" section will evolve** as new tools emerge.

**Update triggers**:
- New AI capabilities become available (e.g., agentic AI, multi-modal LLMs)
- Team adopts new toolchains (e.g., custom scripts, IDE extensions)
- Industry best practices change (e.g., new documentation automation standards)

**Update process**:
1. Propose update to Architecture/Tech Leads
2. Test new tool/approach with pilot team
3. Document learnings and integration requirements
4. Update AKR_CHARTER.md with new guidance
5. Communicate changes to all teams

**Version history** (for Tool Integration section):
- **v1.0 (2025-10)**: Initial guidance (LLM prompts)
- **v2.0 (2025-11)**: Add future-proof philosophy, script guidance, agentic AI anticipation

---

**Remember**: Tools are means to an end. The end is **useful, accurate, maintainable documentation**. Use whatever tools help achieve that outcome, as long as they follow AKR Charter principles

---

## Common Patterns Across Documentation Types

### Business Rules Format

**Format**: `BR-[OBJECTNAME]-###: Rule description`

**Purpose**: 
- Consistent numbering makes rules easier to reference
- Links documentation to code/validation logic
- Enables traceability in discussions and code reviews

**Examples**:
```markdown
## Business Rules
- BR-ENROLLMENT-001: Users cannot enroll in same course twice
- BR-COURSE-002: Course title must be unique within category
- BR-BUTTON-003: Primary buttons require explicit onClick handler
```

**Applies to**: Database objects, backend services, UI components, domain documentation

**Numbering**:
- Start at 001 for each object
- Sequential numbering (001, 002, 003...)
- Gaps are acceptable (if rule deleted, don't renumber)

---

### Optional Sections: Add When Valuable

**Philosophy**: Don't force sections that provide no value.

**Common optional sections**:
- **External Integrations** - When other systems access this object
- **Performance Considerations** - When production revealed bottlenecks
- **Known Limitations** - When technical debt exists
- **Future Considerations** - When refactoring is planned
- **Security Notes** - When special security requirements exist
- **Compliance Notes** - When regulatory requirements apply

**Add these sections**:
- ✅ When you have real information to share
- ✅ When it helps the team understand context
- ✅ When it prevents future confusion

**Don't add these sections**:
- ❌ On Day 1 with placeholder text
- ❌ Just because template suggests it
- ❌ With speculative/future content

---

## Documentation Tiers

### Tier 1: Essential (Always Required)

**What**: Minimum viable documentation

**Sections**:
- Object identification (name, location, type)
- Purpose (what and why - 1-3 sentences)
- Structure/API (varies by documentation type)

---

### Tier 2: Recommended (Include When Applicable)

**What**: Sections that add significant value for most objects

**Varies by type**:
- Database: Constraints, relationships, indexes
- Backend: Dependencies, data operations, business rules
- UI: Props API, states/variants, accessibility

**Why**: Most objects have these, documenting them helps developers.

**Enforcement**: Validation scripts may warn if missing.

---

### Tier 3: Optional (Add as Needed)

**What**: Context-specific sections that vary by object complexity

**Sections**:
- External integrations
- Performance considerations
- Known limitations
- Future considerations
- Security/compliance notes
- Data migration notes
- Custom sections

**Why**: Varies by complexity and production experience.

**Enforcement**: Never enforced. Always allowed.

---

## Team Customization

### Relationship: AKR Charter vs. Team Standards

**AKR Charter** (this document):
- **Scope**: System-wide (all teams)
- **Authority**: Architecture/Tech Lead approval required
- **Change frequency**: Rare (quarterly or less)
- **Content**: Principles, universal conventions, shared patterns
- **Cannot be overridden**: Teams must follow Charter

**Team Standards** (OUR_STANDARDS.md in each project):
- **Scope**: Team-specific (single team/project)
- **Authority**: Team Lead approval sufficient
- **Change frequency**: Frequent (weekly/monthly as needed)
- **Content**: Required sections, team formats, validation rules
- **Can extend Charter**: Teams can be stricter, but can't contradict

**Example**:
```
AKR Charter says: "Use feature tag convention FN#####_US#####"
Team A: "Feature tags optional in commit messages"
Team B: "Feature tags required - validation checks on commits"

Both teams follow Charter convention format, but customize enforcement.
```

---

### What Teams Can Customize

**Teams CAN**:
- ✅ Reclassify sections (Optional → Recommended → Required)
- ✅ Add team-specific format requirements
- ✅ Define validation rules
- ✅ Add team-specific conventions
- ✅ Set stricter standards than Charter

**Teams CANNOT**:
- ❌ Contradict Charter principles
- ❌ Ignore feature tag convention
- ❌ Override file naming conventions
- ❌ Create "Change History" sections in docs

**Example Team Customization**:
```markdown
# OUR_STANDARDS.md

## Our Team's Extensions to AKR Charter

### Required Sections (for us)
- All sections in Tier 1 (Essential) - per AKR Charter
- Business Rules - REQUIRED for all services (elevated from Recommended)
- External Integrations - REQUIRED for externally-accessed components

### Team-Specific Formats
- Business rules must include rationale: BR-XXX-###: Rule (Rationale: ...)
- External integrations must note SLA implications
```

---

## Governance

### How the Charter Evolves

**Process**:
1. Developer/Team proposes change (PR to AKR_CHARTER.md)
2. Cross-team discussion (not just one team affected)
3. Architecture/Tech Lead approval required
4. Technology-specific charters updated to align (if applicable)
5. Teams update their OUR_STANDARDS.md if affected
6. Documentation communicated to all teams

**When to update Charter**:
- ✅ New documentation type added (need shared conventions)
- ✅ Cross-template inconsistency discovered
- ✅ Common instruction duplicated across docs
- ✅ System-wide principle needs refinement

**When NOT to update Charter**:
- ❌ Team-specific need (goes in team's OUR_STANDARDS.md)
- ❌ Technology-specific detail (goes in specific charter)
- ❌ Personal preference without broad impact
- ❌ Temporary experiment (try in team first, generalize if successful)

---

### Authority Hierarchy

```
AKR_CHARTER.md (Universal - System-wide)
    ↓ Extended by
    ├─ AKR_CHARTER_DB.md (Database-specific)
    ├─ AKR_CHARTER_BACKEND.md (Backend-specific)
    └─ AKR_CHARTER_UI.md (UI-specific)
        ↓ Used by
        Templates (table_doc_template.md, service_doc_template.md, etc.)
            ↓ Customized by
            OUR_STANDARDS.md (Team-specific)
                ↓ Used by
                Individual Developers
```

**Conflict Resolution**:
- Universal Charter > Technology Charter (if conflict, Universal wins)
- Technology Charter > Template (if conflict, Charter wins)
- Team Standards > Individual preference
- Teams cannot contradict Charters

---

### Charter Version History

**Version 2.0** (2025-11-17): Universal Framework
- Repositioned AKR as framework (not system)
- Removed database-specific content (moved to AKR_CHARTER_DB.md)
- Added future-proof Tool Integration section (agentic AI, IDE integration)
- Expanded to support database, backend, and UI documentation types

**Version 1.0** (2025-10-22): Initial Charter
- Established five core principles
- Defined universal conventions (feature tags, Git format)
- Set documentation tiers (Essential/Recommended/Optional)
- Clarified governance model

---

## Technology-Specific Charters

**The AKR system includes technology-specific charters** that extend this universal Charter with conventions specific to databases, UIs, APIs, etc.

**Current charters**:
- **AKR_CHARTER_DB.md** - Database-specific conventions
- **AKR_CHARTER_BACKEND.md** - Backend service conventions
- **AKR_CHARTER_UI.md** - UI component conventions

**These charters**:
- Reference and build upon this universal Charter
- Add technology-specific conventions
- Must not contradict universal Charter
- Maintained alongside universal Charter

---

## Quick Reference

### For Developers

**When creating new documentation**:
1. Use appropriate template (see technology-specific charter)
2. Follow AKR Charter conventions (feature tags, file naming)
3. Check technology-specific charter (DB, Backend, UI)
4. Check team standards (OUR_STANDARDS.md if exists)
5. Use tools to assist (LLM or script)
6. Review and enhance tool output
7. Submit PR with feature tag in commit message

**When updating existing documentation**:
1. Keep structure consistent with template
2. Add sections as needed (don't remove valuable content)
3. Update "Last Updated" date
4. Use feature tag in commit message
5. Review for accuracy

**When reviewing documentation PRs**:
1. Is this useful? (most important question)
2. Is this accurate?
3. Does it follow AKR Charter conventions?
4. Are custom sections justified?
5. Approve if yes to all

---

## Questions & Support

**Questions about Charter interpretation?**
- Ask Architecture/Tech Lead team
- Reference technology-specific charters
- Check team standards for team-specific guidance

**Proposing Charter changes?**
- Open PR with rationale
- Tag Architecture/Tech Leads for review
- Expect cross-team discussion

**Need help with documentation?**
- Check technology-specific charter first
- Check templates for structure
- Ask team members for examples

---

**Remember**: The goal is useful documentation that helps the team, not perfect documentation that becomes a burden. When in doubt, prioritize value over compliance.

---

**AKR Charter - End of Document**
