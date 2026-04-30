from __future__ import annotations

from pathlib import Path

import pytest

from harness.write_guard import HarnessValidationError, guarded_write


VALID_DOCUMENT = """---
businessCapability: Training
feature: Course Management
layer: API
project_type: api-backend
status: approved
compliance_mode: pilot
---
<!-- akr-generated
template: reyesmelvinr-emr/core-akr-templates@master/.akr/templates/lean_baseline_service_template_module.md
charter: reyesmelvinr-emr/core-akr-templates@master/copilot-instructions/backend-service.instructions.md
steps-completed: 1, 2, 3, 4, 5, 6, 7
pass-timings-seconds: pass1=12,pass2=9
total-generation-seconds: 21
-->

## Quick Reference
Content.

## Module Files
Content.

## API Operations
Content.

## Integration Context
Content.

## Business Rules
Content.

## Data Operations
Content.

## Questions & Gaps
None.
"""


def test_guarded_write_writes_valid_content(tmp_path: Path) -> None:
    output_path = tmp_path / "docs" / "modules" / "CourseDomain_doc.md"
    result = guarded_write(output_path, VALID_DOCUMENT, compliance_mode="pilot")

    assert result.validation_passed
    assert output_path.exists()
    assert result.estimated_tokens_written > 0


def test_guarded_write_blocks_invalid_content(tmp_path: Path) -> None:
    output_path = tmp_path / "docs" / "modules" / "Broken_doc.md"

    with pytest.raises(HarnessValidationError):
        guarded_write(output_path, "# missing front matter", compliance_mode="pilot")
