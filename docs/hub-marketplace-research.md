---
status: historical-reference
date: 2026-07-01
updated: 2026-07-15
expires: 2026-10-01
purpose: >
  Preserve the evidence and lessons from the original marketplace survey while
  clearly separating dated measurements from current discovery contracts.
---

# Hub and marketplace research snapshot

This document is a historical research record. It is not product documentation
and its counts, rankings, endpoints, client support, and install commands must be
re-verified before use.

## Snapshot history

The initial 2026-07-01 survey observed a local catalog containing 2,460 records
from seven sources. That number was accurate for that cache, but it was later
copied into README and the shipped methodology as though it described the current
ecosystem.

On 2026-07-15, a local cache generated at `2026-07-14T18:44:13Z` contained
83,772 records. This does not establish a universal catalog size; it demonstrates
why catalog totals belong in timestamped evidence rather than durable guidance.

The same rule applies to the original observations of:

- 42 client logos on an agentskills.io carousel;
- marketplace claims of 21,600 or 270,000 indexed items;
- install counts and featured rankings;
- source-share and concentration percentages;
- HTTP status observations and undocumented endpoints.

These values are retained only as examples of point-in-time evidence. Do not use
them in a recommendation without a new timestamped measurement.

## Contract changes found during re-verification

### skills.sh

The original survey used the undocumented, unauthenticated `/api/search`
endpoint. It still responded during the 2026-07-15 review, but the documented
interface is now `/api/v1/skills/search`, uses a `data` response field, requires
Vercel OIDC authentication, and documents rate limits.

Current contract source: <https://www.skills.sh/docs/api>

For local interactive use, prefer the provider CLI:

```bash
npx --yes skills find '<query>'
npx --yes skills add <owner/repository> --list
```

### GitHub code search

Unauthenticated REST code-search requests return 401. Use authenticated `gh api`,
GitHub browser search, or a web-search fallback. Do not present a plain anonymous
`curl` command as a working API path.

### Client discovery locations

The original table became stale as clients adopted native Agent Skills support.
Current sources should be checked directly:

- Codex: <https://learn.chatgpt.com/docs/build-skills>
- Claude Code: <https://code.claude.com/docs/en/skills>
- Cursor: <https://cursor.com/docs/skills>
- OpenCode: <https://opencode.ai/docs/skills>
- Gemini CLI: <https://geminicli.com/docs/cli/using-agent-skills/>
- GitHub Copilot: <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>

In particular, Codex uses `.agents/skills` for repository and user skill
discovery; Cursor supports native skills rather than requiring `.cursor/rules`;
and GitHub Copilot supports project and personal Agent Skills locations.

## Distribution state of this repository

Observed on 2026-07-15:

| Check | Result |
|---|---|
| GitHub repository parsed by `npx skills add ... --list` | One skill found |
| Exact `skills.sh` search | No matching indexed result |
| Expected skills.sh detail page | 404 |
| Local client-hub search | No CodeSigils result |
| Direct repository `.agents/skills` discovery | Present through a canonical symlink |

Therefore “installable from a GitHub source” and “discoverable in a catalog” are
separate claims. The repository should advertise only the first until a catalog
actually indexes it.

## Durable findings

The survey supports a few conclusions that remain useful without carrying its
counts forward:

1. Search local skills before remote catalogs.
2. Inspect index freshness before treating an empty result as authoritative.
3. Prefer documented provider interfaces to observed private endpoints.
4. A successful HTTP response proves reachability, not schema correctness,
   provenance, safety, or task fit.
5. Marketplace metadata is not a substitute for reading the complete candidate
   payload.
6. Installation and skill creation require separate user authorization.

Those conclusions are implemented in the shipped methodology. Volatile source
details live in supporting references and are re-verified at use time.

## Evidence maintenance

`docs/evidence-urls.json` records the network checks run by scheduled CI. The
validator distinguishes status, JSON syntax, and minimal response shape. It does
not treat URL reachability as proof that a marketplace claim is accurate.

When updating this document:

1. record the observation date and method;
2. distinguish provider claims from independently measured values;
3. update the evidence manifest when a referenced contract changes;
4. keep volatile totals out of README and the main `SKILL.md`;
5. preserve older observations as historical rows rather than silently rewriting
   what was measured.

## Re-verification log

| Date | Observation | Outcome |
|---|---|---|
| 2026-07-01 | Initial local catalog survey | 2,460 records in that cache |
| 2026-07-04 | Same cache checked again | Still 2,460; already stale |
| 2026-07-15 | Current local cache inspected | 83,772 records; static totals removed from shipped guidance |
| 2026-07-15 | skills.sh contract checked | Documented v1 API requires authentication; legacy endpoint removed from guidance |
| 2026-07-15 | Client documentation checked | Codex, Cursor, and Copilot placement claims corrected |
| 2026-07-15 | Repository discovery checked | Direct installer recognizes repository; catalogs do not yet index it |
