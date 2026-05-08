from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from donespec.exceptions import SpecValidationError
from donespec.schema import validate_spec_payload
from donespec.strict import validate_strict_payload

VALID_GROUPS = {"must_pass", "must_not"}

VALID_CHECK_TYPES = {
    "command",
    "file_exists",
    "regex_in_file",
    "regex_absent",
    "file_not_modified",
    "http_check",
}


@dataclass(frozen=True)
class AddCheckResult:
    spec_path: Path
    group: str
    check: dict[str, Any]


def add_check_to_file(
    spec_path: Path,
    *,
    group: str,
    check_type: str,
    name: str,
    check_id: str | None = None,
    path: str | None = None,
    pattern: str | None = None,
    run: str | None = None,
    url: str | None = None,
    method: str = "GET",
    expected_status: int = 200,
    expected_exit_code: int = 0,
    timeout_seconds: float | None = None,
    flags: list[str] | None = None,
    headers_json: str | None = None,
) -> AddCheckResult:
    target = spec_path.resolve()
    payload = _load_payload(target)

    check = build_check(
        check_type=check_type,
        name=name,
        check_id=check_id,
        path=path,
        pattern=pattern,
        run=run,
        url=url,
        method=method,
        expected_status=expected_status,
        expected_exit_code=expected_exit_code,
        timeout_seconds=timeout_seconds,
        flags=flags,
        headers_json=headers_json,
    )

    updated = add_check_to_payload(payload, group=group, check=check)

    validate_spec_payload(updated)
    validate_strict_payload(updated)

    target.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")

    return AddCheckResult(spec_path=target, group=group, check=check)


def build_check(
    *,
    check_type: str,
    name: str,
    check_id: str | None = None,
    path: str | None = None,
    pattern: str | None = None,
    run: str | None = None,
    url: str | None = None,
    method: str = "GET",
    expected_status: int = 200,
    expected_exit_code: int = 0,
    timeout_seconds: float | None = None,
    flags: list[str] | None = None,
    headers_json: str | None = None,
) -> dict[str, Any]:
    normalized_type = check_type.strip().lower().replace("-", "_")

    if normalized_type not in VALID_CHECK_TYPES:
        allowed = ", ".join(sorted(VALID_CHECK_TYPES))
        raise SpecValidationError(f"Unsupported check type: {check_type!r}. Allowed: {allowed}")

    clean_name = name.strip()

    if not clean_name:
        raise SpecValidationError("Check name must not be empty")

    check: dict[str, Any] = {
        "type": normalized_type,
        "name": clean_name,
    }

    if check_id is not None and check_id.strip():
        check["id"] = check_id.strip()

    if normalized_type == "command":
        if not run or not run.strip():
            raise SpecValidationError("command checks require --run")

        check["run"] = run.strip()
        check["expected_exit_code"] = expected_exit_code

        if timeout_seconds is not None:
            check["timeout_seconds"] = timeout_seconds

    elif normalized_type in {"file_exists", "file_not_modified"}:
        if not path or not path.strip():
            raise SpecValidationError(f"{normalized_type} checks require --path")

        check["path"] = path.strip()

    elif normalized_type in {"regex_in_file", "regex_absent"}:
        if not path or not path.strip():
            raise SpecValidationError(f"{normalized_type} checks require --path")

        if pattern is None or not pattern:
            raise SpecValidationError(f"{normalized_type} checks require --pattern")

        check["path"] = path.strip()
        check["pattern"] = pattern

        if flags:
            check["flags"] = flags

    elif normalized_type == "http_check":
        if not url or not url.strip():
            raise SpecValidationError("http_check checks require --url")

        check["url"] = url.strip()
        check["method"] = method.strip().upper()
        check["expected_status"] = expected_status

        if timeout_seconds is not None:
            check["timeout_seconds"] = timeout_seconds

        headers = _parse_headers(headers_json)

        if headers:
            check["headers"] = headers

    return check


def add_check_to_payload(
    payload: dict[str, Any],
    *,
    group: str,
    check: dict[str, Any],
) -> dict[str, Any]:
    if group not in VALID_GROUPS:
        allowed = ", ".join(sorted(VALID_GROUPS))
        raise SpecValidationError(f"Invalid group: {group!r}. Allowed: {allowed}")

    updated = deepcopy(payload)
    updated.setdefault("must_pass", [])
    updated.setdefault("must_not", [])

    if not isinstance(updated[group], list):
        raise SpecValidationError(f"{group} must be a list")

    _reject_duplicate_name(updated, check)
    _reject_duplicate_id(updated, check)

    updated[group].append(check)

    return updated


def _load_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SpecValidationError(f"Spec file not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SpecValidationError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise SpecValidationError("Invalid done.json: root value must be an object")

    validate_spec_payload(payload)

    return payload


def _parse_headers(headers_json: str | None) -> dict[str, str]:
    if headers_json is None or not headers_json.strip():
        return {}

    try:
        payload = json.loads(headers_json)
    except json.JSONDecodeError as exc:
        raise SpecValidationError(f"Invalid --headers-json value: {exc}") from exc

    if not isinstance(payload, dict):
        raise SpecValidationError("--headers-json must be a JSON object")

    headers: dict[str, str] = {}

    for key, value in payload.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise SpecValidationError("--headers-json keys and values must be strings")

        headers[key] = value

    return headers


def _reject_duplicate_name(payload: dict[str, Any], check: dict[str, Any]) -> None:
    new_name = check.get("name")

    for existing in _iter_existing_checks(payload):
        if existing.get("name") == new_name:
            raise SpecValidationError(f"duplicate check name: {new_name!r}")


def _reject_duplicate_id(payload: dict[str, Any], check: dict[str, Any]) -> None:
    new_id = check.get("id")

    if not new_id:
        return

    for existing in _iter_existing_checks(payload):
        if existing.get("id") == new_id:
            raise SpecValidationError(f"duplicate check id: {new_id!r}")


def _iter_existing_checks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    for group in ("must_pass", "must_not"):
        group_checks = payload.get(group, [])

        if not isinstance(group_checks, list):
            continue

        for check in group_checks:
            if isinstance(check, dict):
                checks.append(check)

    return checks
