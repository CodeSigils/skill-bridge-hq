#!/usr/bin/env python3
"""Verify evidence URLs against the documented expected state.

The URL list lives in docs/evidence-urls.json so the research evidence base has
one machine-readable source of truth. If the doc adds or removes URLs, update
that manifest instead of editing this script's code.

Usage:
  python3 .github/scripts/verify-marketplace-urls.py
  # Windows: py -3 .github/scripts/verify-marketplace-urls.py
  # Virtualenvs may also support: python .github/scripts/verify-marketplace-urls.py

Outputs a table of URL -> final status with drift annotations.
Exit code 0 = all URLs match documented expected state.
Exit code 1 = one or more URLs differs from the manifest.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "docs" / "evidence-urls.json"


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict[str, Any]]:
    """Load URL entries from the evidence manifest."""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"FAIL: could not read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL: invalid JSON in {path}: {exc}") from exc

    urls = manifest.get("urls")
    if not isinstance(urls, list):
        raise SystemExit(f"FAIL: {path} must contain a top-level 'urls' list")
    return urls


def validate_entry(entry: dict[str, Any]) -> None:
    """Validate one manifest entry before using it."""
    required = ("name", "url", "expected_statuses")
    missing = [key for key in required if key not in entry]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
    if not isinstance(entry["expected_statuses"], list) or not entry["expected_statuses"]:
        raise ValueError("expected_statuses must be a non-empty list")
    for status in entry["expected_statuses"]:
        if not isinstance(status, int):
            raise ValueError("expected_statuses must contain integers")


def check_url(url: str, content_type: str | None = None) -> tuple[int | str, int, str | None]:
    """Return (final_status_code, redirect_count, content_or_error) for one URL.

    When content_type is "json", captures response body and validates JSON.
    """
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "skill-discovery-url-verify"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status = response.status
            redirect_count = len(response.headers.get("Location", "").split("\n")) if "Location" in response.headers else 0
            # For a more accurate redirect count, we'd need to track intermediate responses
            # urllib follows redirects automatically, so we just check final status

            if content_type == "json":
                body = response.read().decode("utf-8")
                try:
                    json.loads(body)
                    return status, redirect_count, "VALID"
                except (json.JSONDecodeError, ValueError):
                    return status, redirect_count, "INVALID_JSON"
            return status, redirect_count, None

    except urllib.error.HTTPError as exc:
        return exc.code, 0, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return "ERROR", 0, str(exc.reason)
    except TimeoutError:
        return "TIMEOUT", 0, "timeout"
    except ValueError as exc:
        return "ERROR", 0, f"invalid URL: {exc}"


def classify_status(status: int | str, expected_statuses: list[int]) -> str:
    """Return OK when status matches the manifest, else DRIFT."""
    if isinstance(status, int) and status in expected_statuses:
        return "OK"
    return "DRIFT"


def main() -> int:
    entries = load_manifest()

    print("=== Evidence URL Re-verification ===")
    print(f"{'Name':<30s} {'Status':<8s} {'Expected':<12s} {'Redirects':<9s} {'Content':<12s} {'Note':<10s}")
    print("-" * 90)

    drift_found = False
    for entry in sorted(entries, key=lambda item: item["name"].lower()):
        try:
            validate_entry(entry)
        except ValueError as exc:
            print(f"  {entry.get('name', '<unnamed>'):<30s} {'-':<8s} {'-':<12s} {'-':<9s} {'-':<12s} MANIFEST: {exc}")
            drift_found = True
            continue

        content_type = entry.get("content_type")
        status, redirects, content = check_url(entry["url"], content_type)
        expected = entry["expected_statuses"]
        note = classify_status(status, expected)
        if note == "DRIFT":
            drift_found = True

        # Content check trumps status check for JSON endpoints
        content_label = content or "—"
        if content_type == "json" and content == "INVALID_JSON":
            note = "BROKEN"
            drift_found = True

        expected_text = "/".join(str(code) for code in expected)
        marker = "  ← DRIFT" if note == "DRIFT" else ""
        marker = "  ← BROKEN" if note == "BROKEN" else marker
        print(
            f"  {entry['name']:<30s} {str(status):<8s} {expected_text:<12s} "
            f"{str(redirects):<9s} {content_label:<12s} {note:<10s}{marker}"
        )

    if drift_found:
        print("\nRESULT: Drift or broken content detected — one or more URLs differ from docs/evidence-urls.json.")
        print("Update the manifest and research doc together after investigating the changed URL state.")
        return 1

    print("\nRESULT: All URLs match documented expected state and content validates OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())