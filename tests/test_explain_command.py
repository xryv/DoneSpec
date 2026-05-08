from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def _write_done_json(payload: dict[str, object]) -> None:
    Path("done.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_explain_command_prints_human_summary() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "explain-test",
                "description": "Example contract for explanation.",
                "must_pass": [
                    {
                        "type": "command",
                        "name": "tests pass",
                        "run": "pytest -q",
                    },
                    {
                        "type": "file_exists",
                        "name": "README exists",
                        "path": "README.md",
                    },
                ],
                "must_not": [
                    {
                        "type": "regex_absent",
                        "name": "README has no TODO markers",
                        "path": "README.md",
                        "pattern": "TODO",
                    }
                ],
            }
        )

        result = runner.invoke(app, ["explain", "done.json"])

        assert result.exit_code == 0, result.output
        assert "DoneSpec explanation: explain-test" in result.output
        assert "Total checks: 3" in result.output
        assert "must_pass: 2" in result.output
        assert "must_not: 1" in result.output
        assert "[command] tests pass" in result.output
        assert "donespec validate done.json --strict" in result.output


def test_explain_command_supports_json_output() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "explain-json-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "name": "DoneSpec file exists",
                        "path": "done.json",
                    }
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["explain", "done.json", "--json"])

        assert result.exit_code == 0, result.output

        payload = json.loads(result.output)

        assert payload["task_id"] == "explain-json-test"
        assert payload["total_checks"] == 1
        assert payload["groups"]["must_pass"] == 1
        assert payload["groups"]["must_not"] == 0
        assert payload["types"]["file_exists"] == 1
        assert payload["checks"][0]["name"] == "DoneSpec file exists"
        assert payload["recommended_gate"] == "donespec validate done.json --strict"


def test_explain_command_supports_strict_mode() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "explain-strict-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "name": "duplicate",
                        "path": "done.json",
                    },
                    {
                        "type": "file_exists",
                        "name": "duplicate",
                        "path": "done.json",
                    },
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["explain", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "Strict validation failed" in result.output
        assert "duplicate check name" in result.output


def test_explain_command_json_error_output() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "explain-strict-json-error-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "name": "duplicate",
                        "path": "done.json",
                    },
                    {
                        "type": "file_exists",
                        "name": "duplicate",
                        "path": "done.json",
                    },
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["explain", "done.json", "--strict", "--json"])

        assert result.exit_code == 2

        payload = json.loads(result.output)

        assert payload["error"]
        assert "Strict validation failed" in payload["error"]
