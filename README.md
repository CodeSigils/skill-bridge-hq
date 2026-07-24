# skill-discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-v1-blue)](https://agentskills.io/specification)
[![Skill](https://img.shields.io/badge/skill-discovery-purple)](skills/skill-discovery/SKILL.md)
[![CI](https://github.com/CodeSigils/skill-discovery/actions/workflows/ci.yml/badge.svg)](https://github.com/CodeSigils/skill-discovery/actions/workflows/ci.yml)

A portable workflow for finding, inspecting, and recommending agent skills.
It searches local installations and external catalogs, checks candidate safety
and compatibility, and reports what it found without installing or creating
anything unless the user explicitly asks.

**Input:** a task description and any constraints (language, framework, offline
requirement, zero-dependency, etc.). **Output:** a structured report with ranked
candidates, task-specific evidence, trust assessment (provenance, dependencies,
permissions, audits), known gaps, and next steps. Volatile external contracts
(catalog endpoints, install commands, marketplace URLs) are verified at use
time rather than cached.

This repository contains a methodology, not a static skill collection. Catalog
sizes, client support, endpoints, and install commands change frequently, so the
shipped workflow verifies volatile contracts at use time and keeps dated research
outside the core instructions.

## What it does in practice

Suppose you ask your agent:

> Find a skill for managing Docker Compose dev environments. It must work
> offline and have no Python dependency.

The workflow guides the agent to:

1. **Define the need** — extract concrete requirements (Docker Compose,
   offline-capable, zero Python dependency) and generate search terms
   (`docker`, `compose`, `containers`, `dev-environments`).
2. **Search locally** — scan installed skills across all client directories
   (`.agents/skills/`, `.claude/skills/`, `.opencode/skills/`, etc.) before
   touching anything remote. If a local match covers the need, report it
   immediately.
3. **Check freshness** — verify that catalog timestamps and version markers are
   current. A skill indexed six months ago with no release update is flagged,
   not silently trusted.
4. **Search externally** — query agentskills.io, GitHub topic search, and
   marketplace APIs. Each source is tried with documented fallbacks; no single
   outage blocks the workflow.
5. **Inspect candidates** — for each serious match, read the full payload:
   `SKILL.md`, any scripts or templates, dependency declarations, license,
   provenance, and maintenance activity.
6. **Evaluate fit** — classify each candidate:
   - **Direct fit** — meets all stated constraints.
   - **Conditional fit** — works if a minor modification is made (e.g., wrap
     the Python dependency in a container).
   - **Partial fit** — covers part of the need; supplementary skill required.
   - **Rejected** — fails a hard constraint (e.g., requires Python at runtime).
7. **Report** — return a ranked table with evidence per candidate, trust
   assessment, known gaps, and next steps. No skill is installed or created
   unless you explicitly ask.

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

## Skill payload — what ships to the user

Only the `skills/skill-discovery/` directory is the runtime payload. Everything
else is repository-only development infrastructure.

```text
skills/skill-discovery/
├── SKILL.md                        # the 7-stage discovery workflow
└── references/                     # loaded on demand, not upfront
    ├── catalog-contracts.md        # catalog interfaces and known shapes
    ├── examples.md                 # example outputs for calibration
    ├── platform-locations.md       # per-client skill directories
    ├── skill-format.md             # frontmatter spec, description quality
    └── trust-review.md             # safety and trust evaluation checklist
```

What users receive:

- A single `SKILL.md` with the complete discovery workflow;
- five reference files loaded only when the relevant stage is reached;
- no runtime scripts, configuration files, dependencies, or test fixtures;
- no agent-specific configuration or hardcoded paths in any shipped file.

Copy `skills/skill-discovery/` into your client's skill directory, as
described in Quick Start above.

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

Two scripts directories serve different purposes:

- **`scripts/`** — standalone maintainer tools runnable outside CI. Anyone can
  clone the repo and run `python3 scripts/validate-skill.py <skill-dir>` to
  validate an arbitrary skill directory. These tools auto-detect their repo
  root and have no CI-specific coupling.
- **`.github/scripts/`** — CI-internal validators and test suites. These are
  tightly coupled to this repository's structure (hardcoded paths, manifest
  loaders, test helpers) and run only in the CI pipeline.

## Evidence and validation

### Dated research

[`docs/hub-marketplace-research.md`](docs/hub-marketplace-research.md) is a
dated historical snapshot, not current product documentation. Its measurements
must not be copied into recommendations without re-verification.

### CI pipeline

CI performs payload and documentation checks on pushes and pull requests.
External URL monitoring runs on a schedule or manually so transient third-party
outages do not make ordinary documentation changes flaky.

### Catalog status

The repository is directly installable by compatible GitHub skill installers,
but it is not yet indexed by skills.sh or the Hermes hub. "Installable" and
"discoverable in a catalog" are intentionally reported as separate states.

## Security

Discovery results are untrusted input. Read [`SECURITY.md`](SECURITY.md) and the
skill's trust-review reference before installing or running third-party content.

## License

MIT — see [LICENSE](LICENSE).
