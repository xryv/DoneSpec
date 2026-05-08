from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def test_root_help_includes_stable_command_descriptions() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0, result.output
    assert "Deterministic completion validation for local development and CI." in result.output
    assert "Validate a DoneSpec task file." in result.output
    assert "Initialize DoneSpec files in a project." in result.output
    assert "Explain a DoneSpec task file without executing checks." in result.output
    assert "Safely add a check to a DoneSpec contract." in result.output
    assert "Print or write the DoneSpec JSON Schema." in result.output
    assert "List available DoneSpec init templates." in result.output
    assert "Inspect whether a project is DoneSpec-ready." in result.output


def test_validate_json_output(tmp_path: Path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "auth.ts").write_text("returnTo\n", encoding="utf-8")
    spec = tmp_path / "done.json"
    spec.write_text(
        json.dumps(
            {
                "version": "1.0",
                "task_id": "cli-json",
                "must_pass": [
                    {"type": "file_exists", "path": "src/auth.ts"},
                    {"type": "regex_in_file", "path": "src/auth.ts", "pattern": "returnTo"},
                ],
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(spec), "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["passed"] is True
    assert payload["total_checks"] == 2


def test_validate_invalid_spec_exits_2(tmp_path: Path):
    spec = tmp_path / "done.json"
    spec.write_text('{"version":"1.0"}', encoding="utf-8")

    result = runner.invoke(app, ["validate", str(spec), "--json"])

    assert result.exit_code == 2
    assert json.loads(result.stdout)["passed"] is False
