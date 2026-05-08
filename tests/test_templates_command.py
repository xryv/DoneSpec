from __future__ import annotations

import json

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def test_templates_command_lists_available_templates() -> None:
    result = runner.invoke(app, ["templates"])

    assert result.exit_code == 0, result.output
    assert "Available DoneSpec templates" in result.output
    assert "generic" in result.output
    assert "python" in result.output
    assert "node" in result.output
    assert "docs" in result.output
    assert "api" in result.output


def test_templates_command_supports_json_output() -> None:
    result = runner.invoke(app, ["templates", "--json"])

    assert result.exit_code == 0, result.output

    payload = json.loads(result.output)
    names = {item["name"] for item in payload["templates"]}

    assert names == {"generic", "python", "node", "docs", "api"}
