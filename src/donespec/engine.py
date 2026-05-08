from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Any

from donespec.checkers import get_checker
from donespec.models import CheckGroup, CheckResult, ValidationContext, ValidationReport


def run_check(config: dict[str, Any], group: CheckGroup, context: ValidationContext) -> CheckResult:
    checker_class = get_checker(config["type"])
    checker = checker_class(config=config, group=group, context=context)
    return checker.run()


def validate_payload(
    payload: dict[str, Any], *, spec_path: Path, root_dir: Path, fail_fast: bool = False
) -> ValidationReport:
    started = perf_counter()
    context = ValidationContext(root_dir=root_dir, spec_path=spec_path)
    results: list[CheckResult] = []

    for group in ("must_pass", "must_not"):
        for config in payload.get(group, []):
            result = run_check(config=config, group=group, context=context)  # type: ignore[arg-type]
            results.append(result)
            if fail_fast and not result.passed:
                break
        if fail_fast and results and not results[-1].passed:
            break

    duration_ms = (perf_counter() - started) * 1000
    failed_checks = sum(1 for result in results if not result.passed)

    return ValidationReport(
        version=payload["version"],
        task_id=payload["task_id"],
        passed=failed_checks == 0,
        total_checks=len(results),
        failed_checks=failed_checks,
        duration_ms=duration_ms,
        results=results,
    )
