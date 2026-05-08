from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from donespec.exceptions import SpecValidationError
from donespec.schema import validate_spec_payload


def load_spec(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SpecValidationError(f"Spec file not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SpecValidationError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise SpecValidationError("Invalid done.json: root value must be an object")

    validate_spec_payload(payload)
    payload.setdefault("must_pass", [])
    payload.setdefault("must_not", [])
    return payload
