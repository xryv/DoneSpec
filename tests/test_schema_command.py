from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app
from donespec.schema import validate_spec_payload
from donespec.strict import validate_strict_payload

runner = CliRunner()
REPO_ROOT = Path(__file__).resolve().parents[1]


def test_schema_command_prints_valid_json_schema() -> None:
    result = runner.invoke(app, ["schema"])

    assert result.exit_code == 0, result.output

    payload = json.loads(result.output)

    assert payload["type"] == "object"
    assert "properties" in payload
    assert "version" in payload["properties"]
    assert "must_pass" in payload["properties"]


def test_schema_command_writes_schema_file() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["schema", "--write", "done.schema.json"])

        assert result.exit_code == 0, result.output
        assert Path("done.schema.json").exists()

        payload = json.loads(Path("done.schema.json").read_text(encoding="utf-8"))

        assert payload["type"] == "object"
        assert "properties" in payload


def test_schema_command_does_not_overwrite_without_force() -> None:
    with runner.isolated_filesystem():
        Path("done.schema.json").write_text('{"custom": true}\n', encoding="utf-8")

        result = runner.invoke(app, ["schema", "--write", "done.schema.json"])

        assert result.exit_code == 1
        assert "Schema file already exists" in result.output
        assert Path("done.schema.json").read_text(encoding="utf-8") == '{"custom": true}\n'


def test_schema_command_overwrites_with_force() -> None:
    with runner.isolated_filesystem():
        Path("done.schema.json").write_text('{"custom": true}\n', encoding="utf-8")

        result = runner.invoke(app, ["schema", "--write", "done.schema.json", "--force"])

        assert result.exit_code == 0, result.output

        payload = json.loads(Path("done.schema.json").read_text(encoding="utf-8"))

        assert payload["type"] == "object"
        assert "properties" in payload


def test_template_examples_validate_against_schema_and_strict_mode() -> None:
    template_specs = sorted((REPO_ROOT / "examples" / "templates").glob("*/done.json"))

    assert template_specs

    for spec_path in template_specs:
        payload = json.loads(spec_path.read_text(encoding="utf-8"))

        validate_spec_payload(payload)
        validate_strict_payload(payload)
