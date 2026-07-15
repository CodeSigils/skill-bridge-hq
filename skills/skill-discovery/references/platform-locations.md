# Platform discovery locations

These locations are a routing aid, not permanent product guarantees. Verify the
named client's current documentation before changing a user's configuration.

| Client | Project locations | User locations | Notes |
|---|---|---|---|
| Codex | `.agents/skills/<name>/SKILL.md` from the working directory through the repository root | `~/.agents/skills/<name>/SKILL.md` | Also supports admin and bundled system skills. Symlinked skill directories are supported. |
| Claude Code | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` | Keep the main file focused and move detailed material into supporting files. |
| Cursor | `.cursor/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md` | corresponding user-level locations | Skills are distinct from `.cursor/rules`. |
| OpenCode | `.opencode/skills`, `.claude/skills`, `.agents/skills` | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` | Walks project locations up to the worktree root. |
| Gemini CLI | `.gemini/skills`, `.agents/skills` | `~/.gemini/skills`, `~/.agents/skills` | Supports install and link commands with explicit scope. |
| GitHub Copilot | `.github/skills`, `.claude/skills`, `.agents/skills` | `~/.copilot/skills`, `~/.agents/skills` | `gh skill` can discover and install skills. |

For an unlisted client, inspect its documentation or runtime-provided available
skills. Do not assume that conformance to the Agent Skills file format implies a
particular filesystem path.

Sources to verify:

- Codex: <https://learn.chatgpt.com/docs/build-skills>
- Claude Code: <https://code.claude.com/docs/en/skills>
- Cursor: <https://cursor.com/docs/skills>
- OpenCode: <https://opencode.ai/docs/skills>
- Gemini CLI: <https://geminicli.com/docs/cli/using-agent-skills/>
- GitHub Copilot: <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>
