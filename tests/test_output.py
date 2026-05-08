from __future__ import annotations

from donespec.output import safe_for_encoding, write_text


class EncodingLimitedStream:
    encoding = "cp1252"

    def __init__(self) -> None:
        self.value = ""

    def write(self, text: str) -> int:
        text.encode(self.encoding)
        self.value += text
        return len(text)


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
