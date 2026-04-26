# enhancement-review-close

## Purpose

Confirm that the iterative enhancement review process is complete for all reviewed ENH-xxx entries in an active capability's `enhancements.md`, then strip all review-related blocks from the file to produce a clean, lean document ready for coding handoff.

This mode is the final step in the `enhancement-review` workflow. It must only be run after at least one iteration of `enhancement-review` has been completed. It does not re-assess requirements. It only validates close-readiness and removes review scaffolding.

## Status applicability

**Active capabilities only.** Enforced by dispatcher pre-check in `SKILL.md`.

## Inputs

- `enhancements.md` (the artifact to close and clean)

## Execution Steps

### Step 1: Locate review blocks

- Scan `enhancements.md` for all `#### Enhancement Review` sections marked with `<!-- akr-capability: review-in-progress -->`.
- If none are found, stop and return:
  "No active review blocks found in `enhancements.md` for <CapabilityName>. Run `/akr-capability enhancement-review [CapabilityName]` first."

### Step 2: Validate close-readiness for each block

For each review block found, check:

| Check | Pass condition |
|---|---|
| No open Business Requirements gaps | The Open Gaps — Business Requirements section contains only `None identified.` or the section is absent |
| No open Technical Requirements gaps | The Open Gaps — Technical Requirements section contains only `None identified.` or the section is absent |
| All Required Actions checked | Every item under Required Actions Before Coding Handoff begins with `- [x]` (not `- [ ]`) |
| Routing decision is not 🚫 | The Routing Decision line does not begin with 🚫, unless an Override Record has been filled in with a non-N/A approver |

### Step 3: Report readiness status

Produce a close-readiness table in chat:

| Enhancement ID | Open Gaps | All Actions Checked | Routing | Override Present | Close-Ready |
|---|---|---|---|---|---|
| ENH-xxx | 0 | Yes / No | ✅ / ⚠️ / 🚫 | Yes / No | ✅ Ready / ❌ Blocked |

### Step 4: Handle blocked enhancements

If any enhancement is not close-ready:

- List the specific unresolved items for each blocked enhancement.
- State: "The following enhancements are not ready to close. Address the listed items and re-run `/akr-capability enhancement-review [CapabilityName]` before closing."
- Do not modify `enhancements.md`.
- Stop.

If all enhancements are close-ready, proceed to Step 5.

### Step 5: Request explicit PO/TL confirmation

Before making any changes to `enhancements.md`, ask the user:

> "All enhancement review blocks are close-ready. Confirming will:
> 1. Promote resolved `## Questions and Gaps` items and addressed `## Dependencies and Risks` items into the appropriate Business or Technical Requirements sections of each ENH entry.
> 2. Remove all `#### Enhancement Review` blocks from `enhancements.md`.
> 3. Clear promoted items from `## Questions and Gaps` and `## Dependencies and Risks`.
> 4. Update the Enhancement Activity table Status to `Review Closed` for each closed ENH entry.
> 5. Update front matter metadata (`status`, `steps-completed`, `generated-at`).
>
> The final routing decision for each enhancement is:
>
> [list each ENH-xxx and its final routing decision]
>
> Type **confirm** to proceed, or **cancel** to abort. **Note:** Cancelling will leave the review blocks in place and will not update the Enhancement Activity table or front matter metadata."

Do not proceed until the user explicitly responds with **confirm**. If the user responds with anything other than **confirm**, stop and make no changes.

### Step 6: Promote resolved Questions and Gaps items into requirements

For each item in `## Questions and Gaps` marked with `✅`:

- Read the resolved statement.
- Classify it as a Business Requirement clarification or a Technical Requirement clarification:
  - **Business Requirement** if it defines user-visible behavior, acceptance conditions, optionality rules, or scope boundaries (e.g., "field is optional", "no downstream integrations in scope").
  - **Technical Requirement** if it defines implementation decisions, data design, storage format, API contract, or persistence behavior (e.g., "surrogate key strategy", "ISO code as business key", "LOV display format").
