# skill-discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-v1-blue)](https://agentskills.io/specification)
[![Skill](https://img.shields.io/badge/skill-discovery-purple)](skills/skill-discovery/SKILL.md)
[![CI](https://github.com/CodeSigils/skill-discovery/workflows/validate/badge.svg)](https://github.com/CodeSigils/skill-discovery/actions)

**A portable discovery methodology for agent skills.** This repo teaches
any agentskills.io-compatible agent how to find the best skill for a task
-- scanning catalogs, marketplaces, and GitHub; evaluating candidates; and
recommending the best match.

> This is a **methodology**, not a skill collection. It teaches agents
> how to find skills. The hub already has 2,460 indexed skills -- a static
> collection adds nothing next to that.

---

## Quick Start

Clone this repo and tell your agent to load `skill-discovery`:

```bash
git clone --filter=blob:none https://github.com/CodeSigils/skill-discovery
```

Then make the skill discoverable. Choose your platform:

<details>
<summary><b>Hermes Agent</b></summary>

**Recommended:** Add the repo path to `skills.external_dirs` in
`~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - /path/to/skill-discovery/skills/skill-discovery
```

This makes skill changes visible without reinstalling and survives
Hermes upgrades.

**Alternative:** Copy the skill directly:

```bash
cp -r skill-discovery/skills/skill-discovery ~/.hermes/skills/
```
</details>

<details>
<summary><b>Claude Code (Anthropic)</b></summary>

```bash
cp -r skill-discovery/skills/skill-discovery .claude/skills/
```

Claude Code discovers skills by scanning `.claude/skills/` for
`SKILL.md` files.
</details>

<details>
<summary><b>Codex CLI (OpenAI)</b></summary>

```bash
cp -r skill-discovery/skills/skill-discovery .codex/skills/
```

Codex CLI discovers skills in `.codex/skills/` via filesystem walk.
</details>

<details>
<summary><b>OpenCode CLI</b></summary>

```bash
cp -r skill-discovery/skills/skill-discovery .opencode/skills/
```

Or create a symlink (zero-maintenance pointer):

```bash
ln -s /path/to/skill-discovery/skills/skill-discovery .opencode/skills/
```
</details>

<details>
<summary><b>Cursor</b></summary>

Cursor uses `.cursor/rules/` for skill-like content:

```bash
cp -r skill-discovery/skills/skill-discovery .cursor/rules/
```

Note: Cursor applies rules as chat context, not via
invocation-based discovery like CLI-focused agents.
</details>

<details>
<summary><b>GitHub Copilot</b></summary>

Copilot uses a plugin marketplace model rather than filesystem-based
skill discovery. For platform-native skills, search the
[awesome-copilot](https://github.com/topics/awesome-copilot) ecosystem.

The methodology's content can be adapted as a Copilot extension,
but direct SKILL.md loading is not natively supported.
</details>

<details>
<summary><b>Gemini CLI (Google)</b></summary>

```bash
cp -r skill-discovery/skills/skill-discovery .agents/skills/
```

Gemini CLI explicitly supports `.agents/skills/` as a cross-tool path.
</details>

<details>
<summary><b>Generic agentskills.io client</b></summary>

Copy the skill to your agent's configured skills directory. Most
clients that support the agentskills.io standard scan a `skills/`
or `.agents/skills/` directory.

```bash
cp -r skill-discovery/skills/skill-discovery <your-skills-dir>/
```
</details>

The repo also ships a `skill-discovery` symlink under `.agents/skills/`
for clients that auto-scan that path. If your agent reads
`.agents/skills/`, discovery is automatic after clone.

---

## What This Repo Contains

```
skill-discovery/
├── README.md                               # you are here
├── SECURITY.md                             # vulnerability reporting
├── LICENSE                                 # MIT
├── .gitignore
├── docs/
│   └── 2026-07-01-hub-marketplace-research.md  # evidence base
├── skills/
│   └── skill-discovery/
│       └── SKILL.md                        # the methodology (~460 lines)
├── .agents/
│   └── skills/
│       └── skill-discovery -> ../../skills/skill-discovery/  # symlink
└── .github/
    ├── workflows/ci.yml                    # checkout → Hermes-refs check
    └── scripts/ci-check.py                 # single grep call
```

**9 files.** One skill. One CI check. Zero platform adapter files.

---

## What This Repo Does NOT Include

| Excluded | Reason |
|----------|--------|
| Static skill collection | The hub already has 2,460 indexed skills — a collection adds nothing next to that number. |
| Install scripts | Every platform provides native skill consumption paths. A script would compete and drift. |
| Platform adapter files (`.claude/`, `.cursor/`, `.codex/` etc.) | User-side setup only. The repo ships only `skills/*/SKILL.md` and a single cross-tool symlink. |
| index.json or plugin.json | No marketplace distribution. Filesystem discovery is sufficient at 1 skill. |
| Hermes-specific references | Any `skill_view()` or `hermes` CLI reference would silently break on non-Hermes agents. CI catches this. |
| Development artifacts (ADRs, review pipeline, architecture docs) | These stay in the source repo. This repo ships only the shipping surface. |

---

## What the Methodology Teaches

When invoked, `skill-discovery` guides any agent through:

1. **Freshness check** -- verify the catalog is up to date before searching
2. **Keyword search** -- match tasks to skills by name, description, and tags
3. **Source filtering** -- prefer official over community sources
4. **Featured/curated source search** -- when keyword search is thin
5. **External marketplace scan** -- fallback through marketplaces and GitHub
6. **Evaluation rubric** -- systematically assess each candidate
7. **Skill creation fallback** -- build a minimal skill when nothing matches

The methodology is self-verifying -- it teaches agents to check
source reachability at runtime rather than relying on hardcoded
URLs that drift.

---

## Evidence Base

This methodology was formed from live research on 2026-07-01. Key findings:

- **2,460 skills** indexed in the Hermes hub from 7 sources
- **42 clients** confirmed on agentskills.io (home page carousel)
- **6 external marketplaces** verified reachable
- **agentskills.io Client Showcase: 404 at ~02:00 UTC, recovered to 200 by ~06:24 UTC, reverted to 404 later same day** -- drift confirmed within hours
- **Hub index: 5 weeks stale** -- freshness check essential
- **Concentration risk:** 83.2% of the index comes from 3 sources (skills.sh, lobehub, browse-sh)
- **Open questions:** 5 documented unknowns (refresh cadence, CLI force-refresh, optional-feature support, top-20 repo patterns, total deduplicated count)

The full research snapshot lives in [`docs/2026-07-01-hub-marketplace-research.md`](docs/2026-07-01-hub-marketplace-research.md)
and includes a **Drift Register** tracking which claims have been re-verified since publication.

> `docs/` is a repo-only artifact -- it provides provenance and audit trail but does
> not ship with any skill installation. The shipped methodology (`skills/skill-discovery/SKILL.md`)
> is self-contained and agent-agnostic.

---

## License

MIT -- see LICENSE.
