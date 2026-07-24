# skill-discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-v1-blue)](https://agentskills.io/specification)
[![Skill](https://img.shields.io/badge/skill-discovery-purple)](skills/skill-discovery/SKILL.md)
[![CI](https://github.com/CodeSigils/skill-discovery/actions/workflows/ci.yml/badge.svg)](https://github.com/CodeSigils/skill-discovery/actions/workflows/ci.yml)

A portable workflow for finding, inspecting, and recommending agent skills.
It searches local installations and external catalogs, checks candidate safety
and compatibility, and reports what it found without installing or creating
anything unless the user explicitly asks.

This repository contains a methodology, not a static skill collection. Catalog
sizes, client support, endpoints, and install commands change frequently, so the
shipped workflow verifies volatile contracts at use time and keeps dated research
outside the core instructions.

## Quick start

Clone the repository:

```bash
git clone --filter=blob:none https://github.com/CodeSigils/skill-discovery
```

The clone exposes the skill at `.agents/skills/skill-discovery`, a symlink to the
canonical `skills/skill-discovery` directory. Codex, Cursor, Gemini CLI, OpenCode,
and GitHub Copilot support `.agents/skills` as a project location. Launch the
client from this repository or copy the canonical directory into the appropriate
project or user-level location.

| Client | Project location | Notes |
|---|---|---|
| Codex | `.agents/skills/skill-discovery` | Scans from the working directory to the repository root. |
| Claude Code | `.claude/skills/skill-discovery` | Native Agent Skills support. |
| Cursor | `.agents/skills/skill-discovery` or `.cursor/skills/skill-discovery` | Native Agent Skills support; do not place the skill under `.cursor/rules`. |
| OpenCode | `.agents/skills/skill-discovery` or `.opencode/skills/skill-discovery` | Also supports Claude-compatible locations. |
| Gemini CLI | `.agents/skills/skill-discovery` or `.gemini/skills/skill-discovery` | Supports project and user scopes. |
| GitHub Copilot | `.agents/skills/skill-discovery` or `.github/skills/skill-discovery` | Also supports `.claude/skills` and personal skill directories. |

For a generic Agent Skills client:

```bash
cp -R skill-discovery/skills/skill-discovery <client-skill-directory>/
```

### Hermes Agent

For local development, point Hermes at the repository's canonical skills
directory:

```yaml
skills:
  external_dirs:
    - /path/to/skill-discovery/skills
```

The repository is not currently indexed in the Hermes hub, so no hub-install
command is advertised. Clone plus `external_dirs` is the verified Hermes path
until registration. Review the skill before enabling it; catalog registration is
a later distribution step, not a prerequisite for local use.

## Repository layout

```text
skill-discovery/
├── README.md
├── SECURITY.md
├── docs/                              # dated research and evidence manifest
├── scripts/                           # standalone validators (validate-skill.py)
├── skills/skill-discovery/
│   ├── SKILL.md                       # focused discovery workflow
│   └── references/                    # loaded only when relevant
├── .agents/skills/skill-discovery     # symlink to the canonical skill
└── .github/
    ├── scripts/                       # CI-only validators and test suite
    └── workflows/ci.yml
```

The canonical payload is `skills/skill-discovery/`. The `.agents` entry is only
a zero-copy discovery adapter; changes belong in the canonical directory.

## What the methodology teaches

1. Search installed and repository-local skills first.
2. Expand task keywords and inspect all relevant directory depths.
3. Search documented catalog interfaces, then authenticated source search and
   browser/web fallbacks.
4. Read the complete candidate payload and evaluate provenance, behavior,
   dependencies, permissions, freshness, compatibility, and task fit.
5. Recommend candidates with evidence and disclosed gaps.
6. Ask before installing a candidate or creating a replacement skill.

## Evidence and validation

[`docs/hub-marketplace-research.md`](docs/hub-marketplace-research.md) is a
dated historical snapshot, not current product documentation. Its measurements
must not be copied into recommendations without re-verification.

CI performs deterministic payload and documentation checks on pushes and pull
requests. External URL monitoring runs on a schedule or manually so transient
third-party outages do not make ordinary documentation changes flaky.

The repository is directly installable by compatible GitHub skill installers,
but it is not yet indexed by skills.sh or the Hermes hub. “Installable” and
“discoverable in a catalog” are intentionally reported as separate states.

## Security

Discovery results are untrusted input. Read [`SECURITY.md`](SECURITY.md) and the
skill's trust-review reference before installing or running third-party content.

## License

MIT — see [LICENSE](LICENSE).
