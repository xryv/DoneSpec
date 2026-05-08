from __future__ import annotations

import json
import sys
from typing import Any

from rich.console import Console
from rich.text import Text

from donespec.models import ValidationReport


def report_to_json(report: ValidationReport) -> str:
    return json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True)


def stream_supports_text(text: str, encoding: str | None) -> bool:
    try:
        text.encode(encoding or "utf-8")
    except UnicodeEncodeError:
        return False
    return True


def status_symbols_for_console(console: Console) -> tuple[str, str]:
    encoding = getattr(getattr(console, "file", None), "encoding", None) or sys.stdout.encoding

    if stream_supports_text("\u2713\u2717", encoding):
        return "\u2713", "\u2717"

    return "+", "x"


def status_symbol_for_console(console: Console, passed: bool) -> str:
    passed_symbol, failed_symbol = status_symbols_for_console(console)
    return passed_symbol if passed else failed_symbol


def safe_symbol_for_console(console: Console, symbol: str, fallback: str) -> str:
    encoding = getattr(getattr(console, "file", None), "encoding", None) or sys.stdout.encoding

    if stream_supports_text(symbol, encoding):
        return symbol

    return fallback


def _style(passed: bool) -> str:
    return "green" if passed else "red"


def print_human_report(report: ValidationReport, console: Console | None = None) -> None:
    console = console or Console()
    passed_symbol, failed_symbol = status_symbols_for_console(console)
    console.print(f"DoneSpec validation: [bold]{report.task_id}[/bold]")
    console.print()

    for result in report.results:
        line = Text()
        symbol = passed_symbol if result.passed else failed_symbol
        line.append(symbol, style=f"bold {_style(result.passed)}")
        line.append(" ")
        line.append(result.name)
        line.append(f"  ({result.duration_ms:.1f}ms)", style="dim")
        console.print(line)
        if not result.passed and result.error:
            console.print(f"  [red]{result.error}[/red]")

    console.print()
    if report.passed:
        console.print(
            f"[bold green]Validation passed.[/bold green] {report.total_checks} checks passed."
        )
        console.print("Exit code: 0", style="dim")
        return

    plural = "check" if report.failed_checks == 1 else "checks"
    console.print("[bold red]Validation failed.[/bold red]")
    console.print(f"{report.failed_checks} {plural} failed.")
    console.print("Exit code: 1", style="dim")


def error_to_json(error: str) -> str:
    payload: dict[str, Any] = {"passed": False, "error": error}
    return json.dumps(payload, indent=2, sort_keys=True)


_ASCII_TRANSLATION = str.maketrans(
    {
        "\u2713": "+",
        "\u2717": "x",
        "\u2192": "->",
        "\u2193": "|",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2014": "-",
        "\u2013": "-",
        "\u2026": "...",
    }
)


def safe_for_encoding(text: str, encoding: str | None) -> str:
    """Return text that can be written to a stream with the given encoding."""

    if not encoding:
        return text

    try:
        text.encode(encoding)
    except UnicodeEncodeError:
        text = text.translate(_ASCII_TRANSLATION)
        return text.encode(encoding, errors="replace").decode(encoding, errors="replace")

    return text


def write_text(text: str, stream: object | None = None) -> None:
    """Write text safely, including on Windows cp1252 terminals and pipes."""

    target = stream or sys.stdout

    try:
        target.write(text)
    except UnicodeEncodeError:
        encoding = getattr(target, "encoding", None)
        target.write(safe_for_encoding(text, encoding))
