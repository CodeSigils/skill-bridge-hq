#!/usr/bin/env python3
"""Check for Hermes-specific references in portable skills.

This is the only CI check this repo needs. It catches the one thing no
agent runtime validates: cross-agent portability. A stray `skill_view()` call
makes the methodology useless on non-Hermes agents.

Patterns checked:
  - skill_view, skill_manage (Hermes-specific tool names)
  - ~/.hermes/ (Hermes config path)
"""

import subprocess
import sys

result = subprocess.run(
    ["grep", "-rnP", r"(?i)(skill_view|skill_manage|~/\.hermes)", "skills/"],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("FAIL: Hermes-specific references found in skills/:")
    print(result.stdout)
    sys.exit(1)

print("PASS: No Hermes-specific references in skills/")
