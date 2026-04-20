## AKR Skill Distribution Update

This automated pull request distributes the latest AKR skill package from core-akr-templates.

### Files Updated
- .github/skills/akr-docs/SKILL.md
- .github/skills/akr-docs/SKILL-COMPAT.md
- .github/hooks/postToolUse.json
- .github/hooks/agentStop.json
- .github/skills/akr-interview/SKILL.md
- .github/skills/akr-interview/scripts/akr-interview.md
- .github/skills/akr-capability/SKILL.md
- .github/skills/akr-capability/SKILL-COMPAT.md
- .github/skills/akr-capability/scripts/enhancement-clarify.md
- .github/skills/akr-capability/scripts/capability-define-clarify.md

### Reviewer Checklist
- [ ] Confirm SKILL.md version/header matches release tag
- [ ] Confirm SKILL-COMPAT.md matrix is present
- [ ] Confirm hook files are present and valid JSON
- [ ] Confirm CODEOWNERS protects .github/skills/akr-docs/SKILL.md
- [ ] Confirm akr-interview SKILL.md is present under .github/skills/akr-interview/
- [ ] Confirm akr-interview.md mode script is present under .github/skills/akr-interview/scripts/
- [ ] Confirm CODEOWNERS protects .github/skills/akr-interview/
- [ ] Confirm akr-capability SKILL.md is present under .github/skills/akr-capability/
- [ ] Confirm akr-capability SKILL-COMPAT.md is present under .github/skills/akr-capability/
- [ ] Confirm enhancement-clarify.md mode script is present under .github/skills/akr-capability/scripts/
- [ ] Confirm capability-define-clarify.md mode script is present under .github/skills/akr-capability/scripts/
- [ ] Confirm CODEOWNERS protects .github/skills/akr-capability/
- [ ] Confirm ONLY developer-facing akr-capability scripts are distributed to app repos (enhancement-clarify.md and capability-define-clarify.md); PO/TL modes stay in consolidation repo only

### Note
Hook files must be merged to activate local session validation before CI.
akr-capability distribution is scoped to developer-facing clarify modes only. The PO/TL modes remain in the consolidation repo and are not pushed to application codebase repos.
