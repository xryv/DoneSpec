from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def _write_done_json(payload: dict[str, object]) -> None:
    Path("done.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _base_payload() -> dict[str, object]:
    return {
        "version": "1.0",
        "task_id": "author-test",
        "must_pass": [],
        "must_not": [],
    }


def test_add_check_adds_file_exists_check() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "file_exists",
                "--name",
                "README exists",
                "--path",
                "README.md",
            ],
        )

        assert result.exit_code == 0, result.output
        assert "DoneSpec check added" in result.output

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))

        assert payload["must_pass"][0] == {
            "type": "file_exists",
            "name": "README exists",
            "path": "README.md",
        }


def test_add_check_adds_command_check() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "command",
                "--name",
                "tests pass",
                "--run",
                "pytest -q",
                "--expected-exit-code",
                "0",
                "--timeout-seconds",
                "60",
            ],
        )

        assert result.exit_code == 0, result.output

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))
        check = payload["must_pass"][0]

        assert check["type"] == "command"
        assert check["name"] == "tests pass"
        assert check["run"] == "pytest -q"
        assert check["expected_exit_code"] == 0
        assert check["timeout_seconds"] == 60


def test_add_check_adds_regex_check_with_flags() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "regex_in_file",
                "--name",
                "README has title",
                "--path",
                "README.md",
                "--pattern",
                "^#",
                "--flag",
                "MULTILINE",
            ],
        )

        assert result.exit_code == 0, result.output

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))
        check = payload["must_pass"][0]

        assert check["type"] == "regex_in_file"
        assert check["flags"] == ["MULTILINE"]


def test_add_check_adds_http_check() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "http_check",
                "--name",
                "health endpoint responds",
                "--url",
                "http://127.0.0.1:8000/health",
                "--method",
                "GET",
                "--expected-status",
                "200",
                "--headers-json",
                '{"Accept": "application/json"}',
            ],
        )

        assert result.exit_code == 0, result.output

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))
        check = payload["must_pass"][0]

        assert check["type"] == "http_check"
        assert check["headers"] == {"Accept": "application/json"}


def test_add_check_can_target_must_not() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--group",
                "must_not",
                "--type",
                "regex_absent",
                "--name",
                "No secrets",
                "--path",
                "README.md",
                "--pattern",
                "SECRET_KEY",
            ],
        )

        assert result.exit_code == 0, result.output

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))

        assert payload["must_pass"] == []
        assert payload["must_not"][0]["name"] == "No secrets"


def test_add_check_rejects_duplicate_name() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "author-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "name": "README exists",
                        "path": "README.md",
                    }
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "file_exists",
                "--name",
                "README exists",
                "--path",
                "docs/index.md",
            ],
        )

        assert result.exit_code == 2
        assert "duplicate check name" in result.output


def test_add_check_rejects_missing_required_field() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "file_exists",
                "--name",
                "README exists",
            ],
        )

        assert result.exit_code == 2
        assert "checks require --path" in result.output


def test_add_check_rejects_invalid_regex_via_strict_validation() -> None:
    with runner.isolated_filesystem():
        _write_done_json(_base_payload())

        result = runner.invoke(
            app,
            [
                "add-check",
                "done.json",
                "--type",
                "regex_in_file",
                "--name",
                "Invalid regex",
                "--path",
                "README.md",
                "--pattern",
                "[",
            ],
        )

        assert result.exit_code == 2
        assert "regex pattern is invalid" in result.output
