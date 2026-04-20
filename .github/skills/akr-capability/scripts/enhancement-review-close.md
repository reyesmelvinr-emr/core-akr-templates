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

> "All enhancement review blocks are close-ready. Confirming will remove all `#### Enhancement Review` blocks from `enhancements.md`, leaving only the core requirements content. The final routing decision for each enhancement is:
>
> [list each ENH-xxx and its final routing decision]
>
> Type **confirm** to proceed, or **cancel** to keep the review blocks."

Do not proceed until the user explicitly responds with **confirm**. If the user responds with anything other than **confirm**, stop and make no changes.

### Step 6: Strip all review blocks

After confirmation, for each ENH-xxx entry in `enhancements.md`:

- Remove the entire `#### Enhancement Review` block, from the `#### Enhancement Review` heading line through to (and including) the last line of the Override Record section.
- Remove the `<!-- akr-capability: review-in-progress -->` marker.
- Do not modify any content outside the review block — Business Requirements, Technical Requirements, Implementation Scope, Dependencies and Limitations, and all other sections must be preserved exactly as the PO/TL left them.

### Step 7: Add close record to Enhancement Activity table

In the Enhancement Activity summary table at the top of `enhancements.md`, update each closed ENH-xxx row:

- Set the Status column to `Review Closed` if it was previously set to a review-in-progress value.
- Leave all other columns unchanged.

### Step 8: Confirm completion

State in chat:

> "Review blocks have been removed from `enhancements.md` for <CapabilityName>. The file is now clean and ready for coding handoff. Final routing decisions:"
>
> [repeat the routing decision list from Step 5]
>
> "Invoke your coding agent when ready."

> Invoked via `/akr-capability enhancement-review-close [CapabilityName]`. This script is part of the `akr-capability` skill family.
