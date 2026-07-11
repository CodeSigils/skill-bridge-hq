#!/usr/bin/env python3
"""Validate docs/ frontmatter: required fields, expiry check, basic integrity.

Checks:
  - Required frontmatter fields present (status, date, purpose)
  - expires field exists (or warn if missing)
  - YAML parses correctly
  - No unlabelled code fences (maintainability)
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, date
from pathlib import Path

import yaml

DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"

# Regex to match frontmatter between --- delimiters
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
# Regex to match code fences with optional language label
FENCE_RE = re.compile(r"^```(\w*)$")


def parse_frontmatter(content: str) -> dict | None:
    """Parse YAML frontmatter from markdown content. Returns None if missing."""
    match = FRONTMATTER_RE.search(content)
    if not match:
        return None
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def check_expiry(fm: dict, fname: str) -> tuple[list[str], list[str]]:
    """Check expires field. Returns (errors, warnings)."""
    errors = []
    warnings = []

    if "expires" not in fm:
        warnings.append(f"{fname}: no 'expires' field — add one for freshness guidance")
        return errors, warnings

    expires_val = fm["expires"]
    expiry: datetime | None = None

    if isinstance(expires_val, date) and not isinstance(expires_val, datetime):
        expiry = datetime.combine(expires_val, datetime.min.time())
    elif isinstance(expires_val, str):
        try:
            expiry = datetime.strptime(expires_val, "%Y-%m-%d")
        except ValueError:
            errors.append(f"{fname}: 'expires' not a valid YYYY-MM-DD date")
            return errors, warnings
    elif isinstance(expires_val, datetime):
        expiry = expires_val
    else:
        errors.append(f"{fname}: 'expires' not a date or string")
        return errors, warnings

    if expiry and expiry < datetime.now():
        warnings.append(f"{fname}: expired on {fm['expires']}")

    return errors, warnings


def check_fences(content: str, fname: str) -> list[str]:
    """Check for unlabelled code fences. Returns list of warnings."""
    warnings = []
    lines = content.split("\n")
    fences: list[tuple[int, str]] = []  # (line_number, language)

    for i, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if match:
            # Skip frontmatter delimiters (---)
            if line.startswith("---"):
                continue
            lang = match.group(1).strip()
            fences.append((i + 1, lang))

    # Pair up opening/closing fences
    for i in range(0, len(fences), 2):
        if i + 1 >= len(fences):
            warnings.append(f"{fname}: unmatched code fence at line {fences[i][0]}")
            break
        open_line, lang = fences[i]
        close_line, _ = fences[i + 1]
        if not lang:
            warnings.append(f"{fname}: unlabelled code fence at line {open_line} (closes at {close_line})")

    return warnings


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not DOCS_DIR.exists():
        print(f"FAIL: docs directory not found at {DOCS_DIR}")
        return 1

    for fname in sorted(os.listdir(DOCS_DIR)):
        if not fname.endswith(".md"):
            continue
        path = DOCS_DIR / fname
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{fname}: could not read: {exc}")
            continue

        fm = parse_frontmatter(content)
        if fm is None:
            errors.append(f"{fname}: missing or invalid YAML frontmatter")
            continue

        # Required fields
        for field in ("status", "date", "purpose"):
            if field not in fm:
                errors.append(f"{fname}: missing required field '{field}'")

        # Expiry check
        e, w = check_expiry(fm, fname)
        errors.extend(e)
        warnings.extend(w)

        # Fence check
        warnings.extend(check_fences(content, fname))

        print(f"  PASS  {fname}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  WARN  {w}")

    if errors:
        print(f"\n{'=' * 50}")
        for e in errors:
            print(f"  FAIL  {e}")
        return 1

    print("\nPASS: All docs valid")
    return 0


if __name__ == "__main__":
    from pathlib import Path
    sys.exit(main())