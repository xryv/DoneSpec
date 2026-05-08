from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


@pytest.fixture
def spec_payload() -> dict[str, Any]:
    return {
        "version": "1.0",
        "task_id": "test-task",
        "must_pass": [],
        "must_not": [],
    }
