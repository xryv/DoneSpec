from __future__ import annotations

import re
from collections import Counter
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any

from donespec.exceptions import SpecValidationError

REGEX_CHECK_TYPES = {"regex_in_file", "regex_absent"}
PATH_CHECK_TYPES = {
    "file_exists",
    "regex_in_file",
    "regex_absent",
    "file_not_modified",
}

REGEX_FLAGS = {
    "IGNORECASE": re.IGNORECASE,
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
}


def validate_strict_payload(payload: dict[str, Any]) -> None:
    """Validate semantic DoneSpec rules that go beyond JSON Schema."""
    errors: list[str] = []

    must_pass = payload.get("must_pass", [])
    must_not = payload.get("must_not", [])

    if not must_pass and not must_not:
        errors.append("done.json must contain at least one check in must_pass or must_not")

    checks = _iter_checks(payload)

    _validate_names(checks, errors)
    _validate_ids(checks, errors)
    _validate_paths(checks, errors)
    _validate_regex_patterns(checks, errors)

    if errors:
        raise SpecValidationError(
            "Strict validation failed:\n" + "\n".join(f"- {error}" for error in errors)
        )


def _iter_checks(payload: dict[str, Any]) -> list[tuple[str, int, dict[str, Any]]]:
    checks: list[tuple[str, int, dict[str, Any]]] = []

    for group in ("must_pass", "must_not"):
        group_checks = payload.get(group, [])

        if not isinstance(group_checks, list):
            continue

        for index, check in enumerate(group_checks):
            if isinstance(check, dict):
                checks.append((group, index, check))

    return checks


def _validate_names(
    checks: list[tuple[str, int, dict[str, Any]]],
    errors: list[str],
) -> None:
    names: list[str] = []

    for group, index, check in checks:
        pointer = f"{group}[{index}]"
        name = check.get("name")

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{pointer} must define a non-empty name")
            continue

        names.append(name)

    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)

    for name in duplicates:
        errors.append(f"duplicate check name: {name!r}")


def _validate_ids(
    checks: list[tuple[str, int, dict[str, Any]]],
    errors: list[str],
) -> None:
    ids: list[str] = []

    for group, index, check in checks:
        pointer = f"{group}[{index}]"
        check_id = check.get("id")

        if check_id is None:
            continue

        if not isinstance(check_id, str) or not check_id.strip():
            errors.append(f"{pointer} id must be a non-empty string when provided")
            continue

        ids.append(check_id)

    duplicates = sorted(check_id for check_id, count in Counter(ids).items() if count > 1)

    for check_id in duplicates:
        errors.append(f"duplicate check id: {check_id!r}")


def _validate_paths(
    checks: list[tuple[str, int, dict[str, Any]]],
    errors: list[str],
) -> None:
    for group, index, check in checks:
        check_type = check.get("type")

        if check_type not in PATH_CHECK_TYPES:
            continue

        pointer = f"{group}[{index}]"
        path = check.get("path")

        if not isinstance(path, str):
            continue

        if _is_absolute_path(path):
            errors.append(f"{pointer} path must be relative: {path!r}")

        if _contains_parent_traversal(path):
            errors.append(f"{pointer} path must not contain '..': {path!r}")


def _validate_regex_patterns(
    checks: list[tuple[str, int, dict[str, Any]]],
    errors: list[str],
) -> None:
    for group, index, check in checks:
        check_type = check.get("type")

        if check_type not in REGEX_CHECK_TYPES:
            continue

        pointer = f"{group}[{index}]"
        pattern = check.get("pattern")

        if not isinstance(pattern, str):
            continue

        try:
            re.compile(pattern, _regex_flags(check.get("flags", [])))
        except re.error as exc:
            errors.append(f"{pointer} regex pattern is invalid: {exc}")


def _regex_flags(flag_names: Any) -> int:
    if not isinstance(flag_names, list):
        return 0

    value = 0

    for flag_name in flag_names:
        if isinstance(flag_name, str):
            value |= REGEX_FLAGS.get(flag_name, 0)

    return value


def _is_absolute_path(path: str) -> bool:
    return PureWindowsPath(path).is_absolute() or PurePosixPath(path).is_absolute()


def _contains_parent_traversal(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return ".." in normalized.split("/")
