from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from donespec import __version__


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    passed: bool
    details: str | None = None
    required: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "passed": self.passed,
            "details": self.details,
            "required": self.required,
        }


@dataclass(frozen=True)
class DoctorReport:
    root: str
    checks: list[DoctorCheck]

    @property
    def required_passed(self) -> bool:
        return all(check.passed for check in self.checks if check.required)

    @property
    def all_passed(self) -> bool:
        return all(check.passed for check in self.checks)

    def to_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "required_passed": self.required_passed,
            "all_passed": self.all_passed,
            "checks": [check.to_dict() for check in self.checks],
        }


def run_doctor(root: Path) -> DoctorReport:
    root = root.resolve()
    checks: list[DoctorCheck] = []

    checks.append(
        DoctorCheck(
            name="DoneSpec installed",
            passed=True,
            details=f"version {__version__}",
            required=True,
        )
    )

    done_json = root / "done.json"
    checks.append(
        DoctorCheck(
            name="done.json exists",
            passed=done_json.exists(),
            details=str(done_json) if done_json.exists() else "missing",
            required=True,
        )
    )

    checks.append(_json_check(done_json))

    checks.extend(
        [
            _file_check(root, "AGENTS.md", "AGENTS.md exists"),
            _file_check(root, "CLAUDE.md", "CLAUDE.md exists"),
            _file_check(root, ".vscode/tasks.json", "VS Code tasks exist"),
            _file_check(root, ".githooks/pre-push", "Git pre-push hook exists"),
            _file_check(
                root,
                "scripts/install-git-hooks.ps1",
                "Windows Git hooks installer exists",
            ),
            _file_check(
                root,
                "scripts/install-git-hooks.sh",
                "Unix Git hooks installer exists",
            ),
            _file_check(
                root,
                ".github/workflows/ci.yml",
                "GitHub Actions workflow exists",
            ),
            _regex_check(
                root,
                ".github/workflows/ci.yml",
                "CI runs DoneSpec self-validation",
                "donespec validate done.json",
            ),
        ]
    )

    git_root = _git_root(root)
    checks.append(
        DoctorCheck(
            name="Git repository detected",
            passed=git_root is not None,
            details=git_root or "not a Git repository",
            required=False,
        )
    )

    hooks_path = _git_config(root, "core.hooksPath")
    checks.append(
        DoctorCheck(
            name="Git hooks path configured",
            passed=hooks_path == ".githooks",
            details=hooks_path or "not configured",
            required=False,
        )
    )

    return DoctorReport(root=str(root), checks=checks)


def _file_check(root: Path, relative_path: str, name: str) -> DoctorCheck:
    path = root / relative_path
    return DoctorCheck(
        name=name,
        passed=path.exists(),
        details=relative_path if path.exists() else "missing",
        required=False,
    )


def _json_check(path: Path) -> DoctorCheck:
    if not path.exists():
        return DoctorCheck(
            name="done.json is valid JSON",
            passed=False,
            details="done.json not found",
            required=True,
        )

    try:
        json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return DoctorCheck(
            name="done.json is valid JSON",
            passed=False,
            details=str(exc),
            required=True,
        )

    return DoctorCheck(
        name="done.json is valid JSON",
        passed=True,
        details="valid",
        required=True,
    )


def _regex_check(
    root: Path,
    relative_path: str,
    name: str,
    pattern: str,
) -> DoctorCheck:
    path = root / relative_path

    if not path.exists():
        return DoctorCheck(
            name=name,
            passed=False,
            details=f"{relative_path} missing",
            required=False,
        )

    content = path.read_text(encoding="utf-8-sig")

    return DoctorCheck(
        name=name,
        passed=pattern in content,
        details=f"{relative_path} contains {pattern!r}"
        if pattern in content
        else f"{relative_path} does not contain {pattern!r}",
        required=False,
    )


def _git_root(root: Path) -> str | None:
    result = _run_git(root, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    return value or None


def _git_config(root: Path, key: str) -> str | None:
    result = _run_git(root, "config", key)
    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    return value or None


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return subprocess.CompletedProcess(
            args=["git", *args],
            returncode=1,
            stdout="",
            stderr="git unavailable",
        )