- If the resolved statement is already explicitly captured in the existing Business or Technical Requirements with equivalent specificity, do not duplicate it — mark it as `already incorporated` for cleanup only.
- If it adds specificity not yet present, append it as a bullet to the appropriate section of the relevant ENH entry:
  - Business Requirement clarifications → append to `#### Business Requirements`.
  - Technical Requirement clarifications regarding data design or API contract → append to `##### Implementation Scope` under `- Other implementation notes:`.
  - Technical Requirement clarifications regarding constraints or known limitations → append to `##### Dependencies and Limitations` under `- Technical limitations or constraints:`.

Use judgment to normalize the statement into requirement-style language (declarative, implementable).

### Step 7: Promote addressed Dependencies and Risks items into requirements

For each item in `## Dependencies and Risks`:

- A **Risk** or **Dependency** item is considered addressed if:
  - A corresponding **Mitigation** entry exists and the mitigation fully resolves the risk or dependency, OR
  - The risk/dependency was explicitly confirmed as resolved during the enhancement review iterations.
- An item is considered **still open** if it represents an unresolved forward-looking risk or a real pre-release dependency without a confirmed mitigation.
- For **addressed** items:
  - Incorporate the mitigation or confirmation into the relevant ENH Technical Requirements `##### Dependencies and Limitations` section as a technical constraint or confirmed note, if not already present.
  - Mark the addressed item (and its corresponding Mitigation entry) for removal in Step 9.
- For **open** items: leave them unchanged.

### Step 8: Strip all review blocks

After promoting resolved content, for each ENH-xxx entry in `enhancements.md`:

- Remove the entire `#### Enhancement Review` block, from the `#### Enhancement Review` heading line through to (and including) the last line of the `##### Override Record` section.
- Remove the `<!-- akr-capability: review-in-progress -->` marker.
- Do not modify any content outside the review block — Business Requirements, Technical Requirements, Implementation Scope, Dependencies and Limitations, and all other sections must be preserved exactly as the PO/TL left them, except for the additions made in Steps 6 and 7.

### Step 9: Clean Questions and Gaps and Dependencies and Risks sections

- In `## Questions and Gaps`: remove all `✅` items. If no items remain, replace the section body with `None.`
- In `## Dependencies and Risks`: remove addressed Risk, Dependency, and Mitigation lines identified in Step 7. If no items remain, replace the section body with `None.` Leave open items unchanged.

### Step 10: Update front matter metadata and Enhancement Activity table

#### 10a: Update front matter metadata

In the YAML front matter block at the top of `enhancements.md`, apply the following updates:

- Set `status` to `review-complete` (replacing any prior value such as `draft`).
- Set the `<!-- steps-completed: N -->` comment to reflect the total number of steps completed in this close execution (count Steps 1–10 that executed without being skipped).
- Set the `<!-- generated-at: ... -->` comment to the current UTC date and time in ISO 8601 format (e.g., `generated-at: 2026-04-22T00:00:00Z`). Replace any placeholder value such as `NEEDS`.

#### 10b: Add close record to Enhancement Activity table

In the Enhancement Activity summary table at the top of `enhancements.md`, update each closed ENH-xxx row:

- Set the Status column to `Review Closed` if it was previously set to a review-in-progress value.
- Leave all other columns unchanged.

### Step 11: Confirm completion

State in chat:

> "Review blocks have been removed from `enhancements.md` for <CapabilityName>. Resolved items have been incorporated into requirements and cleaned from `## Questions and Gaps` and `## Dependencies and Risks`. The file is now clean and ready for coding handoff. Final routing decisions:"
>
> [repeat the routing decision list from Step 5]
>
> "Invoke your coding agent when ready."

> Invoked via `/akr-capability enhancement-review-close [CapabilityName]`. This script is part of the `akr-capability` skill family.
