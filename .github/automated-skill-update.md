## AKR Skill Distribution Update

This automated pull request distributes the latest AKR skill package from core-akr-templates.

### Files Updated
- .github/skills/akr-docs/SKILL.md
- .github/skills/akr-docs/SKILL-COMPAT.md
- .github/hooks/postToolUse.json
- .github/hooks/agentStop.json
- .github/skills/akr-interview/SKILL.md
- .github/skills/akr-interview/scripts/akr-interview.md

### Reviewer Checklist
- [ ] Confirm SKILL.md version/header matches release tag
- [ ] Confirm SKILL-COMPAT.md matrix is present
- [ ] Confirm hook files are present and valid JSON
- [ ] Confirm CODEOWNERS protects .github/skills/akr-docs/SKILL.md
- [ ] Confirm akr-interview SKILL.md is present under .github/skills/akr-interview/
- [ ] Confirm akr-interview.md mode script is present under .github/skills/akr-interview/scripts/
- [ ] Confirm CODEOWNERS protects .github/skills/akr-interview/

### Note
Hook files must be merged to activate local session validation before CI.
