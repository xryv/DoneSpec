from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class AgentMode(StrEnum):
    all = "all"
    codex = "codex"
    claude = "claude"
    none = "none"


@dataclass
class InitResult:
    created: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    overwritten: list[str] = field(default_factory=list)


def initialize_project(
    root: Path,
    *,
    agent: AgentMode = AgentMode.all,
    with_vscode: bool = True,
    with_hooks: bool = True,
    force: bool = False,
) -> InitResult:
    root = root.resolve()
    result = InitResult()

    files = _build_files(
        agent=agent,
        with_vscode=with_vscode,
        with_hooks=with_hooks,
    )

    for relative_path, content in files.items():
        _write_file(
            root / relative_path,
            relative_path=relative_path,
            content=content,
            force=force,
            result=result,
        )

    for relative_path in _executable_paths(agent=agent, with_hooks=with_hooks):
        path = root / relative_path
        if path.exists():
            path.chmod(path.stat().st_mode | 0o111)

    return result


def _write_file(
    path: Path,
    *,
    relative_path: str,
    content: str,
    force: bool,
    result: InitResult,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not force:
        result.skipped.append(relative_path)
        return

    existed = path.exists()
    path.write_text(content, encoding="utf-8", newline="\n")

    if existed:
        result.overwritten.append(relative_path)
    else:
        result.created.append(relative_path)


def _build_files(
    *,
    agent: AgentMode,
    with_vscode: bool,
    with_hooks: bool,
) -> dict[str, str]:
    files: dict[str, str] = {
        "done.json": _done_json(
            agent=agent,
            with_vscode=with_vscode,
            with_hooks=with_hooks,
        )
    }

    if agent in {AgentMode.all, AgentMode.codex, AgentMode.claude}:
        files["AGENTS.md"] = _agents_md()

    if agent in {AgentMode.all, AgentMode.claude}:
        files["CLAUDE.md"] = _claude_md()

    if with_vscode:
        files[".vscode/tasks.json"] = _vscode_tasks_json()

    if with_hooks:
        files[".githooks/pre-push"] = _pre_push_hook()
        files["scripts/install-git-hooks.ps1"] = _install_hooks_ps1()
        files["scripts/install-git-hooks.sh"] = _install_hooks_sh()

    return files


def _executable_paths(*, agent: AgentMode, with_hooks: bool) -> list[str]:
    _ = agent
    if not with_hooks:
        return []

    return [
        ".githooks/pre-push",
        "scripts/install-git-hooks.sh",
    ]


def _done_json(
    *,
    agent: AgentMode,
    with_vscode: bool,
    with_hooks: bool,
) -> str:
    must_pass: list[dict[str, object]] = [
        {
            "type": "file_exists",
            "name": "DoneSpec file exists",
            "path": "done.json",
        }
    ]

    if agent in {AgentMode.all, AgentMode.codex, AgentMode.claude}:
        must_pass.extend(
            [
                {
                    "type": "file_exists",
                    "name": "Agent instructions exist",
                    "path": "AGENTS.md",
                },
                {
                    "type": "regex_in_file",
                    "name": "Agent instructions require DoneSpec validation",
                    "path": "AGENTS.md",
                    "pattern": "donespec validate done\\.json",
                },
            ]
        )

    if agent in {AgentMode.all, AgentMode.claude}:
        must_pass.extend(
            [
                {
                    "type": "file_exists",
                    "name": "Claude Code instructions exist",
                    "path": "CLAUDE.md",
                },
                {
                    "type": "regex_in_file",
                    "name": "Claude imports shared agent protocol",
                    "path": "CLAUDE.md",
                    "pattern": "@AGENTS\\.md",
                },
            ]
        )

    if with_vscode:
        must_pass.extend(
            [
                {
                    "type": "file_exists",
                    "name": "VS Code tasks exist",
                    "path": ".vscode/tasks.json",
                },
                {
                    "type": "regex_in_file",
                    "name": "VS Code task runs DoneSpec validation",
                    "path": ".vscode/tasks.json",
                    "pattern": "donespec validate done\\.json",
                },
            ]
        )

    if with_hooks:
        must_pass.extend(
            [
                {
                    "type": "file_exists",
                    "name": "Git pre-push hook exists",
                    "path": ".githooks/pre-push",
                },
                {
                    "type": "regex_in_file",
                    "name": "Git pre-push hook runs DoneSpec",
                    "path": ".githooks/pre-push",
                    "pattern": "donespec validate done\\.json",
                },
                {
                    "type": "file_exists",
                    "name": "Git hooks installer exists",
                    "path": "scripts/install-git-hooks.ps1",
                },
                {
                    "type": "file_exists",
                    "name": "Unix Git hooks installer exists",
                    "path": "scripts/install-git-hooks.sh",
                },
            ]
        )

    payload = {
        "version": "1.0",
        "task_id": "initial-validation",
        "must_pass": must_pass,
        "must_not": [],
    }

    return json.dumps(payload, indent=2) + "\n"


def _agents_md() -> str:
    return """# AGENTS.md

## Purpose

This repository uses DoneSpec as the deterministic completion gate for AI coding agent work.

Done means deterministically verified.

## Completion rule

Before declaring any task complete, run:

donespec validate done.json

If validation fails, the task is not complete.

The agent should:

1. Read the failing DoneSpec output.
2. Identify which check failed.
3. Fix the underlying issue.
4. Run DoneSpec again.
5. Repeat until validation passes.

## Rules

Do not weaken done.json checks to make a task pass unless the human explicitly asks to change the validation contract.

Do not claim completion until DoneSpec passes.
"""


def _claude_md() -> str:
    return """@AGENTS.md

## Claude Code specific notes

This repository uses DoneSpec as the completion gate.

Before reporting a task as complete, run:

donespec validate done.json

If validation fails, continue fixing the task until DoneSpec passes.
"""


def _vscode_tasks_json() -> str:
    return """{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "DoneSpec: Validate",
      "type": "shell",
      "command": "donespec validate done.json",
      "options": {
        "env": {
          "PATH": "${workspaceFolder}\\\\.venv\\\\Scripts;${workspaceFolder}/.venv/bin;${env:PATH}",
          "Path": "${workspaceFolder}\\\\.venv\\\\Scripts;${env:Path}",
          "VIRTUAL_ENV": "${workspaceFolder}\\\\.venv"
        }
      },
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated",
        "clear": true
      }
    },
    {
      "label": "DoneSpec: Validate JSON",
      "type": "shell",
      "command": "donespec validate done.json --json",
      "options": {
        "env": {
          "PATH": "${workspaceFolder}\\\\.venv\\\\Scripts;${workspaceFolder}/.venv/bin;${env:PATH}",
          "Path": "${workspaceFolder}\\\\.venv\\\\Scripts;${env:Path}",
          "VIRTUAL_ENV": "${workspaceFolder}\\\\.venv"
        }
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated",
        "clear": true
      }
    }
  ]
}
"""


def _pre_push_hook() -> str:
    return """#!/usr/bin/env sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [ -x ".venv/Scripts/python.exe" ]; then
  export PATH="$ROOT/.venv/Scripts:$PATH"
  PYTHON=".venv/Scripts/python.exe"
elif [ -x ".venv/bin/python" ]; then
  export PATH="$ROOT/.venv/bin:$PATH"
  PYTHON=".venv/bin/python"
else
  PYTHON="python"
fi

echo "[DoneSpec] Running pre-push validation..."
"$PYTHON" -m donespec validate done.json

echo "[DoneSpec] Pre-push validation passed."
"""


def _install_hooks_ps1() -> str:
    return """$ErrorActionPreference = "Stop"

git config core.hooksPath .githooks

Write-Host ""
Write-Host "DoneSpec Git hooks installed."
Write-Host ""
Write-Host "Active hooks path:"
git config core.hooksPath
Write-Host ""
Write-Host "Pre-push will run:"
Write-Host "  donespec validate done.json"
Write-Host ""
"""


def _install_hooks_sh() -> str:
    return """#!/usr/bin/env sh
set -eu

git config core.hooksPath .githooks

echo ""
echo "DoneSpec Git hooks installed."
echo ""
echo "Active hooks path:"
git config core.hooksPath
echo ""
echo "Pre-push will run:"
echo "  donespec validate done.json"
echo ""
"""
