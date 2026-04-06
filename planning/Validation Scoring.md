This is a well-reasoned direction. Let me think through what this actually requires and where the real design challenges are.

---

## The Core Idea and Why It's Sound

What you're describing is a two-component scoring system:

- **Structural score** — what `validate_documentation.py` already produces (section presence, front matter validity, marker counts, penalty deductions)
- **Semantic score** — an LLM-evaluated relevance rating per human-authored section, combined into a document-level signal

The key insight in your proposal is that *intent to contribute* should score better than *abandonment*. A developer who writes "For further confirmation" is signaling that they engaged with the section and made a conscious decision to defer it. That's categorically different from a section that still contains the original template placeholder text or an unmodified ❓ marker. The LLM is well-positioned to detect this distinction because it can understand the difference between acknowledgment of a gap and absence of engagement.

---

## The Human-Authored Fields Problem Reframed

Your point about the original document generator not knowing how to fill certain sections is the right reframe. The mandatory human-authored fields detection I described was framed as a validation gate — which implicitly assumes the person generating the document is the same person who should fill the business context fields. That assumption is wrong.

The better model is a **handoff-aware workflow**. The generating developer produces a structurally complete draft with ❓ markers in sections they can't answer. The document then needs to reach the right domain expert before it can graduate to production. The semantic scoring system you're proposing is actually the mechanism that enforces this handoff — a document where all the business context sections still contain template text or bare ❓ markers will score poorly, and that score should block the merge until someone with the right knowledge engages with those sections.

This reframes validation from "did you fill this in" to "did the right person engage with this document." The LLM score is the signal for engagement quality.

---

## How the Semantic Scoring Would Work

The flow would look like this at a high level:

```
Document submitted for validation
         ↓
validate_documentation.py runs
  → structural_score (0–100)
  → list of sections with their content
         ↓
LLM scoring call (per human-authored section)
  → relevance_score per section (0–10)
  → engagement_classification per section
         ↓
combined_score = weighted_average(structural_score, semantic_scores)
  → pass / warn / fail based on team-configured threshold
```

### Section classification before scoring

Before the LLM evaluates content quality, the validator needs to classify each section by its authorship expectation. Not all sections should be scored the same way:

| Section type | Scoring approach |
|---|---|
| AI-generated structural sections (Module Files, Operations Map) | Structural validation only — no semantic scoring |
| Mixed sections (Architecture Overview, Business Rules description column) | Score only the human-authored rows/cells |
| Fully human-authored sections (Why It Exists, Since When, Quick Reference business context) | Full semantic scoring |
| Explicitly deferred sections (DEFERRED marker with rationale) | Score the rationale text, not the deferred content |

The `akr:section` directives in the templates already carry metadata about which sections are human-authored vs. AI-generated. The `parse_template_directives.py` script can be extended to include an `authorship` field in directive blocks:

```
<!-- akr:section
id: business_rules
title: Business Rules
required: true
order: 5
authorship: mixed
human_columns: [why_it_exists, since_when]
-->
```

This gives the scoring system an explicit map of what to evaluate rather than asking the LLM to guess.

### The LLM scoring prompt design

The scoring call needs to be carefully designed to produce consistent, calibrated results. The prompt should give the LLM:

1. The document title and module purpose (so it can judge relevance to context)
2. The specific section content to evaluate
3. The section's expected purpose (from the directive metadata)
4. A defined scoring rubric that the LLM applies consistently

A rubric that operationalizes your intent would look like this:

```
Score 0-2: Template placeholder text unchanged, or bare ❓ marker 
           with no surrounding context. No evidence of human 
           engagement.

Score 3-4: Some attempt at content but clearly generic — could apply 
           to any module. No specific business context.

Score 5-6: Content is module-specific and acknowledges the actual 
           domain, even if incomplete. Includes explicit deferrals 
           like "For further confirmation" or "Not available as of 
           the moment" that demonstrate awareness of the gap.

Score 7-8: Content is substantive and relevant. Business context is 
           evident. Some gaps may exist but they are acknowledged 
           explicitly.

Score 9-10: Content is complete, specific to this module, and 
            demonstrates genuine domain knowledge. No unexplained 
            gaps.
```

The critical design choice here is that scores 5-6 explicitly reward the "For further confirmation" case. A developer who writes that is communicating something meaningful — they know the section exists, they know they can't answer it, and they've flagged it for someone else. That should score better than leaving the template placeholder because it's honest and actionable.



The `is_template_text` flag is important — it's a binary check for whether the content is literally the unchanged template placeholder text, which should be treated as a hard failure rather than just a low score.

