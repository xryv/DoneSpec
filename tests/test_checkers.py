from __future__ import annotations

import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

from donespec.engine import validate_payload


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(204)
        self.end_headers()

    def log_message(self, format, *args):
        return


def test_command_checker_passes(tmp_path: Path):
    payload = {
        "version": "1.0",
        "task_id": "command-pass",
        "must_pass": [{"type": "command", "run": "python -c 'print(123)'"}],
    }

    report = validate_payload(payload, spec_path=tmp_path / "done.json", root_dir=tmp_path)

    assert report.passed is True
    assert report.results[0].metadata["exit_code"] == 0


def test_file_and_regex_checkers(tmp_path: Path):
    source = tmp_path / "src" / "auth.ts"
    source.parent.mkdir()
    source.write_text("export const returnTo = '/home'\n", encoding="utf-8")

    payload = {
        "version": "1.0",
        "task_id": "regex-pass",
        "must_pass": [
            {"type": "file_exists", "path": "src/auth.ts"},
            {"type": "regex_in_file", "path": "src/auth.ts", "pattern": "returnTo"},
            {"type": "regex_absent", "path": "src/auth.ts", "pattern": "password = 'admin'"},
        ],
    }

    report = validate_payload(payload, spec_path=tmp_path / "done.json", root_dir=tmp_path)

    assert report.passed is True
    assert report.total_checks == 3


def test_file_not_modified_detects_forbidden_change(tmp_path: Path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)
    target = tmp_path / "src" / "types.ts"
    target.parent.mkdir()
    target.write_text("export type UserId = string\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"], cwd=tmp_path, check=True, capture_output=True
    )

    target.write_text("export type UserId = number\n", encoding="utf-8")

    payload = {
        "version": "1.0",
        "task_id": "forbidden-change",
        "must_not": [{"type": "file_not_modified", "path": "src/types.ts"}],
    }

    report = validate_payload(payload, spec_path=tmp_path / "done.json", root_dir=tmp_path)

    assert report.passed is False
    assert "Forbidden path modified" in (report.results[0].error or "")


def test_http_check_passes(tmp_path: Path):
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        payload = {
            "version": "1.0",
            "task_id": "api-check",
            "must_pass": [
                {
                    "type": "http_check",
                    "url": f"http://127.0.0.1:{server.server_port}/health",
                    "expected_status": 204,
                }
            ],
        }
        report = validate_payload(payload, spec_path=tmp_path / "done.json", root_dir=tmp_path)
    finally:
        server.shutdown()

    assert report.passed is True
