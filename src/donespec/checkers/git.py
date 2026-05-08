from __future__ import annotations

import subprocess
from time import perf_counter

from donespec.checkers.base import Checker, timed


class FileNotModifiedChecker(Checker):
    type_name = "file_not_modified"

    def default_name(self) -> str:
        return f"{self.config['path']} not modified"

    @timed
    def run(self, started: float):
        raw_path = self.config["path"]

        repo_check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=self.context.root_dir,
            text=True,
            capture_output=True,
            check=False,
        )
        if repo_check.returncode != 0:
            duration_ms = (perf_counter() - started) * 1000
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error="file_not_modified requires a Git work tree",
                metadata={"path": raw_path, "stderr": repo_check.stderr.strip()},
            )

        status = subprocess.run(
            ["git", "status", "--porcelain", "--", raw_path],
            cwd=self.context.root_dir,
            text=True,
            capture_output=True,
            check=False,
        )
        duration_ms = (perf_counter() - started) * 1000

        if status.returncode != 0:
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error=status.stderr.strip() or "git status failed",
                metadata={"path": raw_path, "exit_code": status.returncode},
            )

        porcelain = status.stdout.strip()
        passed = porcelain == ""

        return self.result(
            passed=passed,
            duration_ms=duration_ms,
            error=None if passed else f"Forbidden path modified: {raw_path}",
            details="clean" if passed else porcelain,
            metadata={"path": raw_path, "git_status": porcelain},
        )
