# AKR Copilot Space - Bootstrap and Maintenance Checklist

Date: 2026-04-21
Status: Draft starter template
Owner: Space owner

## Space URL
- _Space URL pending provisioning. Once the Space is created, record the URL here and update `docs/AKR_COPILOT_QUICKSTART.md` to match._

## Pre-session checks
- [ ] The three intended repositories are attached to the Space.
- [ ] Repository indexing has completed and returns expected search results.
- [ ] The Space instruction is present and matches docs/AKR_SPACE_INSTRUCTION.md.
- [ ] akr-capability-map.json is attached and reflects current repository metadata.
- [ ] At least one active business capability artifact exists in the business docs repository.

## After metadata changes
Trigger: merge that updates modules.yaml or source doc front matter.

- [ ] Regenerate akr-capability-map.json using the generation script.
- [ ] Remove the previous akr-capability-map.json from the Space file attachments.
- [ ] Attach the new akr-capability-map.json to the Space.
- [ ] Run the following two smoke prompts and confirm the expected mode is returned:
  - Full evidence prompt: ask about a capability that has both source module docs
    and a consolidation index.md. Expected: [MODE: BUSINESS + TECHNICAL].
  - Technical only prompt: ask about a capability that has source docs but no
    consolidation artifact. Expected: [MODE: TECHNICAL ONLY] with a business
    context note.
- [ ] Record update date in the maintenance log.

## After Space instruction changes
- [ ] Save updated text in docs/AKR_SPACE_INSTRUCTION.md first.
- [ ] Apply the same text in the Space instruction field.
- [ ] Run 5-question smoke test:
  - [ ] Full evidence
  - [ ] Technical only
  - [ ] Ambiguous
  - [ ] Insufficient evidence
  - [ ] Conflict

## After new capability onboarding
Trigger: a new businessCapability has been defined and its first source module
docs have been merged.

- [ ] Confirm the new capability name appears in akr-capability-map.json.
- [ ] Confirm at least index.md exists in the consolidation repository under
  docs/business-capabilities/new/ or active/ for the new capability.
- [ ] Regenerate and re-attach akr-capability-map.json to the Space.
- [ ] Run one smoke prompt using the new capability name.
  Expected: [MODE: TECHNICAL ONLY] if no consolidation doc exists yet,
  or [MODE: BUSINESS + TECHNICAL] if index.md is already present.
- [ ] If the capability returns [MODE: AMBIGUOUS], check that businessCapability
  metadata in the source module docs matches the name in akr-capability-map.json
  exactly, including capitalisation.
- [ ] Record update in the maintenance log.

## Maintenance log
| Date | Change | Updated by | Verification done |
|---|---|---|---|
| YYYY-MM-DD | Initial template | TODO | TODO |
