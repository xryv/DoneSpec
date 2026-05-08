from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def test_doctor_fails_without_done_json() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["doctor"])

        assert result.exit_code == 1
        assert "DoneSpec doctor" in result.output
        assert "done.json exists" in result.output
        assert "Project is missing required DoneSpec files" in result.output


def test_doctor_passes_required_checks_after_init() -> None:
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--yes"])
        assert init_result.exit_code == 0, init_result.output

        result = runner.invoke(app, ["doctor"])

        assert result.exit_code == 0, result.output
        assert "DoneSpec doctor" in result.output
        assert "Project has the required DoneSpec files" in result.output
        assert "done.json exists" in result.output
        assert "AGENTS.md exists" in result.output
        assert "CLAUDE.md exists" in result.output


def test_doctor_json_output_after_init() -> None:
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--yes"])
        assert init_result.exit_code == 0, init_result.output

        result = runner.invoke(app, ["doctor", "--json"])

        assert result.exit_code == 0, result.output

        payload = json.loads(result.output)
        assert payload["required_passed"] is True
        assert payload["root"]
        assert any(check["name"] == "done.json exists" for check in payload["checks"])


def test_doctor_detects_invalid_done_json() -> None:
    with runner.isolated_filesystem():
        Path("done.json").write_text("{invalid json", encoding="utf-8")

        result = runner.invoke(app, ["doctor"])

        assert result.exit_code == 1
        assert "done.json is valid JSON" in result.output
        assert "Project is missing required DoneSpec files" in result.output
