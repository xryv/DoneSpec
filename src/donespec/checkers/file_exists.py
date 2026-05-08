from __future__ import annotations

from time import perf_counter

from donespec.checkers.base import Checker, timed
from donespec.pathing import resolve_under_root


class FileExistsChecker(Checker):
    type_name = "file_exists"

    def default_name(self) -> str:
        return f"{self.config['path']} exists"

    @timed
    def run(self, started: float):
        raw_path = self.config["path"]
        target = resolve_under_root(self.context.root_dir, raw_path)
        exists = target.exists()
        duration_ms = (perf_counter() - started) * 1000

        return self.result(
            passed=exists,
            duration_ms=duration_ms,
            error=None if exists else f"File does not exist: {raw_path}",
            details=f"resolved_path={target}",
            metadata={"path": raw_path, "resolved_path": str(target), "is_file": target.is_file()},
        )
