from __future__ import annotations

import subprocess
from time import perf_counter

from donespec.checkers.base import Checker, timed


class CommandChecker(Checker):
    type_name = "command"

    def default_name(self) -> str:
        return self.config.get("run", "command")

    @timed
    def run(self, started: float):
        command = self.config["run"]
        expected_exit_code = int(self.config.get("expected_exit_code", 0))
        timeout_seconds = float(self.config.get("timeout_seconds", 120))

        try:
            completed = subprocess.run(
                command,
                cwd=self.context.root_dir,
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            duration_ms = (perf_counter() - started) * 1000
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error=f"Command timed out after {timeout_seconds:g}s",
                metadata={
                    "command": command,
                    "timeout_seconds": timeout_seconds,
                    "stdout": exc.stdout,
                    "stderr": exc.stderr,
                },
            )

        duration_ms = (perf_counter() - started) * 1000
        passed = completed.returncode == expected_exit_code
        details = f"exit_code={completed.returncode}, expected_exit_code={expected_exit_code}"
        return self.result(
            passed=passed,
            duration_ms=duration_ms,
            error=None if passed else details,
            details=details,
            metadata={
                "command": command,
                "exit_code": completed.returncode,
                "expected_exit_code": expected_exit_code,
                "stdout_tail": completed.stdout[-4000:],
                "stderr_tail": completed.stderr[-4000:],
            },
        )
