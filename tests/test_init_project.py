from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from donespec.cli import app

runner = CliRunner()


def test_init_creates_default_agent_ready_files() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--yes"])

        assert result.exit_code == 0, result.output
        assert Path("done.json").exists()
        assert Path("AGENTS.md").exists()
        assert Path("CLAUDE.md").exists()
        assert Path(".vscode/tasks.json").exists()
        assert Path(".githooks/pre-push").exists()
        assert Path("scripts/install-git-hooks.ps1").exists()
        assert Path("scripts/install-git-hooks.sh").exists()

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))
        names = {check["name"] for check in payload["must_pass"]}

        assert payload["version"] == "1.0"
        assert "Agent instructions require DoneSpec validation" in names
        assert "VS Code task runs DoneSpec validation" in names
        assert "Git pre-push hook runs DoneSpec" in names


def test_init_does_not_overwrite_existing_files_without_force() -> None:
    with runner.isolated_filesystem():
        Path("done.json").write_text('{"custom": true}\n', encoding="utf-8")

        result = runner.invoke(app, ["init", "--yes"])

        assert result.exit_code == 0, result.output
        assert Path("done.json").read_text(encoding="utf-8") == '{"custom": true}\n'
        assert "Skipped existing files" in result.output


def test_init_force_overwrites_existing_files() -> None:
    with runner.isolated_filesystem():
        Path("done.json").write_text('{"custom": true}\n', encoding="utf-8")

        result = runner.invoke(app, ["init", "--yes", "--force"])

        assert result.exit_code == 0, result.output

        payload = json.loads(Path("done.json").read_text(encoding="utf-8"))
        assert payload["task_id"] == "initial-validation"
        assert "Overwritten" in result.output


def test_init_codex_mode_does_not_create_claude_file() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--yes", "--agent", "codex"])

        assert result.exit_code == 0, result.output
        assert Path("AGENTS.md").exists()
        assert not Path("CLAUDE.md").exists()


def test_init_without_vscode_or_hooks() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--yes", "--no-vscode", "--no-hooks"])

        assert result.exit_code == 0, result.output
        assert Path("done.json").exists()
        assert Path("AGENTS.md").exists()
        assert not Path(".vscode/tasks.json").exists()
        assert not Path(".githooks/pre-push").exists()
        assert not Path("scripts/install-git-hooks.ps1").exists()