---

## The Combined Score Architecture

### Weighting

The structural score and semantic score operate at different scales and have different governance meanings, so they shouldn't be averaged naively. A reasonable starting weight distribution would be:

```
structural_score  →  40% of combined score
semantic_score    →  60% of combined score
```

The semantic score gets higher weight because structural compliance is a necessary but not sufficient condition for a useful document. A structurally perfect document with no meaningful human input is worse governance than a structurally imperfect document with genuine business context filled in.

The semantic score itself is the average of individual section scores, but weighted by section importance. Business Rules "Why It Exists" and Quick Reference business context should count more than a peripheral questions and gaps section.

### Threshold configuration

Different teams and compliance modes should have different thresholds. These belong in the project's `modules.yaml` or `.akr-config.json`:

```yaml
project:
  name: TrainingTracker.Api
  compliance_mode: production
  scoring:
    minimum_combined_score: 70
    minimum_semantic_score: 60
    minimum_structural_score: 80
    block_on_template_text: true
    block_on_unengaged_sections: 2  # max sections with score < 3
```

For pilot mode, the thresholds are advisory — scores below threshold produce warnings. For production mode, they're blocking.

### What the output looks like

The combined scoring output should be surfaced in the PR comment in a way that's actionable, not just a number:

```
## AKR Documentation Quality Report: CourseDomain

Combined Score: 74/100  ⚠️ Below production threshold (80)

Structural Score:  85/100  ✅
Semantic Score:    67/100  ⚠️

Section Scores:
  Module Files          ——  (structural only)
  Operations Map        ——  (structural only)
  Business Rules        6/10  ⚠️  "Why It Exists" column contains 
                               acknowledged gaps — needs domain expert input
  Architecture Overview 8/10  ✅
  Quick Reference       4/10  ❌  Generic content, no module-specific 
                               business context
  Data Operations       7/10  ✅
  Questions & Gaps      5/10  ⚠️  Acknowledged gaps present

Sections requiring domain expert input before production merge:
  → Business Rules: "Why It Exists" — 3 rows awaiting business rationale
  → Quick Reference: Business context section needs product owner input

Unengaged sections (template text unchanged): 0  ✅
```

This output is more useful than a raw validation failure because it tells the team *who* needs to act, not just *what* is wrong. "Needs domain expert input" is actionable. "Validation failed" is not.

---
For a proof of concept the goal is to validate the approach with minimal moving parts, not to build the full system. Let me focus on what's actually necessary to demonstrate the value.

---

## What the PoC Needs to Prove

The core hypothesis is: **LLM semantic scoring can meaningfully distinguish engaged human input from abandoned template text, and that signal is useful to a tech lead reviewing a PR.** Everything in the PoC design should serve that hypothesis and nothing else.

---

## Minimal Architecture

### Git diff as the section filter

Your instinct about using git history is the right call. Instead of scoring every section on every run, the validator compares the current document against its previous committed version and extracts only the changed sections. This eliminates the cost and latency concern for incremental runs — in practice most PRs change one or two sections, so most scoring runs are one or two LLM calls.

The approach is straightforward:

```python
def get_changed_sections(doc_path: str) -> list[dict]:
    """
    Compare current file against HEAD~1 and return only 
    sections whose content changed.
    """
    import subprocess
    
    # Get the previous version of the file
    result = subprocess.run(
        ["git", "show", f"HEAD:{doc_path}"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        # New file — all sections are changed
        return extract_all_sections(doc_path)
    
    previous_content = result.stdout
    current_content = Path(doc_path).read_text(encoding="utf-8")
    
    previous_sections = extract_sections(previous_content)
    current_sections = extract_sections(current_content)
    
    changed = []
    for section_id, content in current_sections.items():
        prev_content = previous_sections.get(section_id, "")
        if content.strip() != prev_content.strip():
            changed.append({
                "section_id": section_id,
                "content": content,
                "is_new": section_id not in previous_sections
            })
    
    return changed
```

For a new document (no previous commit), all sections are treated as changed and scored. For subsequent PRs, only the sections the developer actually touched get scored. This is also honest from a governance perspective — the score attached to an unchanged section reflects when it was last evaluated, not a stale assumption about its current state.

### Section extraction

The section extraction function needs to be simple and reliable. For the PoC, heading-to-heading extraction is sufficient. The known edge cases (nested headings, code blocks, tables) don't need to be handled perfectly — just consistently:

