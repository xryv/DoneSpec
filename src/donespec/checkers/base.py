from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any

from donespec.models import CheckGroup, CheckResult, ValidationContext


class Checker(ABC):
    """Base class for deterministic checkers."""

    type_name: str

    def __init__(self, config: dict[str, Any], group: CheckGroup, context: ValidationContext) -> None:
        self.config = config
        self.group = group
        self.context = context

    @abstractmethod
    def run(self) -> CheckResult:
        """Execute the checker and return a structured result."""

    def result(
        self,
        *,
        passed: bool,
        duration_ms: float,
        error: str | None = None,
        details: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CheckResult:
        return CheckResult(
            id=self.config.get("id"),
            name=self.config.get("name") or self.default_name(),
            type=self.type_name,
            group=self.group,
            passed=passed,
            duration_ms=duration_ms,
            error=error,
            details=details,
            metadata=metadata or {},
        )

    def default_name(self) -> str:
        return self.type_name


def timed(fn):
    """Decorator helper for checker implementations."""

    def wrapper(self: Checker):
        started = perf_counter()
        try:
            return fn(self, started)
        except Exception as exc:  # noqa: BLE001 - checker failures must be reported, not crash the run
            duration_ms = (perf_counter() - started) * 1000
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error=str(exc),
                metadata={"exception_type": exc.__class__.__name__},
            )

    return wrapper
