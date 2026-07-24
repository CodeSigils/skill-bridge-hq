#!/usr/bin/env python3
"""Check for Hermes-specific references in portable skills.

This is the portability gate for the shipped skill surface. It catches
references that would make the methodology unusable for non-Hermes agents.

Patterns checked in skills/:
  - skill_view, skill_manage (Hermes-specific tool names)
  - ~/.hermes/ (Hermes config path)
  - hermes CLI commands such as `hermes skills ...`
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILLS_DIR = Path("skills")

FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Hermes tool name", re.compile(r"\bskill_(?:view|manage)\b", re.IGNORECASE)),
    ("Hermes config path", re.compile(r"~/\.hermes(?:/|\b)", re.IGNORECASE)),
    (
        "Hermes CLI command",
        re.compile(
            r"\bhermes\s+(?:skills?|config|tools?|setup|help|doctor|gateway|run|serve|cron)\b",
            re.IGNORECASE,
        ),
    ),
)


def iter_skill_markdown_files(root: Path) -> list[Path]:
    """Yield tracked portable skill markdown files under root."""
    if not root.exists():
        raise FileNotFoundError(f"{root} does not exist")
    return sorted(root.rglob("*.md"))


def scan_file(path: Path) -> list[tuple[Path, int, str, str]]:
    """Return portability violations for one file."""
    violations: list[tuple[Path, int, str, str]] = []
    text = path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for label, pattern in FORBIDDEN_PATTERNS:
            if pattern.search(line):
                violations.append((path, line_no, label, line.rstrip()))
    return violations


def main() -> int:
    try:
        files = iter_skill_markdown_files(SKILLS_DIR)
    except OSError as exc:
        print(f"FAIL: could not scan {SKILLS_DIR}: {exc}")
        return 1

    violations: list[tuple[Path, int, str, str]] = []
    for path in files:
        try:
            violations.extend(scan_file(path))
        except OSError as exc:
            print(f"FAIL: could not read {path}: {exc}")
            return 1

    if violations:
        print("FAIL: Hermes-specific references found in skills/:")
        for path, line_no, label, line in violations:
            print(f"{path}:{line_no}: {label}: {line}")
        return 1

    print("PASS: No Hermes-specific references in skills/")
    return 0


if __name__ == "__main__":
    sys.exit(main())