```python
def extract_sections(content: str) -> dict[str, str]:
    """
    Extract ## level sections as a dict of normalized_heading -> content.
    Content includes everything between this heading and the next ## heading.
    """
    sections = {}
    current_heading = None
    current_lines = []
    
    for line in content.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = re.sub(r"[^a-z0-9]+", "", line[3:].strip().lower())
            current_lines = []
        elif current_heading is not None:
            current_lines.append(line)
    
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()
    
    return sections
```

This is intentionally naive. It will have edge cases. For the PoC that's acceptable — you're validating the scoring concept, not building a production-grade markdown parser.

### Which sections get scored

For the PoC, hardcode the list of human-authored sections rather than reading from directive metadata. The directive-based approach is the right long-term design but adds complexity you don't need yet. A simple lookup in `validate_documentation.py` is sufficient:

```python
HUMAN_AUTHORED_SECTIONS = {
    "quickreferencetldr": {
        "display_name": "Quick Reference (TL;DR)",
        "purpose": "Business context: why this module exists and when to use it",
        "weight": 1.5
    },
    "businessrules": {
        "display_name": "Business Rules",
        "purpose": "Business rationale for enforcement rules, including Why It Exists and Since When columns",
        "weight": 2.0
    },
    "purposeandscope": {
        "display_name": "Purpose and Scope",
        "purpose": "Business purpose and scope boundaries of this module",
        "weight": 1.5
    },
    "questionsandgaps": {
        "display_name": "Questions and Gaps",
        "purpose": "Unresolved questions and gaps requiring human input",
        "weight": 1.0
    }
}
```

Weights are relative — Business Rules gets the highest weight because it's the section where business context is most critical and most commonly left as a placeholder.

---

## The Scoring Call

Keep it minimal. One call per changed human-authored section, structured output, low temperature:

```python
def score_section(
    section_id: str,
    section_content: str,
    module_name: str,
    section_purpose: str
) -> dict:
    
    import anthropic
    client = anthropic.Anthropic()
    
    prompt = f"""You are evaluating a section of technical module documentation.

Module: {module_name}
Section: {section_id}
Expected purpose: {section_purpose}

Content to evaluate:
---
{section_content[:2000]}
---

Score this content 0-10:
0-2: Unchanged template placeholder or bare unresolved marker. No human engagement.
3-4: Generic content, could apply to any module. No specific context.
5-6: Module-aware, even if incomplete. Explicit acknowledgment of gaps 
     ("For further confirmation", "Not available as of the moment", 
     "Pending confirmation from product owner") scores here.
7-8: Substantive and module-specific. Business context evident.
9-10: Complete and specific. Demonstrates genuine domain knowledge.

Respond with JSON only, no other text:
{{"score": <0-10>, "classification": "<placeholder|generic|acknowledged_gap|substantive|complete>", "rationale": "<one sentence>"}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError:
        return {"score": 0, "classification": "error", "rationale": "Could not parse scoring response"}
```

Truncating the section content to 2000 characters keeps token costs low. For the PoC this is a reasonable tradeoff — sections longer than 2000 characters are almost certainly not template placeholders anyway.

---

## Integrating Into validate_documentation.py

Add a new function that orchestrates the semantic scoring and produces a result that integrates cleanly with the existing validation output:

```python
def run_semantic_validation(
    doc_path: str,
    module_name: str,
    compliance_mode: str
) -> dict:
    
    changed_sections = get_changed_sections(doc_path)
    
    if not changed_sections:
        return {
            "ran": False,
            "reason": "No sections changed since last commit",
            "section_scores": {},
            "semantic_score": None
        }
    
    section_scores = {}
    total_weighted_score = 0
    total_weight = 0
    
    for section in changed_sections:
        section_id = section["section_id"]
        
        if section_id not in HUMAN_AUTHORED_SECTIONS:
            continue
        
        meta = HUMAN_AUTHORED_SECTIONS[section_id]
        
        # Hard check: is this literally template placeholder text?
        is_template = _is_template_placeholder(section["content"])
        
        if is_template:
            result = {
                "score": 0,
                "classification": "placeholder",
                "rationale": "Content matches template placeholder text",
                "is_template_text": True
            }
        else:
            result = score_section(
                section_id=section_id,
                section_content=section["content"],
                module_name=module_name,
                section_purpose=meta["purpose"]
            )
            result["is_template_text"] = False
        
        section_scores[section_id] = {
            **result,
            "display_name": meta["display_name"],
            "weight": meta["weight"]
        }
        
        total_weighted_score += result["score"] * meta["weight"]
        total_weight += meta["weight"]
    
    semantic_score = (
        round((total_weighted_score / total_weight) * 10, 1)
        if total_weight > 0 else None
    )
    
    return {
        "ran": True,
        "section_scores": section_scores,
        "semantic_score": semantic_score,
        "has_template_text": any(
            s["is_template_text"] for s in section_scores.values()
        )
    }
```

