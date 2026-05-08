from __future__ import annotations

import json
from importlib import resources
from typing import Any

from jsonschema import Draft202012Validator

from donespec.exceptions import SpecValidationError


def load_schema() -> dict[str, Any]:
    schema_ref = resources.files("donespec.schemas").joinpath("done.schema.json")
    return json.loads(schema_ref.read_text(encoding="utf-8"))


def validate_spec_payload(payload: dict[str, Any]) -> None:
    validator = Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if not errors:
        return

    formatted: list[str] = []
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        formatted.append(f"{path}: {error.message}")

    raise SpecValidationError("Invalid done.json:\n" + "\n".join(f"- {line}" for line in formatted))
