from __future__ import annotations

import re
from time import perf_counter

from donespec.checkers.base import Checker, timed
from donespec.pathing import resolve_under_root

_FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE,
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
}


def compile_flags(raw_flags: list[str] | None) -> re.RegexFlag:
    flags = re.NOFLAG
    for raw_flag in raw_flags or []:
        flags |= _FLAG_MAP[raw_flag]
    return flags


class RegexInFileChecker(Checker):
    type_name = "regex_in_file"

    def default_name(self) -> str:
        return f"{self.config['pattern']} exists in {self.config['path']}"

    @timed
    def run(self, started: float):
        raw_path = self.config["path"]
        pattern = self.config["pattern"]
        target = resolve_under_root(self.context.root_dir, raw_path)

        if not target.exists():
            duration_ms = (perf_counter() - started) * 1000
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error=f"File does not exist: {raw_path}",
                metadata={"path": raw_path, "pattern": pattern},
            )

        content = target.read_text(encoding="utf-8", errors="replace")
        match = re.search(pattern, content, flags=compile_flags(self.config.get("flags")))
        duration_ms = (perf_counter() - started) * 1000

        return self.result(
            passed=match is not None,
            duration_ms=duration_ms,
            error=None if match else f"Pattern not found: {pattern}",
            details=f"file={raw_path}",
            metadata={
                "path": raw_path,
                "pattern": pattern,
                "match_start": match.start() if match else None,
                "match_end": match.end() if match else None,
            },
        )


class RegexAbsentChecker(Checker):
    type_name = "regex_absent"

    def default_name(self) -> str:
        return f"{self.config['pattern']} absent from {self.config['path']}"

    @timed
    def run(self, started: float):
        raw_path = self.config["path"]
        pattern = self.config["pattern"]
        target = resolve_under_root(self.context.root_dir, raw_path)

        if not target.exists():
            duration_ms = (perf_counter() - started) * 1000
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error=f"File does not exist: {raw_path}",
                metadata={"path": raw_path, "pattern": pattern},
            )

        content = target.read_text(encoding="utf-8", errors="replace")
        match = re.search(pattern, content, flags=compile_flags(self.config.get("flags")))
        duration_ms = (perf_counter() - started) * 1000
        passed = match is None

        return self.result(
            passed=passed,
            duration_ms=duration_ms,
            error=None if passed else f"Forbidden pattern found: {pattern}",
            details=f"file={raw_path}",
            metadata={
                "path": raw_path,
                "pattern": pattern,
                "match_start": match.start() if match else None,
                "match_end": match.end() if match else None,
            },
        )