The `_is_template_placeholder` check is a fast regex pass before the LLM call — if the content matches known template patterns (🤖 markers, ❓ markers without surrounding text, or literal bracket placeholders like `[HUMAN: ...]`), skip the API call entirely and score it zero. This handles the obvious cases without spending tokens.

```python
def _is_template_placeholder(content: str) -> bool:
    stripped = content.strip()
    
    # Empty or only whitespace
    if not stripped:
        return True
    
    # Only markers with no surrounding content
    cleaned = re.sub(r"[🤖❓]", "", stripped).strip()
    if not cleaned:
        return True
    
    # Literal template placeholder patterns
    placeholder_patterns = [
        r"^\[HUMAN:.*\]$",
        r"^❓\s*\[HUMAN:.*\]$",
        r"^🤖\s*\[AI:.*\]$",
        r"^\[.*\]$"
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, stripped, re.DOTALL):
            return True
    
    return False
```

---

## Combined Score Calculation

Keep the weighting simple for the PoC. The structural score comes from the existing `_compute_completeness` function. The combined score is a straightforward weighted average:

```python
def compute_combined_score(
    structural_score: float,
    semantic_result: dict
) -> dict:
    
    if not semantic_result["ran"] or semantic_result["semantic_score"] is None:
        # No semantic scoring ran — use structural score only
        return {
            "combined_score": structural_score,
            "structural_score": structural_score,
            "semantic_score": None,
            "semantic_weight_applied": False
        }
    
    semantic_score = semantic_result["semantic_score"]
    
    # 40% structural, 60% semantic for the PoC
    combined = round(
        (structural_score * 0.4) + (semantic_score * 0.6), 1
    )
    
    return {
        "combined_score": combined,
        "structural_score": structural_score,
        "semantic_score": semantic_score,
        "semantic_weight_applied": True
    }
```

---

## Output in the PR Comment

The PR comment is where the tech lead and product owner see the results. For the PoC, the output should be informative enough to be useful without being overwhelming:

```markdown
## AKR Documentation Quality: CourseDomain

Combined Score: 71/100  ⚠️

| Component | Score | Weight |
|---|---|---|
| Structural | 85/100 | 40% |
| Semantic | 61/100 | 60% |

**Section Scores (changed sections only):**

| Section | Score | Classification | Notes |
|---|---|---|---|
| Business Rules | 5/10 | acknowledged_gap | Why It Exists column has explicit deferrals — domain expert input needed |
| Quick Reference | 4/10 | generic | Content does not reference specific module behavior |
| Questions & Gaps | 7/10 | substantive | Specific questions raised with context |

⚠️ 1 section awaiting domain expert input before production merge.

_Semantic scoring applied to 3 changed sections. Unchanged sections retain previous scores._
```

The note about which sections were scored and which retained previous scores is important transparency — it tells the reviewer exactly what was evaluated in this PR.

---

## What to Leave Out of the PoC

To keep it minimal:

**No persistent score storage.** Each PR run scores from scratch against the git diff. You lose the "unchanged sections retain previous scores" capability for now, which means on a first full run you score all human-authored sections. On subsequent PRs you only score changed sections. That's sufficient for the PoC.

**No configurable thresholds.** Use hardcoded thresholds for the PoC: 70 combined, 60 semantic minimum. Make them constants at the top of the file so they're easy to find and adjust based on what you learn.

**No directive metadata integration.** The hardcoded `HUMAN_AUTHORED_SECTIONS` dict is sufficient. The directive-based approach is the right long-term design but adds complexity that doesn't help validate the core hypothesis.

**No score caching.** The git diff approach already limits scoring to changed sections, which solves the cost problem for incremental runs. Caching adds implementation complexity for marginal additional benefit at this stage.

**Warn-only mode regardless of compliance mode.** For the PoC, the semantic score should never block a merge. It should surface in the PR comment as information for the tech lead and product owner who are doing the actual approval. That's consistent with your point that human review is the real gate — the score is a signal that supports the review, not a replacement for it.

This last point is the most important PoC design decision. You're building a tool to help reviewers, not to automate their judgment. Keeping it advisory during the PoC lets you observe whether the scores are actually useful to reviewers before you make any of them blocking.