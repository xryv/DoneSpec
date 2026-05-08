from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def _write_done_json(payload: dict[str, object]) -> None:
    Path("done.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_validate_strict_passes_valid_contract() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
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

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 0, result.output
        assert "Validation passed" in result.output


def test_validate_strict_rejects_empty_contract() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
                "must_pass": [],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "Strict validation failed" in result.output
        assert "at least one check" in result.output


def test_validate_strict_requires_check_names() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "path": "done.json",
                    }
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "must define a non-empty name" in result.output


def test_validate_strict_rejects_duplicate_check_names() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
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

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "duplicate check name" in result.output


def test_validate_strict_rejects_duplicate_check_ids() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
                "must_pass": [
                    {
                        "id": "same-id",
                        "type": "file_exists",
                        "name": "first",
                        "path": "done.json",
                    },
                    {
                        "id": "same-id",
                        "type": "file_exists",
                        "name": "second",
                        "path": "done.json",
                    },
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "duplicate check id" in result.output


def test_validate_strict_rejects_invalid_regex() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
                "must_pass": [
                    {
                        "type": "regex_in_file",
                        "name": "invalid regex",
                        "path": "done.json",
                        "pattern": "[",
                    }
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "regex pattern is invalid" in result.output


def test_validate_strict_rejects_absolute_paths() -> None:
    with runner.isolated_filesystem():
        absolute_path = str(Path.cwd() / "done.json")

        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "name": "absolute path",
                        "path": absolute_path,
                    }
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "path must be relative" in result.output


def test_validate_strict_rejects_parent_traversal_paths() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "strict-test",
                "must_pass": [
                    {
                        "type": "file_exists",
                        "name": "parent traversal",
                        "path": "../done.json",
                    }
                ],
                "must_not": [],
            }
        )

        result = runner.invoke(app, ["validate", "done.json", "--strict"])

        assert result.exit_code == 2
        assert "path must not contain '..'" in result.output


def test_validate_without_strict_allows_duplicate_names() -> None:
    with runner.isolated_filesystem():
        _write_done_json(
            {
                "version": "1.0",
                "task_id": "non-strict-test",
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

        result = runner.invoke(app, ["validate", "done.json"])

        assert result.exit_code == 0, result.output
