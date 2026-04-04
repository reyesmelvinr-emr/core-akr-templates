#!/usr/bin/env python3
"""
AKR Template Directive Parser — parse_template_directives.py

Extracts akr: generation contract directives from a template file and emits
them as structured JSON for deterministic model or tooling consumption.

This is the canonical parser for the directive architecture. Without it,
akr: directive blocks must be parsed by the LLM itself, which is unreliable
for structured attribute extraction. This script makes parsing deterministic
regardless of model attention behavior or context window size.

Callers
-------
  akr-generate.md (Step 2): Pre-parse template before model invocation.
      The JSON output is injected into the model context as structured facts,
      replacing the need for the model to read and parse raw template text.

  CI (validate-documentation.yml): Validate that template directives are
      internally consistent (all condition references resolve, no duplicate
      section IDs, required fields present) before accepting template changes.

  validate_documentation.py: Import parse_template() to get authoritative
      required section lists instead of using hardcoded MODULE_REQUIRED_SECTIONS.

Usage
-----
  # Output JSON (default — feed to model or tooling)
  python parse_template_directives.py templates/lean_baseline_service_template_module.md

  # Human-readable summary (debugging)
  python parse_template_directives.py <template> --output text

  # Validate directive syntax only — no stdout output, exit 1 on errors
  python parse_template_directives.py <template> --validate

  # Pretty-print JSON
  python parse_template_directives.py <template> --pretty

JSON Output Schema
------------------
  {
    "template": {
      "id":            string,
      "version":       string,
      "project_types": [string, ...],
      "charter":       string
    },
    "conditions": {
      "<token>": "<detection description>",
      ...
    },
    "sections": [
      {
        "id":               string,          -- snake_case identifier
        "required":         bool,
        "order":            string,          -- raw order value ("8", "7a")
        "order_sort_key":   float,           -- "7a" -> 7.1 for stable sorting
        "condition":        string | null,   -- condition token or null
        "columns":          [string, ...],   -- table column names if declared
        "rule_id_format":   string | null,
        "violation":        string | null,
        "diagram_format":   string | null,
        "grounding":        string | null,
        "coverage":         string | null,
        "note":             string | null,
        "format":           string | null,
        "guidance":         string | null,
        "sub_sections":     [string, ...],
        "sub_tables":       [string, ...],
        "fields":           [string, ...],
        "markers":          [string, ...],
        "marker_guidance":  string | null,
        "flow_fields_per_step": [string, ...],
        "required_elements": [string, ...],
        "source":           string | null,
        "sync_note":        string | null
      },
      ...                                    -- sorted by order_sort_key ascending
    ],
    "required_sections":     [string, ...], -- IDs of required unconditional sections
    "conditional_sections":  [{"id": string, "condition": string}, ...],
    "parsing_errors":        [string, ...]  -- non-empty if any block had errors
  }

Exit Codes
----------
  0  = success (or --validate passed with no errors)
  1  = parsing/validation errors present
  2  = usage error (file not found, bad arguments)

Notes
-----
  - Pure Python stdlib — no pip install required.
  - Directive blocks are HTML comments (<!-- ... -->) containing lines that
    start with "akr:" after optional whitespace.
  - Inline attributes use key=value syntax: id=foo required=true order=8
  - Body attributes use YAML-style indented key: value syntax.
  - List values use inline YAML style: [item1, item2, item3]
  - Order values may include a single lowercase letter suffix: "7a", "7b".
    These sort after their integer prefix (7 < 7a < 7b < 8).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# HTML comment extraction
# Using re.DOTALL so '.' matches newlines, enabling multi-line comment capture.
# This avoids the [^>] anti-pattern which breaks on '>' inside comment bodies.
# ---------------------------------------------------------------------------

_COMMENT_PATTERN = re.compile(r"<!--(.*?)-->", re.DOTALL)


def _extract_directive_blocks(content: str) -> List[Tuple[str, int]]:
    """
    Return all HTML comment blocks that contain at least one akr: directive line.
    Each entry is (inner_block_text, start_char_position_in_content).
    start_char_position is used for error messages only.
    """
    results: List[Tuple[str, int]] = []
    for match in _COMMENT_PATTERN.finditer(content):
        inner = match.group(1)
        if re.search(r"^\s*akr:", inner, re.MULTILINE):
            results.append((inner, match.start()))
    return results


# ---------------------------------------------------------------------------
# Inline attribute parser
# Handles: key=value  key="quoted value"  key='single quoted'
# Does NOT handle values with embedded '=' — values must be simple tokens or
# quoted strings. This is sufficient for all known akr: directive attributes.
# ---------------------------------------------------------------------------

_INLINE_ATTR_PATTERN = re.compile(
    r'(\w[\w\-]*)'       # key: word characters and hyphens
    r'\s*=\s*'           # = with optional surrounding whitespace
    r'(?:'
    r'"([^"]*?)"'        # double-quoted value
    r"|"
    r"'([^']*?)'"        # single-quoted value
    r"|"
    r"([^\s>\"'=]+)"     # unquoted token (no whitespace, >, ", ', or =)
    r")"
)


def _parse_inline_attrs(attr_string: str) -> Dict[str, str]:
    """
    Parse key=value pairs from a single attribute string line.
    All values are returned as strings; callers cast as needed.
    Returns an empty dict if attr_string is empty or contains no pairs.
    """
    attrs: Dict[str, str] = {}
    for match in _INLINE_ATTR_PATTERN.finditer(attr_string):
        key = match.group(1)
        # Take first non-None capture group for the value
        value = next((g for g in (match.group(2), match.group(3), match.group(4)) if g is not None), "")
        attrs[key] = value
    return attrs


# ---------------------------------------------------------------------------
# Body attribute parser
# Handles indented lines in the format:   key: value
# List values: columns: [Rule ID, Rule Description, Why It Exists]
# ---------------------------------------------------------------------------

def _parse_list_value(value: str) -> List[str]:
    """
    Parse an inline YAML-style list: [item1, item2, item3].
    Returns a list of stripped item strings.
    Returns [value] if value is not list syntax (single-item fallback).
    """
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1]
        return [item.strip() for item in inner.split(",") if item.strip()]
    return [stripped] if stripped else []


def _parse_body_attrs(lines: List[str]) -> Dict[str, Any]:
    """
    Parse indented 'key: value' style attribute lines.
    Lines without ':' are silently skipped (comments, blank lines).
    List-valued attributes ([...]) are parsed into Python lists.
    All other values are strings.
    """
    attrs: Dict[str, Any] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, _, raw_value = stripped.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            continue
        # Detect and parse list values
        if raw_value.startswith("["):
            attrs[key] = _parse_list_value(raw_value)
        else:
            attrs[key] = raw_value
    return attrs


# ---------------------------------------------------------------------------
# Order value normalization
# Converts order strings to float sort keys for stable section ordering.
#   "0"  -> 0.0
#   "8"  -> 8.0
#   "7a" -> 7.1   (a=0.1, b=0.2, ..., z=2.6)
#   "7b" -> 7.2
# ---------------------------------------------------------------------------

_ORDER_PATTERN = re.compile(r"^(\d+)([a-z]?)$", re.IGNORECASE)


def _order_sort_key(order_str: str) -> float:
    """
    Convert an order attribute value to a float sort key.
    Raises ValueError if the format is unrecognized.
    """
    order_str = order_str.strip()
    match = _ORDER_PATTERN.match(order_str)
    if not match:
        raise ValueError(f"Unrecognized order format: '{order_str}'. Expected integer with optional letter suffix (e.g., 7, 7a).")
    numeric_part = int(match.group(1))
    letter_part = match.group(2).lower()
    fractional = (ord(letter_part) - ord("a") + 1) * 0.1 if letter_part else 0.0
    return float(numeric_part) + fractional


# ---------------------------------------------------------------------------
# Per-directive-type parsers
# ---------------------------------------------------------------------------

def _parse_akr_template_block(body_lines: List[str]) -> Dict[str, Any]:
    """
    Parse an akr:template block body into a template metadata dict.
    Expected fields: id, version, project_types (list), charter.
    """
    body = _parse_body_attrs(body_lines)
    project_types = body.get("project_types", [])
    # Normalize scalar value to list
    if isinstance(project_types, str):
        project_types = [project_types]
    return {
        "id": body.get("id", ""),
        "version": body.get("version", ""),
        "project_types": project_types,
        "charter": body.get("charter", ""),
    }


def _parse_akr_conditions_block(body_lines: List[str]) -> Dict[str, str]:
    """
    Parse an akr:conditions block into a dict mapping condition token -> description.
    Each non-blank body line: condition_token: "description text"
    """
    conditions: Dict[str, str] = {}
    for line in body_lines:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, _, raw_value = stripped.partition(":")
        key = key.strip()
        # Strip surrounding quotes from description
        raw_value = raw_value.strip().strip('"').strip("'")
        if key:
            conditions[key] = raw_value
    return conditions


def _parse_akr_section_block(inline_rest: str, body_lines: List[str]) -> Dict[str, Any]:
    """
    Parse an akr:section block into a section descriptor.

    The directive first line suffix (inline_rest) carries:
      id=<snake_case_id>  required=<true|false>  order=<N|Na>  condition=<token>

    Body lines carry:
      columns, rule_id_format, violation, diagram_format, grounding,
      coverage, note, format, guidance, sub_sections, sub_tables,
      fields, markers, marker_guidance, flow_fields_per_step,
      required_elements, source, sync_note

    Returns a fully populated section dict with all known keys present.
    Fields not found in the directive default to None or [].
    """
    inline = _parse_inline_attrs(inline_rest)
    body = _parse_body_attrs(body_lines)

    section_id = inline.get("id", "")
    required_str = inline.get("required", "true").lower()
    required = required_str not in ("false", "no", "0")
    order_str = inline.get("order", "0")
    condition = inline.get("condition") or None

    try:
        sort_key = _order_sort_key(order_str)
    except ValueError:
        sort_key = 9999.0  # Push malformed-order sections to end; error reported separately

    def _body_str(key: str) -> Optional[str]:
        val = body.get(key)
        return str(val) if val is not None else None

    def _body_list(key: str) -> List[str]:
        val = body.get(key, [])
        if isinstance(val, list):
            return val
        return [str(val)] if val else []

    return {
        "id": section_id,
        "required": required,
        "order": order_str,
        "order_sort_key": sort_key,
        "condition": condition,
        # Table structure
        "columns": _body_list("columns"),
        "rule_id_format": _body_str("rule_id_format"),
        "violation": _body_str("violation"),
        # Format constraints
        "diagram_format": _body_str("diagram_format"),
        "format": _body_str("format"),
        # Content guidance
        "grounding": _body_str("grounding"),
        "coverage": _body_str("coverage"),
        "note": _body_str("note"),
        "guidance": _body_str("guidance"),
        "source": _body_str("source"),
        "sync_note": _body_str("sync_note"),
        "marker_guidance": _body_str("marker_guidance"),
        # Sub-structure lists
        "sub_sections": _body_list("sub_sections"),
        "sub_tables": _body_list("sub_tables"),
        "fields": _body_list("fields"),
        "markers": _body_list("markers"),
        "flow_fields_per_step": _body_list("flow_fields_per_step"),
        "required_elements": _body_list("required_elements"),
    }


# ---------------------------------------------------------------------------
# Main parse entry point
# ---------------------------------------------------------------------------

def parse_template(template_path: Path) -> Dict[str, Any]:
    """
    Parse all akr: directives in a template file.

    Returns the complete generation contract as a dict. See module docstring
    for the full output schema.

    This function does not raise on individual directive parse errors — errors
    are accumulated in the returned 'parsing_errors' list so callers can
    decide whether to fail hard or warn.
    """
    content = template_path.read_text(encoding="utf-8")
    blocks = _extract_directive_blocks(content)

    template_meta: Optional[Dict[str, Any]] = None
    conditions: Dict[str, str] = {}
    sections: List[Dict[str, Any]] = []
    parsing_errors: List[str] = []

    for block_text, block_pos in blocks:
        # Split block into non-blank lines
        all_lines = block_text.splitlines()

        # Find the line containing the akr: directive type
        directive_line_idx: Optional[int] = None
        for i, line in enumerate(all_lines):
            if re.match(r"\s*akr:", line):
                directive_line_idx = i
                break

        if directive_line_idx is None:
            continue  # No akr: line found in this block (should not happen after _extract)

        directive_line = all_lines[directive_line_idx].strip()
        body_lines = all_lines[directive_line_idx + 1:]

        # Parse directive type and the rest of its first line
        directive_match = re.match(r"akr:(\w+)(.*)", directive_line, re.IGNORECASE)
        if not directive_match:
            parsing_errors.append(f"Unrecognized directive syntax at char {block_pos}: '{directive_line}'")
            continue

        directive_type = directive_match.group(1).lower()
        inline_rest = directive_match.group(2).strip()

        try:
            if directive_type == "template":
                if template_meta is not None:
                    parsing_errors.append("Multiple akr:template blocks found — only the first is used.")
                else:
                    template_meta = _parse_akr_template_block(body_lines)

            elif directive_type == "conditions":
                conditions.update(_parse_akr_conditions_block(body_lines))

            elif directive_type == "section":
                section = _parse_akr_section_block(inline_rest, body_lines)
                if not section["id"]:
                    parsing_errors.append(
                        f"akr:section at char {block_pos} is missing required 'id' attribute — section skipped."
                    )
                else:
                    sections.append(section)

            else:
                parsing_errors.append(
                    f"Unknown directive type 'akr:{directive_type}' at char {block_pos} — skipped."
                )

        except Exception as exc:  # noqa: BLE001
            parsing_errors.append(
                f"Error parsing 'akr:{directive_type}' block at char {block_pos}: {exc}"
            )

    # Sort sections by computed sort key (ascending)
    sections.sort(key=lambda s: (s["order_sort_key"], s["id"]))

    # Derive convenience index fields
    required_sections = [
        s["id"] for s in sections if s["required"] and s["condition"] is None
    ]
    conditional_sections = [
        {"id": s["id"], "condition": s["condition"]}
        for s in sections
        if s["condition"] is not None
    ]

    return {
        "template": template_meta or {},
        "conditions": conditions,
        "sections": sections,
        "required_sections": required_sections,
        "conditional_sections": conditional_sections,
        "parsing_errors": parsing_errors,
    }


# ---------------------------------------------------------------------------
# Directive contract validation
# ---------------------------------------------------------------------------

def validate_directives(parsed: Dict[str, Any]) -> List[str]:
    """
    Validate the internal consistency of a parsed directive contract.

    Checks:
      - akr:template block is present and has required fields
      - akr:conditions block is present (conditional sections need it)
      - All condition references in akr:section blocks resolve to declared tokens
      - No duplicate section IDs
      - All order values match the expected format
      - At least one section is declared

    Returns a list of error message strings. Empty list means the contract is valid.
    """
    errors: List[str] = list(parsed.get("parsing_errors", []))

    # --- Template block ---
    template = parsed.get("template", {})
    if not template:
        errors.append("akr:template block not found. Template metadata cannot be inferred by the model.")
    else:
        if not template.get("id"):
            errors.append("akr:template 'id' field is missing or empty.")
        if not template.get("version"):
            errors.append("akr:template 'version' field is missing or empty.")
        if not template.get("project_types"):
            errors.append("akr:template 'project_types' field is missing or empty.")
        if not template.get("charter"):
            errors.append("akr:template 'charter' field is missing or empty.")

    # --- Conditions block ---
    if not parsed.get("conditions"):
        errors.append(
            "akr:conditions block not found or empty. "
            "Sections with condition= attributes will evaluate incorrectly."
        )

    # --- Sections ---
    sections = parsed.get("sections", [])
    if not sections:
        errors.append("No akr:section blocks found. The generation contract is empty.")
        return errors  # Nothing more to check

    # Duplicate section ID check
    seen_ids: Dict[str, int] = {}
    for section in sections:
        sid = section["id"]
        if sid in seen_ids:
            errors.append(
                f"Duplicate section id '{sid}' — each section must have a unique id."
            )
        seen_ids[sid] = seen_ids.get(sid, 0) + 1

    # Required + conditional contradiction check
    for section in sections:
        if section.get("required") and section.get("condition"):
            errors.append(
                f"Section '{section['id']}' is required=true but also has "
                f"condition='{section['condition']}'. "
                f"Required sections cannot be conditional."
            )

    # Condition token resolution check
    known_conditions = set(parsed.get("conditions", {}).keys())
    for section in parsed.get("conditional_sections", []):
        cond = section.get("condition")
        if cond and cond not in known_conditions:
            errors.append(
                f"Section '{section['id']}' references condition '{cond}' "
                f"which is not declared in akr:conditions. "
                f"Known tokens: {sorted(known_conditions) or '(none)'}."
            )

    # Order format check (catches malformed values not already pushed to 9999.0)
    for section in sections:
        order_str = str(section.get("order", ""))
        if not _ORDER_PATTERN.match(order_str):
            errors.append(
                f"Section '{section['id']}' has non-standard order value '{order_str}'. "
                f"Expected format: integer with optional single lowercase letter "
                f"suffix (e.g., 8, 7a). Fractional letter suffixes beyond 'a'–'z' "
                f"are not supported."
            )

    # Duplicate order sort-key check
    seen_order_keys: Dict[float, str] = {}
    for section in sections:
        key = section.get("order_sort_key", 9999.0)
        if key == 9999.0:
            continue  # malformed or unset — already reported above
        if key in seen_order_keys:
            errors.append(
                f"Duplicate order value: section '{section['id']}' and "
                f"'{seen_order_keys[key]}' both resolve to sort key {key}. "
                f"Use distinct order values."
            )
        else:
            seen_order_keys[key] = section["id"]

    return errors


# ---------------------------------------------------------------------------
# Text output formatter (for human review / debugging)
# ---------------------------------------------------------------------------

def format_text_output(parsed: Dict[str, Any], validation_errors: List[str]) -> str:
    """Format the parsed contract as a human-readable text summary."""
    lines: List[str] = []

    template = parsed.get("template", {})
    template_id = template.get("id") or "(missing)"
    template_ver = template.get("version") or "?"
    charter = template.get("charter") or "(none)"
    project_types = ", ".join(template.get("project_types") or []) or "(none)"

    lines.append(f"Template:      {template_id} v{template_ver}")
    lines.append(f"Charter:       {charter}")
    lines.append(f"Project types: {project_types}")
    lines.append("")

    conditions = parsed.get("conditions", {})
    lines.append(f"Conditions ({len(conditions)}):")
    for token, desc in conditions.items():
        truncated = desc[:80] + "..." if len(desc) > 80 else desc
        lines.append(f"  {token}: {truncated}")
    lines.append("")

    sections = parsed.get("sections", [])
    lines.append(f"Sections ({len(sections)}) — sorted by order:")
    col_order = "Order"
    col_id = "ID"
    col_req = "Req"
    col_cond = "Condition"
    lines.append(f"  {col_order:<8}  {col_id:<30}  {col_req:<5}  {col_cond}")
    lines.append("  " + "-" * 68)
    for s in sections:
        req_flag = "yes" if s["required"] else "no"
        cond = s["condition"] or ""
        lines.append(f"  {s['order']:<8}  {s['id']:<30}  {req_flag:<5}  {cond}")
    lines.append("")

    required = parsed.get("required_sections", [])
    lines.append(f"Required sections ({len(required)}):")
    for sid in required:
        lines.append(f"  - {sid}")
    lines.append("")

    conditional = parsed.get("conditional_sections", [])
    lines.append(f"Conditional sections ({len(conditional)}):")
    for entry in conditional:
        lines.append(f"  - {entry['id']} (when: {entry['condition']})")
    lines.append("")

    if validation_errors:
        lines.append(f"Validation: FAILED ({len(validation_errors)} error(s))")
        for err in validation_errors:
            lines.append(f"  [ERROR] {err}")
    else:
        lines.append("Validation: OK — directive contract is internally consistent.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Compact output formatter (for CI quick-scan)
# ---------------------------------------------------------------------------

def _format_compact(parsed: Dict[str, Any]) -> str:
    """Return a compact JSON summary omitting typed section attributes."""
    template = parsed.get("template", {})
    compact = {
        "template_id": template.get("id", ""),
        "template_version": template.get("version", ""),
        "charter": template.get("charter", ""),
        "conditions": parsed.get("conditions", {}),
        "sections": [
            {
                "id": s["id"],
                "required": s["required"],
                "order": s["order"],
                "condition": s["condition"],
            }
            for s in parsed.get("sections", [])
        ],
        "required_sections": parsed.get("required_sections", []),
        "conditional_sections": parsed.get("conditional_sections", []),
    }
    return json.dumps(compact, indent=2)


# ---------------------------------------------------------------------------
# Batch validation (--all DIR)
# ---------------------------------------------------------------------------

def _validate_all(templates_dir: Path) -> int:
    """Parse and validate every .md file in templates_dir. Returns exit code."""
    templates = sorted(templates_dir.rglob("*.md"))
    if not templates:
        print(f"No .md files found in {templates_dir}", file=sys.stderr)
        return 2
    results = []
    for tmpl in templates:
        parsed = parse_template(tmpl)
        val_errors = validate_directives(parsed)
        parsed["validation_errors"] = val_errors
        results.append({
            "template": str(tmpl),
            "template_id": parsed.get("template", {}).get("id", "(unknown)"),
            "template_version": parsed.get("template", {}).get("version", "(unknown)"),
            "section_count": len(parsed.get("sections", [])),
            "required_count": len(parsed.get("required_sections", [])),
            "conditional_count": len(parsed.get("conditional_sections", [])),
            "parsing_errors": parsed.get("parsing_errors", []),
            "validation_errors": val_errors,
        })
    print(json.dumps({"templates_scanned": len(templates), "results": results}, indent=2))
    error_count = sum(len(r["parsing_errors"]) + len(r["validation_errors"]) for r in results)
    if error_count:
        print(f"\n\u274c {error_count} error(s) across {len(templates)} template(s).", file=sys.stderr)
        for r in results:
            all_errors = r["parsing_errors"] + r["validation_errors"]
            if all_errors:
                print(f"\n  {r['template']}:", file=sys.stderr)
                for e in all_errors:
                    print(f"    - {e}", file=sys.stderr)
        return 1
    print(f"\u2705 {len(templates)} template(s) validated. No directive errors.", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="parse_template_directives",
        description=(
            "AKR Template Directive Parser. "
            "Extracts akr: generation contract directives from a template file."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python parse_template_directives.py templates/lean_baseline_service_template_module.md\n"
            "  python parse_template_directives.py <template> --output text\n"
            "  python parse_template_directives.py <template> --validate\n"
            "  python parse_template_directives.py <template> --pretty\n"
            "  python parse_template_directives.py --all templates/\n"
            "  python parse_template_directives.py <template> --compact\n"
        ),
    )
    p.add_argument(
        "template",
        nargs="?",
        help="Path to the AKR template markdown file.  Required unless --all is used.",
    )
    p.add_argument(
        "--all",
        metavar="DIR",
        dest="all_dir",
        help=(
            "Batch mode: parse and validate every .md file in DIR. "
            "Prints a JSON summary. Exit 0 = all valid, 1 = errors found, 2 = no files."
        ),
    )
    p.add_argument(
        "--output",
        choices=["json", "text"],
        default="json",
        help="Output format. 'json' (default) for machine consumption; 'text' for debugging.",
    )
    p.add_argument(
        "--compact",
        action="store_true",
        help=(
            "Emit a compact JSON summary with only id/required/order/condition per section. "
            "Omits typed attributes. Ignored when --all is used."
        ),
    )
    p.add_argument(
        "--validate",
        action="store_true",
        help=(
            "Validate directive consistency only. "
            "No stdout output; errors go to stderr. "
            "Exit 0 = valid, exit 1 = errors found."
        ),
    )
    p.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output with 2-space indentation (default: compact).",
    )
    return p


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    # Batch mode: --all DIR
    if args.all_dir:
        all_dir = Path(args.all_dir)
        if not all_dir.is_dir():
            print(f"[ERROR] Not a directory: {all_dir}", file=sys.stderr)
            return 2
        return _validate_all(all_dir)

    if not args.template:
        parser.print_usage(sys.stderr)
        print("[ERROR] Provide a template file path or use --all DIR.", file=sys.stderr)
        return 2

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"[ERROR] Template file not found: {template_path}", file=sys.stderr)
        return 2

    try:
        parsed = parse_template(template_path)
    except OSError as exc:
        print(f"[ERROR] Could not read template file: {exc}", file=sys.stderr)
        return 1

    validation_errors = validate_directives(parsed)

    if args.validate:
        if validation_errors:
            for err in validation_errors:
                print(f"[ERROR] {err}", file=sys.stderr)
            return 1
        print("OK — directive contract is valid.", file=sys.stderr)
        return 0

    if args.compact:
        print(_format_compact(parsed))
    elif args.output == "text":
        print(format_text_output(parsed, validation_errors))
    else:
        indent = 2 if args.pretty else None
        print(json.dumps(parsed, indent=indent))

    # Emit validation errors to stderr even in non-validate mode so tooling
    # can detect them without suppressing the primary JSON output.
    if validation_errors:
        for err in validation_errors:
            print(f"[WARN] {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
