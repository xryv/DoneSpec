from __future__ import annotations

from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from donespec.checkers.base import Checker, timed


class HttpCheckChecker(Checker):
    type_name = "http_check"

    def default_name(self) -> str:
        return f"{self.config.get('method', 'GET')} {self.config['url']} returns expected status"

    @timed
    def run(self, started: float):
        url = self.config["url"]
        method = self.config.get("method", "GET")
        expected_status = int(self.config.get("expected_status", 200))
        timeout_seconds = float(self.config.get("timeout_seconds", 10))
        headers = self.config.get("headers", {})

        request = Request(url, method=method, headers=headers)
        status: int | None = None
        reason: str | None = None

        try:
            with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - user-controlled local validation tool
                status = int(response.status)
                reason = response.reason
        except HTTPError as exc:
            status = int(exc.code)
            reason = exc.reason
        except URLError as exc:
            duration_ms = (perf_counter() - started) * 1000
            return self.result(
                passed=False,
                duration_ms=duration_ms,
                error=f"HTTP request failed: {exc.reason}",
                metadata={"url": url, "method": method, "expected_status": expected_status},
            )

        duration_ms = (perf_counter() - started) * 1000
        passed = status == expected_status
        return self.result(
            passed=passed,
            duration_ms=duration_ms,
            error=None if passed else f"Expected HTTP {expected_status}, got {status}",
            details=f"status={status}, reason={reason}",
            metadata={
                "url": url,
                "method": method,
                "status": status,
                "reason": reason,
                "expected_status": expected_status,
            },
        )
