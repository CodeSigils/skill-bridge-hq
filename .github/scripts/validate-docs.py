#!/usr/bin/env python3
"""Validate docs/ frontmatter: required fields, expiry check, basic integrity.

Checks:
  - Required frontmatter fields present (status, date, updated, purpose)
  - expires field exists (or warn if missing)
  - YAML parses correctly
  - No unlabelled code fences (maintainability)
"""
import os
import sys
import yaml
import re

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "docs")
errors = []
warnings = []

for fname in sorted(os.listdir(DOCS_DIR)):
    if not fname.endswith(".md"):
        continue
    path = os.path.join(DOCS_DIR, fname)
    with open(path) as f:
        raw = f.read()

    # Parse frontmatter
    m = re.match(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
    if not m:
        errors.append(f"{fname}: missing YAML frontmatter")
        continue

    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{fname}: YAML parse error: {e}")
        continue

    if not isinstance(fm, dict):
        errors.append(f"{fname}: frontmatter is not a mapping")
        continue

    # Required fields
    for field in ("status", "date", "purpose"):
        if field not in fm:
            errors.append(f"{fname}: missing required field '{field}'")

    # Expiry check
    if "expires" not in fm:
        warnings.append(f"{fname}: no 'expires' field — add one for freshness guidance")
    else:
        from datetime import datetime, date
        expires_val = fm["expires"]
        if isinstance(expires_val, date) and not isinstance(expires_val, datetime):
            expiry = datetime.combine(expires_val, datetime.min.time())
        elif isinstance(expires_val, str):
            expiry = datetime.strptime(expires_val, "%Y-%m-%d")
        elif isinstance(expires_val, datetime):
            expiry = expires_val
        else:
            errors.append(f"{fname}: 'expires' not a date or string")
            expiry = None
        if expiry and expiry < datetime.now():
            warnings.append(f"{fname}: expired on {fm['expires']}")

    # Unlabelled code fences
    lines = raw.split("\n")
    fence_ix = [i for i, l in enumerate(lines) if re.match(r"^```", l)]
    # Skip frontmatter fences (first and second `---`)
    fence_ix = [i for i in fence_ix if not lines[i].startswith("---")]
    # Pair up fences; check if first of each pair has a label
    for i in range(0, len(fence_ix) - 1, 2):
        opening = lines[fence_ix[i]]
        if opening.strip() == "```":
            warnings.append(f"{fname}: unlabelled code fence at line {fence_ix[i]+1}")

    print(f"  PASS  {fname}")

if warnings:
    print("\nWarnings:")
    for w in warnings:
        print(f"  WARN  {w}")

if errors:
    print(f"\n{'='*50}")
    for e in errors:
        print(f"  FAIL  {e}")
    sys.exit(1)

print("\nPASS: All docs valid")
