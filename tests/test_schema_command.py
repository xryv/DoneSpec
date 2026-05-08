from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


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
