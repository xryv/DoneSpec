from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any


def explain_payload(
    payload: dict[str, Any],
    *,
    spec_path: Path | None = None,
) -> dict[str, Any]:
    """Return a machine-readable explanation of a DoneSpec contract."""
    checks = _checks(payload)

    groups = {
        "must_pass": len(payload.get("must_pass", [])),
        "must_not": len(payload.get("must_not", [])),
    }

    types = Counter(check["type"] for check in checks if isinstance(check.get("type"), str))

    return {
        "spec_path": str(spec_path) if spec_path else None,
        "schema": payload.get("$schema"),
        "version": payload.get("version"),
        "task_id": payload.get("task_id"),
        "description": payload.get("description"),
        "total_checks": len(checks),
        "groups": groups,
        "types": dict(sorted(types.items())),
        "checks": [_check_summary(check) for check in checks],
        "recommended_gate": "donespec validate done.json --strict",
    }


def explain_to_text(explanation: dict[str, Any]) -> str:
    """Return a human-readable explanation of a DoneSpec contract."""
    lines: list[str] = []

    task_id = explanation.get("task_id") or "<unknown>"
    spec_path = explanation.get("spec_path")
    schema = explanation.get("schema")
    description = explanation.get("description")
    total_checks = explanation.get("total_checks", 0)
    groups = explanation.get("groups", {})
    types = explanation.get("types", {})
    checks = explanation.get("checks", [])

    lines.append(f"DoneSpec explanation: {task_id}")
    lines.append("")

    if spec_path:
        lines.append(f"Spec: {spec_path}")

    lines.append(f"Version: {explanation.get('version')}")
    lines.append(f"Total checks: {total_checks}")

    if schema:
        lines.append(f"Schema: {schema}")

    if description:
        lines.append("")
        lines.append("Description:")
        lines.append(str(description))

    lines.append("")
    lines.append("Groups:")
    lines.append(f"- must_pass: {groups.get('must_pass', 0)}")
    lines.append(f"- must_not: {groups.get('must_not', 0)}")

    lines.append("")
    lines.append("Check types:")

    if types:
        for check_type, count in types.items():
            lines.append(f"- {check_type}: {count}")
    else:
        lines.append("- none")

    _append_group(lines, checks, "must_pass", "Must pass", "✓")
    _append_group(lines, checks, "must_not", "Must not", "✗")

    lines.append("")
    lines.append("Recommended gate:")
    lines.append(str(explanation.get("recommended_gate")))

    return "\n".join(lines) + "\n"


def _checks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    for group in ("must_pass", "must_not"):
        group_checks = payload.get(group, [])

        if not isinstance(group_checks, list):
            continue

        for index, check in enumerate(group_checks):
            if not isinstance(check, dict):
                continue

            item = dict(check)
            item["_group"] = group
            item["_index"] = index
            items.append(item)

    return items


def _check_summary(check: dict[str, Any]) -> dict[str, Any]:
    detail_fields = [
        "run",
        "path",
        "pattern",
        "url",
        "method",
        "expected_status",
        "expected_exit_code",
        "timeout_seconds",
        "flags",
    ]

    details = {field: check[field] for field in detail_fields if field in check}

    return {
        "group": check.get("_group"),
        "index": check.get("_index"),
        "id": check.get("id"),
        "name": check.get("name"),
        "type": check.get("type"),
        "details": details,
    }


def _append_group(
    lines: list[str],
    checks: list[dict[str, Any]],
    group: str,
    title: str,
    symbol: str,
) -> None:
    group_checks = [check for check in checks if check.get("group") == group]

    lines.append("")
    lines.append(f"{title}:")

    if not group_checks:
        lines.append("- none")
        return

    for check in group_checks:
        index = int(check.get("index", 0)) + 1
        check_type = check.get("type") or "<unknown>"
        name = check.get("name") or "<unnamed>"
        details = check.get("details", {})

        lines.append(f"{symbol} {index}. [{check_type}] {name}")

        if isinstance(details, dict):
            for key, value in details.items():
                lines.append(f"   {key}: {value}")
