#!/usr/bin/env python3
"""Validate a single Agent Skill directory.

Usage:
    python scripts/validate-skill.py skills/skill-discovery
    python scripts/validate-skill.py skills/skill-discovery --root /path/to/repo

The script inspects SKILL.md inside the given directory for frontmatter
correctness, payload budget, description limits, code fence balance,
and relative link integrity.  Exit code 0 means clean, 1 means violations
found (printed to stderr).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
FENCE_RE = re.compile(r"^```([^`]*)$")
MARKDOWN_LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(content: str) -> dict | None:
    """Return parsed leading YAML frontmatter, or ``None``."""
    match = FRONTMATTER_RE.search(content)
    if not match:
        return None
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    return frontmatter if isinstance(frontmatter, dict) else None


def check_fences(content: str, label: str) -> list[str]:
    """Require matched fences and a language tag on opening fences."""
    errors: list[str] = []
    opening: tuple[int, str] | None = None
    for line_number, line in enumerate(content.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        if opening is None:
            language = match.group(1).strip()
            opening = (line_number, language)
            if not language:
                errors.append(
                    f"{label}:{line_number}: opening code fence has no language"
                )
        else:
            opening = None
    if opening is not None:
        errors.append(f"{label}:{opening[0]}: unmatched code fence")
    return errors


def check_relative_links(path: Path, content: str, root: Path) -> list[str]:
    """Ensure relative Markdown links resolve inside the repository."""
    errors: list[str] = []
    for target in MARKDOWN_LINK_RE.findall(content):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(
                f"{path.relative_to(root)}: link escapes repository: {target}"
            )
            continue
        if not resolved.exists():
            errors.append(
                f"{path.relative_to(root)}: missing link target: {target}"
            )
    return errors


def find_repo_root(start: Path) -> Path | None:
    """Walk upward from *start* looking for a ``.git`` directory."""
    current = start.resolve()
    while current != current.parent:
        if (current / ".git").is_dir():
            return current
        current = current.parent
    return None


def validate_skill(skill_md: Path, root: Path | None = None) -> list[str]:
    """Validate Agent Skills frontmatter, size, references, and fences."""
    if root is None:
        root = find_repo_root(skill_md) or skill_md.resolve().parent.parent.parent
    label = str(skill_md.relative_to(root))
    content = skill_md.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        return [f"{label}: missing or invalid YAML frontmatter"]

    errors: list[str] = []
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
        errors.append(f"{label}: invalid or missing skill name")
    elif name != skill_md.parent.name:
        errors.append(
            f"{label}: name '{name}' does not match directory "
            f"'{skill_md.parent.name}'"
        )
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{label}: missing non-empty description")
    elif len(description) > 1024:
        errors.append(f"{label}: description exceeds 1024 characters")
    line_count = len(content.splitlines())
    if line_count > 500:
        errors.append(
            f"{label}: {line_count} lines exceeds the 500-line payload budget"
        )
    errors.extend(check_fences(content, label))
    errors.extend(check_relative_links(skill_md, content, root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", help="Directory containing SKILL.md")
    parser.add_argument(
        "--root",
        help="Repository root for link validation (auto-detected if omitted)",
    )
    args = parser.parse_args()
    skill_path = Path(args.skill_dir).resolve()
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: {skill_md} not found", file=sys.stderr)
        return 1
    root = Path(args.root).resolve() if args.root else find_repo_root(skill_path)
    errors = validate_skill(skill_md, root)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
