# skill-bridge-hq — Agent Context

## What this repo is

A portable **skill-discovery methodology** for any agentskills.io-compatible agent. It teaches agents how to find the best skill for a task by scanning catalogs, marketplaces, and GitHub.

This is a **methodology**, not a skill collection. The single skill is under `skills/skill-discovery/`.

## Files to know

| Path | Purpose |
|------|---------|
| `skills/skill-discovery/SKILL.md` | The methodology — load this skill |
| `.agents/skills/skill-discovery` | Symlink for agents that scan `.agents/skills/` |
| `.github/scripts/ci-check.py` | CI: catches Hermes-specific references |
| `.github/workflows/ci.yml` | GitHub Actions: runs ci-check.py on push/PR to main |

## Quick start

To make the methodology available, point your agent at `skills/skill-discovery/`:

- **Hermes:** add to `skills.external_dirs` in config.yaml
- **Claude Code:** `cp -r skills/skill-discovery .claude/skills/`
- **Gemini CLI:** `cp -r skills/skill-discovery .agents/skills/`
- **Generic agentskills.io client:** copy to your skills directory

## Design principles

- Zero platform adapter files — `skills/*/SKILL.md` is the canonical format
- Zero reference files — inline everything as code blocks
- The methodology is self-verifying — it teaches agents to check source freshness at runtime
