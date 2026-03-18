## AKR Skill Distribution Update

This automated pull request distributes the latest AKR skill package from core-akr-templates.

### Files Updated
- .github/skills/akr-docs/SKILL.md
- .github/skills/akr-docs/SKILL-COMPAT.md
- .github/hooks/postToolUse.json
- .github/hooks/agentStop.json

### Reviewer Checklist
- [ ] Confirm SKILL.md version/header matches release tag
- [ ] Confirm SKILL-COMPAT.md matrix is present
- [ ] Confirm hook files are present and valid JSON
- [ ] Confirm CODEOWNERS protects .github/skills/akr-docs/SKILL.md

### Note
Hook files must be merged to activate local session validation before CI.
