#!/usr/bin/env python3
"""Re-verify marketplace URLs listed in docs/ and report drift.

Usage:
  python .github/scripts/verify-marketplace-urls.py

Outputs a table of URL → status with drift annotations.
Exit code 0 = all stable, 1 = any URL drifted since last doc update.
"""

import subprocess
import sys
import os

DOC_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
                        "docs", "2026-07-01-hub-marketplace-research.md")

# URLs to check — mirrors the External Marketplaces table in the doc
URLS = {
    "skills.sh":               "https://skills.sh/",
    "agentskill.sh":           "https://agentskill.sh/",
    "SkillsMP":                "https://skillsmp.com/",
    "ClawHub":                 "https://clawhub.ai/",
    "skilldock.io":            "https://skilldock.io/",
    "agentskills.io":          "https://agentskills.io/",
    "agentskills.io (spec)":   "https://agentskills.io/specification",
    "agentskills.io (showcase)": "https://agentskills.io/client-showcase",
    "agentskills.io (repo)":   "https://github.com/agentskills/agentskills",
    "Hermes Atlas":            "https://hermesatlas.com/lists/top-skills",
}

def check_url(name, url):
    """Return (status_code, note) for one URL."""
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", "10", "-L", url],
            capture_output=True, text=True, timeout=15
        )
        code = r.stdout.strip()
        note = ""
        if code not in ("200", "201", "202", "204"):
            note = "DRIFT"
        return code, note
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "DRIFT"
    except Exception as e:
        return "ERROR", str(e)


print("=== Marketplace URL Re-verification ===")
print(f"{'Name':<30s} {'Status':<8s} {'Note':<10s}")
print("-" * 50)

drift_found = False
for name in sorted(URLS.keys()):
    url = URLS[name]
    code, note = check_url(name, url)
    marker = "  ← DRIFT" if note else ""
    print(f"  {name:<30s} {code:<8s} {note:<10s}{marker}")
    if note:
        drift_found = True

if drift_found:
    print("\nRESULT: Drift detected — one or more URLs returned non-200.")
    print("Update the docs/ file or investigate the URLs above.")
    sys.exit(1)
else:
    print("\nRESULT: All URLs reachable (matching doc state)")
    sys.exit(0)
