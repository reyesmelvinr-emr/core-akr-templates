# AKR Copilot Space - Developer Quickstart

Date: 2026-04-21
Audience: Developers using AKR Copilot Space

## What this Space does and how to access it
This Space improves Copilot's retrieval focus by combining module mappings and
capability-tagged documentation across three repositories: the backend codebase,
the UI codebase, and the business documentation repository.

Copilot in this Space follows AKR retrieval policies automatically. You do not
need to reference any files or invoke any skills. Ask your question in the Space
and Copilot will declare what kind of answer it was able to produce based on
the evidence it found.

**Access this Space here:**
- TODO: insert Space URL

Ask all capability-scoped questions through this Space URL, not through your
IDE or a regular Copilot Chat window. Regular Copilot Chat does not apply
AKR retrieval policies and will produce unscoped answers.

## Ask better questions
Good prompts include one of these anchors:
- businessCapability name
- module name
- explicit file reference

Examples:
- How does EnrollmentManagement handle duplicate enrollment submissions?
- In enrollment-service module, what happens when the user is already enrolled?
- Based on docs/services/enrollment-service.md, what are known limitations?

## Response modes and what to do with each

**[MODE: BUSINESS + TECHNICAL]**
Both technical and business evidence were found. High confidence.
Sources are listed at the end of the answer.
Action: Use the answer. Check the sources cited if you need to verify.

**[MODE: TECHNICAL ONLY]**
Technical evidence was found but no business documentation exists in the
consolidation repository for this capability.
Action: Use the technical answer for code-level questions. For business impact
or requirements questions, escalate to the Space owner — the consolidation
repository may be missing an index.md for this capability.

**[MODE: AMBIGUOUS]**
Copilot could not determine which capability or module your question is about,
or multiple targets matched with no clear anchor.
Action: Add a capability name, module name, or explicit file reference
to your question and ask again.

**[MODE: INSUFFICIENT EVIDENCE]**
Copilot could not find enough grounded technical evidence to answer.
Action: Reference the specific module files explicitly using their path
in your question and ask again. If the problem persists, escalate to
the Space owner — modules.yaml or front matter metadata may be missing.

## Expected limits (POC)
- Retrieval can miss relevant files even when they exist.
- Answers may vary if metadata is incomplete.
- Ambiguous questions produce lower-confidence outputs.

## If results look wrong
Escalate to the Space owner and include all of the following:

1. The exact prompt you used.
2. The response mode returned.
3. The capability or module you expected the answer to cover.
4. The mode you expected to see and why.
5. Any file or metadata you believe is missing or incorrectly tagged.

The Space owner will check whether the issue is a missing capability map
entry, missing front matter metadata, a stale map attachment, or a gap
in the consolidation repository.
