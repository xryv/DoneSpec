from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

CheckGroup = Literal["must_pass", "must_not"]


class ValidationContext(BaseModel):
    """Runtime context shared by every checker."""

    root_dir: Path
    spec_path: Path

    model_config = {"arbitrary_types_allowed": True}


class CheckResult(BaseModel):
    """Structured result returned by every checker."""

    id: str | None = None
    name: str
    type: str
    group: CheckGroup
    passed: bool
    duration_ms: float = Field(ge=0)
    error: str | None = None
    details: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ValidationReport(BaseModel):
    """Complete validation report emitted by the engine."""

    version: str
    task_id: str
    passed: bool
    total_checks: int
    failed_checks: int
    duration_ms: float = Field(ge=0)
    results: list[CheckResult]

    @property
    def exit_code(self) -> int:
        return 0 if self.passed else 1
