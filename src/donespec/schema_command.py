from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path

SCHEMA_RESOURCE = "schemas/done.schema.json"


def get_schema_text() -> str:
    """Return the packaged DoneSpec JSON Schema as formatted JSON text."""
    schema_path = files("donespec").joinpath(SCHEMA_RESOURCE)
    text = schema_path.read_text(encoding="utf-8")

    # Validate that the packaged schema is valid JSON before returning it.
    payload = json.loads(text)

    return json.dumps(payload, indent=2) + "\n"


def write_schema_file(path: Path, *, force: bool = False) -> Path:
    """Write the packaged DoneSpec JSON Schema to a target path."""
    target = path.resolve()

    if target.exists() and not force:
        raise FileExistsError(str(target))

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(get_schema_text(), encoding="utf-8")

    return target
