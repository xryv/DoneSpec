from __future__ import annotations

import pytest

from donespec.exceptions import SpecValidationError
from donespec.schema import validate_spec_payload


def test_schema_accepts_minimal_command_spec():
    validate_spec_payload(
        {
            "version": "1.0",
            "task_id": "fix-auth-bug",
            "must_pass": [{"type": "command", "run": "pytest"}],
        }
    )


def test_schema_rejects_unknown_checker():
    with pytest.raises(SpecValidationError):
        validate_spec_payload(
            {
                "version": "1.0",
                "task_id": "bad",
                "must_pass": [{"type": "llm_judge", "prompt": "is this done?"}],
            }
        )
