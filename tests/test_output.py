from __future__ import annotations

from rich.console import Console

from donespec.models import CheckResult, ValidationReport
from donespec.output import print_human_report, safe_for_encoding, write_text


class EncodingLimitedStream:
    encoding = "cp1252"

    def __init__(self) -> None:
        self.value = ""

    def write(self, text: str) -> int:
        text.encode(self.encoding)
        self.value += text
        return len(text)

    def flush(self) -> None:
        return None

    def isatty(self) -> bool:
        return False


def test_safe_for_encoding_preserves_utf8_text() -> None:
    text = "\u2713 passed \u2192 done"

    assert safe_for_encoding(text, "utf-8") == text


def test_safe_for_encoding_replaces_status_glyphs_for_cp1252() -> None:
    text = "\u2713 passed\n\u2717 failed\nagent \u2192 contract"

    safe = safe_for_encoding(text, "cp1252")

    assert "+ passed" in safe
    assert "x failed" in safe
    assert "agent -> contract" in safe
    safe.encode("cp1252")


def test_write_text_falls_back_for_cp1252_stream() -> None:
    stream = EncodingLimitedStream()

    write_text("\u2713 ok\n\u2717 failed\n", stream)

    assert stream.value == "+ ok\nx failed\n"


def test_print_human_report_uses_ascii_status_symbols_for_cp1252_stream() -> None:
    stream = EncodingLimitedStream()
    console = Console(file=stream, force_terminal=False, color_system=None)
    report = ValidationReport(
        version="1.0",
        task_id="cp1252-output",
        passed=False,
        total_checks=2,
        failed_checks=1,
        duration_ms=1.0,
        results=[
            CheckResult(
                name="README exists",
                type="file_exists",
                group="must_pass",
                passed=True,
                duration_ms=0.1,
            ),
            CheckResult(
                name="README was not modified",
                type="file_not_modified",
                group="must_not",
                passed=False,
                duration_ms=0.2,
                error="file changed",
            ),
        ],
    )

    print_human_report(report, console=console)

    assert "+ README exists" in stream.value
    assert "x README was not modified" in stream.value
    assert "\u2713" not in stream.value
    assert "\u2717" not in stream.value
