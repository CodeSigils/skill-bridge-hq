#!/usr/bin/env python3
"""Monitor evidence URLs, redirects, JSON syntax, and minimal response shapes."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "docs" / "evidence-urls.json"


class RedirectTracker(urllib.request.HTTPRedirectHandler):
    """Count redirects followed by one opener invocation."""

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        self.count += 1
        return super().redirect_request(request, file_pointer, code, message, headers, new_url)


@dataclass(frozen=True)
class CheckResult:
    status: int | str
    redirects: int
    content: str
    final_url: str


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict[str, Any]]:
    """Load and validate the manifest envelope."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: could not load {path}: {exc}") from exc
    entries = document.get("urls") if isinstance(document, dict) else None
    if not isinstance(entries, list):
        raise SystemExit(f"FAIL: {path} must contain a top-level 'urls' list")
    return entries


def validate_entry(entry: dict[str, Any]) -> None:
    """Validate one manifest entry before network access."""
    for field in ("name", "url", "expected_statuses", "source_section"):
        if field not in entry:
            raise ValueError(f"missing required field '{field}'")
    if not isinstance(entry["name"], str) or not isinstance(entry["url"], str):
        raise ValueError("name and url must be strings")
    statuses = entry["expected_statuses"]
    if not isinstance(statuses, list) or not statuses or not all(isinstance(value, int) for value in statuses):
        raise ValueError("expected_statuses must be a non-empty integer list")
    max_redirects = entry.get("max_redirects")
    if max_redirects is not None and (not isinstance(max_redirects, int) or max_redirects < 0):
        raise ValueError("max_redirects must be a non-negative integer")
    canonical_url = entry.get("canonical_url")
    if canonical_url is not None and not isinstance(canonical_url, str):
        raise ValueError("canonical_url must be a string")
    schema = entry.get("json_schema")
    if schema is not None:
        if entry.get("content_type") != "json" or not isinstance(schema, dict):
            raise ValueError("json_schema requires content_type=json and an object schema")
        if schema.get("type") not in {"array", "object"}:
            raise ValueError("json_schema.type must be 'array' or 'object'")
        required = schema.get("required_keys", [])
        if not isinstance(required, list) or not all(isinstance(key, str) for key in required):
            raise ValueError("json_schema.required_keys must be a string list")


def validate_json_shape(value: Any, schema: dict[str, Any] | None) -> str:
    """Return a compact semantic validation result."""
    if schema is None:
        return "VALID_JSON"
    expected = schema["type"]
    if expected == "array" and not isinstance(value, list):
        return "SCHEMA:expected-array"
    if expected == "object" and not isinstance(value, dict):
        return "SCHEMA:expected-object"
    if isinstance(value, dict):
        missing = [key for key in schema.get("required_keys", []) if key not in value]
        if missing:
            return f"SCHEMA:missing-{','.join(missing)}"
    return "VALID_SCHEMA"


def check_url(entry: dict[str, Any], timeout: int = 15) -> CheckResult:
    """Fetch one URL and validate JSON when requested."""
    tracker = RedirectTracker()
    opener = urllib.request.build_opener(tracker)
    request = urllib.request.Request(
        entry["url"],
        method="GET",
        headers={"User-Agent": "skill-discovery-contract-monitor/2"},
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            body = response.read() if entry.get("content_type") == "json" else b""
            if entry.get("content_type") != "json":
                return CheckResult(response.status, tracker.count, "-", response.geturl())
            try:
                value = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return CheckResult(response.status, tracker.count, "INVALID_JSON", response.geturl())
            return CheckResult(
                response.status,
                tracker.count,
                validate_json_shape(value, entry.get("json_schema")),
                response.geturl(),
            )
    except urllib.error.HTTPError as exc:
        return CheckResult(exc.code, tracker.count, f"HTTP_{exc.code}", exc.geturl())
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return CheckResult("ERROR", tracker.count, str(exc), entry["url"])


def contract_drift_reasons(entry: dict[str, Any], result: CheckResult) -> list[str]:
    """Return concrete reasons why a response differs from its manifest contract."""
    reasons: list[str] = []
    if result.status not in entry["expected_statuses"]:
        reasons.append(f"status={result.status}")
    if result.redirects > entry.get("max_redirects", result.redirects):
        reasons.append(f"redirects={result.redirects}")
    canonical_url = entry.get("canonical_url")
    if canonical_url is not None and result.final_url != canonical_url:
        reasons.append(f"final_url={result.final_url}")
    if entry.get("content_type") == "json" and result.content not in {"VALID_JSON", "VALID_SCHEMA"}:
        reasons.append(result.content)
    return reasons


def result_is_valid(entry: dict[str, Any], result: CheckResult) -> bool:
    """Return whether status, redirects, canonical URL, and content all match."""
    return not contract_drift_reasons(entry, result)


def main() -> int:
    """Run scheduled external contract monitoring."""
    entries = load_manifest()
    failed = False
    print(f"{'Name':<44} {'Status':<8} {'Redirects':<10} {'Content':<28} Result")
    print("-" * 105)
    for entry in sorted(entries, key=lambda value: str(value.get("name", "")).casefold()):
        try:
            validate_entry(entry)
        except ValueError as exc:
            print(f"{entry.get('name', '<unnamed>'):<44} {'-':<8} {'-':<10} {'-':<28} MANIFEST: {exc}")
            failed = True
            continue
        result = check_url(entry)
        reasons = contract_drift_reasons(entry, result)
        valid = not reasons
        failed = failed or not valid
        print(
            f"{entry['name']:<44} {str(result.status):<8} {result.redirects:<10} "
            f"{result.content[:28]:<28} {'OK' if valid else 'DRIFT:' + ';'.join(reasons)}"
        )
    if failed:
        print("\nFAIL: one or more external contracts drifted")
        return 1
    print("\nPASS: external status and minimal response contracts match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
