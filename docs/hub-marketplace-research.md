---
status: reference
date: 2026-07-01
updated: 2026-07-04
expires: 2026-10-01
purpose: >
  Reference map of the agent-skill ecosystem as of mid-2026 — hub indexes,
  external marketplaces, client platforms, ecosystem directories, and open
  questions. A raw evidence snapshot for anyone researching how agent skills
  are indexed, discovered, and distributed.
---

# Hub & Marketplace Catalog Research

> **Warning:** This is a point-in-time research snapshot (2026-07-01).
> URLs drift, indexes age, marketplaces change. Every source below records
> its verification timestamp and method so you can assess freshness.
> Treat all findings as hypotheses, not truths, until re-verified.

---

## 1. The Landscape

### 1.1 Hermes Built-in Hub (local cache)

The Hermes agent ships with a pre-populated hub index — no network calls
needed for a local search.

| Field | Value | Source |
|-------|-------|--------|
| Index format | JSON (`version`, `generated_at`, `skill_count`, `skills`) | `~/.hermes/skills/.hub/index-cache/hermes-index.json` |
| Index age | 2026-05-26 — stale (~5 weeks at time of research) | `generated_at` field |
| Total indexed | 2,460 skills | Live cache count |

**Source breakdown of the 2,460 indexed skills:**

| Source | Skills | Share | Trust tier | Notes |
|--------|--------|-------|------------|-------|
| skills.sh | 1,218 | 49.5% | Community | Primary public leaderboard. Powers the featured cache. Install via `npx skills add` |
| lobehub | 500 | 20.3% | Community | LobeChat skill catalog |
| browse-sh | 330 | 13.4% | Community | Browser-level skill collection |
| clawhub | 200 | 8.1% | Evaluate | OpenClaw marketplace — source quality not yet confirmed |
| github | 127 | 5.2% | High | Community repos, fully transparent |
| official | 84 | 3.4% | Highest | Hermes-bundled, maintained |
| claude-marketplace | 1 | <0.1% | High | A single entry |
| **Total** | **2,460** | **100%** | | |

**Metadata available per skill:**

```text
All sources:  name, description, identifier, source, repo, path, tags,
              extra, trust_level
skills.sh:    + resolved_github_id
```

**Featured skills cache:** 100 curated skills from major vendors (Anthropic,
Microsoft Azure, Vercel, Remotion) stored in `skills_sh_featured.json`. All
sourced from skills.sh.

**Key structural note:** The hub catalog is an **index, not an install**.
Most of the 2,460 entries exist only as metadata. A hub search finds
entries, but physically loading a skill requires it to be installed
separately (either via the hub's install mechanism or direct filesystem
placement). This means search hit count does not equal available tools.

#### 1.1.1 Concentration Risk

Three sources account for 83.2% of the index: skills.sh (49.5%), lobehub
(20.3%), and browse-sh (13.4%). This means the hub's breadth depends heavily
on skills.sh staying healthy and indexed. If skills.sh changes its format or
goes offline, nearly half the index becomes metadata-only with no resolution
path.

---

### 1.2 External Marketplaces

All URLs verified with `curl -s -o /dev/null -w "%{http_code}"` at the
timestamp shown. These are live external services — verify reachability
before depending on any of them.

| Marketplace | URL | HTTP status | Role | Notes |
|-------------|-----|-------------|------|-------|
| skills.sh | https://skills.sh/ | 200 | Primary public leaderboard | All-time leaderboard, per-skill pages. Installed via `npx skills add`. 1,218 entries in the Hermes hub index. |
| agentskill.sh | https://agentskill.sh/ | 200 | Cross-platform marketplace | Role/platform filtering, quality scores, security audits. Large catalog. |
| SkillsMP | https://skillsmp.com/ | 200 | Broad aggregator | Occupation and category maps. Claims 270K+ indexed SKILL.md files. |
| ClawHub | https://clawhub.ai/ | 200 | OpenClaw skills/plugins marketplace | 200 entries in hub index. Source quality should be evaluated before use. |
| skilldock.io | https://skilldock.io/ | 200 | Versioned skill registry | Publish/install workflow. V1 had 10+ repos / 20+ skills. V2 in development. |
| agentskills.io | https://agentskills.io/ | 200 (spec page) | Open specification standard | [![stars](https://img.shields.io/github/stars/agentskills/agentskills)](https://github.com/agentskills/agentskills/stargazers) — GitHub repo. Client Showcase was 404 at ~02:00 UTC, returned 200 by ~06:24 UTC same day — drift confirmed within hours. Re-verified 404 on 2026-07-01 (later session). |

#### 1.2.1 Discovered: agentskills.io Client Showcase Drift

At approximately 02:00 UTC on 2026-07-01, the agentskills.io Client Showcase
page returned HTTP 404. By approximately 06:24 UTC the same day, it returned
HTTP 200. The root cause is unknown — page moved, server flake, or routing
issue. This was the research team's first encounter with ecosystem URL drift
in real time: between two research sessions on the same day, a source URL
changed behaviour and then self-recovered.

**Update (same day, later session):** The page is 404 again. The earlier
200 appears to have been a temporary recovery, not a permanent fix. As of
this writing the page is persistently unavailable, reinforcing the conclusion
that external URLs must be verified at query time, not recorded once and
trusted.

---

### 1.3 agentskills.io Client Ecosystem

Live count from the home page carousel (deduplicated): **42 client platforms**
as of 2026-07-01.

| Client | Category | URL |
|--------|----------|-----|
| Claude Code | IDE agent | claude.ai/code |
| OpenAI Codex | CLI agent | developers.openai.com/codex |
| Gemini CLI | CLI agent | geminicli.com |
| GitHub Copilot | IDE plugin | github.com |
| Cursor | IDE | cursor.com |
| VS Code | IDE | code.visualstudio.com |
| Junie | IDE agent | junie.jetbrains.com |
| OpenCode | CLI agent | opencode.ai |
| Roo Code | CLI agent | roocode.com |
| TRAE | IDE agent | trae.ai |
| Goose | CLI agent | block.github.io/goose |
| OpenHands | CLI agent | openhands.dev |
| Claude | Web agent | claude.ai |
| Spring AI | Framework | docs.spring.io/spring-ai |
| Snowflake Cortex Code | Data platform | docs.snowflake.com |
| Google AI Edge Gallery | Edge AI | github.com/google-ai-edge/gallery |
| Fast Agent | Framework | fast-agent.ai |
| Letta | Memory framework | letta.com |
| Mistral AI Vibe | CLI agent | github.com/mistralai/mistral-vibe |
| Laravel Boost | Framework | github.com/laravel/boost |
| Tabnine | IDE plugin | tabnine.com |
| Factory | AI worker | factory.ai |
| Workshop | Platform | workshop.ai |
| Qodo | Testing | qodo.ai |
| VS Code Extensions (VT Code, Amp, bub, etc.) | IDE extensions | — |
| **... and 18 more** | | |

**Notable observation:** Hermes Agent was NOT listed on the carousel at
time of research, despite being an agentskills.io-compatible client (it
loads skills from `skills/*/SKILL.md`). Whether this is intentional,
an oversight, or a stale carousel is unknown.

---

### 1.4 Ecosystem Directories

| Directory | URL | What it contains | Machine-parseable? |
|-----------|-----|------------------|--------------------|
| Hermes Atlas | hermesatlas.com | 178+ repos across 12 categories, weekly star velocity | GitHub stars, descriptions, categories — but not file trees, skill counts, or reference ratios |
| agentskills.io repo | github.com/agentskills/agentskills | Specification, tools, reference implementation | README only |
| awesome-copilot | github.com/github/awesome-copilot | Community-curated Copilot resources ([![stars](https://img.shields.io/github/stars/github/awesome-copilot)](https://github.com/github/awesome-copilot/stargazers)) | Links + categories — not programmatically parseable |
| anthropics/claude-plugins-official | github.com/anthropics/claude-plugins-official | 37 plugins, 29+ SKILL.md files | Full repo tree (git-cloneable) |
| openai/skills | github.com/openai/skills | Official Codex skill catalog | Full repo tree (git-cloneable) |

---

### 1.5 Platform-Vendor Skill Repos

These are individual repositories that ship SKILL.md files — the
"leaf nodes" of the ecosystem. The list is not exhaustive; it represents
repos that appeared in hub index data and marketplace scans.

| Repo | Stars | Skills | Format | Discovery mechanism |
|------|-------|--------|--------|--------------------|
| addyosmani/agent-skills | [![stars](https://img.shields.io/github/stars/addyosmani/agent-skills)](https://github.com/addyosmani/agent-skills/stargazers) | 24 | Flat SKILL.md, no YAML frontmatter | README-based browsing |
| anthropics/claude-plugins-official | [![stars](https://img.shields.io/github/stars/anthropics/claude-plugins-official)](https://github.com/anthropics/claude-plugins-official/stargazers) | 37 plugins, 29+ SKILL.md | agentskills.io + extensions | `.claude-plugin/` directory |
| openai/skills | — | ~20 | agentskills.io | `$skill-installer` CLI |
| wondelai/skills | [![stars](https://img.shields.io/github/stars/wondelai/skills)](https://github.com/wondelai/skills/stargazers) | 50 | agentskills.io (book-philosophy format) | Flat root directory |
| vercel-labs/skills | — | Featured on skills.sh | agentskills.io | `npx skills` |
| microsoft/azure-skills | — | Featured on skills.sh | agentskills.io | Featured cache in hub |

---

## 2. Discovery Layers — What Happens at Each Level

The agent-skill ecosystem operates across three distinct layers.
Understanding the separation helps diagnose why certain searches succeed
or fail.

### Layer A: Agent-Side Retrieval (what the runtime provides)

Each platform has its own mechanism for loading skills into a session:

| Platform | Retrieval mechanism |
|----------|---------------------|
| Hermes | `hermes skills search`, `skill_view()`, `skills.external_dirs`, hub cache |
| Claude Code | Directory walk `.claude/skills/`, plugin.json, skillOverrides config |
| Codex CLI | Directory walk `.codex/skills/`, `$skill-installer` |
| Gemini CLI | `gemini skills list`, `gemini skills install`, directory walk |
| Cursor | `.cursor/rules/` — no search, just glob match on file name |

These mechanisms are platform-specific and not interchangeable. A skill
placed in `.claude/skills/` is invisible to Codex CLI, and vice versa.

### Layer B: Catalog Research (what the agent does to find skills)

Three sub-methods exist, typically used as a fallback chain:

- **Catalog search** — keyword + tag + source filter against a hub index
  (fastest, but index is stale)
- **Marketplace scan** — fallback chain through external marketplaces
  (broader, but URLs drift)
- **GitHub deep search** — direct repo inspection when catalogs miss
  (most current, but slowest and requires network)

### Layer C: Publishing / Registration (how skills become discoverable)

Getting a skill into the findable pool involves different channels per
platform:

| Channel | Platforms served | Access |
|---------|-----------------|--------|
| `hermes skills publish` | Hermes | Hermes-specific CLI |
| `external_dirs` config | Hermes | Config file entry |
| skills.sh auto-indexing | Hermes, generic | Automatic from GitHub activity |
| agentskill.sh submission | Multi-platform | Manual submission form |
| Hermes Atlas registration | Hermes ecosystem | GitHub issue |
| Claude Code plugin.json | Claude Code | Platform-specific manifest |

---

## 3. Sources

Every source was accessed and verified on 2026-07-01. The "Method" column
documents how the data was collected so you can reproduce or update it.

| Source | URL / Path | Method | Finding | Verified |
|--------|------------|--------|---------|----------|
| Hermes hub index (local cache) | `~/.hermes/skills/.hub/index-cache/hermes-index.json` | Live cache read | 2,460 skills, 7 sources, index dated 2026-05-26 | 2026-07-01 |
| Hermes hub featured cache | `~/.hermes/skills/.hub/index-cache/skills_sh_featured.json` | Live cache read | 100 featured skills from skills.sh | 2026-07-01 |
| Hermes installed skills | `hermes skills list` | CLI command | ~240 installed, mix of builtin/local/skills.sh | 2026-07-01 |
| agentskills.io overview | https://agentskills.io/home | Browser | 42 client logos visible on home page carousel | 2026-07-01 |
| agentskills.io spec | https://agentskills.io/specification | Browser | `name` + `description` required; optional `ref`, `scripts`, `assets` | 2026-07-01 |
| agentskills.io client-showcase | https://agentskills.io/client-showcase | Browser | **404 at ~02:00 UTC; 200 by ~06:24 UTC same day** | 2026-07-01 |
| agentskills.io repo | https://github.com/agentskills/agentskills | Browser | [![stars](https://img.shields.io/github/stars/agentskills/agentskills)](https://github.com/agentskills/agentskills/stargazers) (observed on page) | 2026-07-01 |
| Hermes Atlas top skills | https://hermesatlas.com/lists/top-skills | Browser | 18 ranked entries with star counts (73.1K, 23.2K, 4.9K etc.) | 2026-07-01 |
| skills.sh | https://skills.sh/ | HTTP 200 | Primary public leaderboard | 2026-07-01 |
| agentskill.sh | https://agentskill.sh/ | HTTP 200 | Broad marketplace with quality scores | 2026-07-01 |
| SkillsMP | https://skillsmp.com/ | HTTP 200 | Aggregator claiming 270K+ SKILL.md files | 2026-07-01 |
| ClawHub | https://clawhub.ai/ | HTTP 200 | OpenClaw marketplace | 2026-07-01 |
| skilldock.io | https://skilldock.io/ | HTTP 200 | Versioned skill registry; V2 in development | 2026-07-01 |

---

## 4. Open Questions

These questions were identified during research and remain unanswered.
They represent the gap between what is known and what would be useful to
know about the ecosystem.

| # | Question | Current evidence | Would benefit from |
|---|----------|-----------------|--------------------|
| 1 | How often does the Hermes hub index auto-refresh? | Index dated 2026-05-26. Pull-based or push-based unknown. | Source code audit of `hermes_cli/skills_hub.py` or config grep for sync/refresh patterns. |
| 2 | Is there a CLI command to force-refresh the hub index? | Not documented in `hermes skills list` or `hermes skills search`. | `hermes help` / `hermes skills --help` review. |
| 3 | Which agentskills.io clients support optional SKILL.md features (scripts, references)? | Spec marks them as optional; per-platform implementation unknown. | Per-platform testing or documentation review. |
| 4 | What are the root-level skill repo directory patterns for the top-20 Atlas repos? | Only 7 repos measured; 20 would give statistical confidence. | GitHub API tree queries for each repo (non-mutating). |
| 5 | How many total unique agent skills exist across all marketplaces? | Upper bound unknown. SkillsMP claims 270K+ SKILL.md files but no deduplication methodology is published. | Cross-marketplace deduplication study. |

---

## 5. Key Findings

All findings are based on live-verified data from 2026-07-01.

### 5.1 The Hub Index Provides Breadth but Not Depth

- **2,460 skills indexed** from 7 sources. The hub is useful as a starting
  point but most entries (91%) are community-contributed; only 3.4% are
  officially maintained.
- **Hub index is ~6 weeks stale** (last generated 2026-05-26). New skills
  published since 2026-05-26 are invisible to hub searches.
  A freshness check should precede any hub-dependent search.

### 5.2 The Ecosystem Has a Single-Source Risk

- **skills.sh dominates**: 49.5% of the hub index. Combined with lobehub
  (20.3%) and browse-sh (13.4%), three sources make up 83.2% of all indexed
  skills. If any of these changes format or availability, coverage drops
  sharply.
- **ClawHub (8.1%) has untrusted quality.** Its 200 entries are in the
  index but marked "Evaluate" — no quality guarantee.

### 5.3 agentskills.io Adoption Is Real but Hard to Count

- **42 client platforms** confirmed via the home page carousel. The standard
  is broadly adopted across IDE agents, CLI agents, frameworks, and data
  platforms.
- **Hermes Agent is not listed** on the carousel despite being a compatible
  client. The showcase may be incomplete or voluntary.
- **The Client Showcase page was 404 at ~02:00 UTC, recovered to 200 by**
  **~06:24 UTC, then returned to 404.** It was re-verified 404 again in a
  later session the same day. The recovery was temporary. This concretely
  demonstrates that URL reachability can change between research sessions
  — and that a single recovery does not mean permanent availability.
  Any study of the ecosystem must verify URLs at the time of use, not
  rely on a one-time snapshot.

### 5.4 External Marketplaces Are Reachable but Uneven

All 6 marketplaces verified returned HTTP 200 on 2026-07-01. However:

- **SkillsMP claims 270K+ SKILL.md files** — this is an order of magnitude
  larger than the hub index. If accurate, the hub is indexing <1% of
  available skills. The claim could not be independently verified.
- **skilldock.io** is the only versioned registry with a publish/install
  workflow. Its V2 status means its current shape is transitional.

### 5.5 The agentskills.io Spec Is Minimal

The open standard requires only `name` and `description` in YAML frontmatter.
Optional fields (`ref`, `scripts`, `assets`) exist but have unknown adoption
rates across the 42 clients. This minimal surface is both a strength
(low barrier to entry) and a weakness (no standard way to declare
dependencies, version constraints, or installation requirements).

---

## 6. Research Methodology

### Data Collection

- Hub index data: local cache read from `~/.hermes/skills/.hub/index-cache/`
- Marketplace status: `curl -s -o /dev/null -w "%{http_code}" <url>`
- Client ecosystem: manual browser inspection of agentskills.io home page carousel, deduplicated by logo
- Platform repos: GitHub API and manual repo inspection
- All timestamps are UTC

### Known Limitations

- The 42-client count is from a home page carousel — logos that were not
  rendered (scroll depth) may have been missed.
- Marketplace HTTP status is a liveness check only, not a content-quality
  assessment. A 200 means the server responded, not that the content is
  accurate or well-maintained.
- Skill counts (2,460 indexed, 240 installed, 100 featured) are from a
  single Hermes agent instance. Other agents may have different index
  snapshots depending on when they last synced.
- "270K+ SKILL.md files" from SkillsMP is the marketplace's own claim.
  No independent verification was performed.

### Drift Register

Re-verification events recorded after the initial 2026-07-01 snapshot:

| Date | Item | Previous value | Current value | Delta |
|------|------|----------------|---------------|-------|
| 2026-07-01 | agentskills.io/client-showcase | 200 at 06:24 UTC | 404 | Reverted to original broken state |
| 2026-07-01 | addyosmani/agent-skills stars | 68K | 68,290 | +290 (still rounds to ~68K) |
| 2026-07-01 | anthropics/claude-plugins-official stars | 31.3K | 31,374 | +74 (rounded to ~31K) |
| 2026-07-01 | agentskills/agentskills stars | 21,302 | 21,322 | +20 |
| 2026-07-01 | skills.sh | 200 (direct) | 308 (redirect → 200) | Redirect applied; still reachable |
| 2026-07-01 | agentskills.io (home) | 200 | 200 | Stable |
| 2026-07-01 | agentskills.io/specification | 200 | 200 | Stable |
| 2026-07-01 | agentskill.sh | 200 | 200 | Stable |
| 2026-07-01 | skillsmp.com | 200 | 200 | Stable |
| 2026-07-01 | clawhub.ai | 200 | 200 | Stable |
| 2026-07-01 | skilldock.io | 200 | 200 | Stable |
| 2026-07-04 | addyosmani/agent-skills stars | 68,290 (drift register) | 68,878 | +588 (now ~69K) |
| 2026-07-04 | anthropics/claude-plugins-official stars | 31,374 (drift register) | 31,532 | +158 (still ~31K) |
| 2026-07-04 | agentskills/agentskills stars | 21,322 (drift register) | 22,195 | +873 (now ~22K) |
| 2026-07-04 | awesome-copilot stars | ~35.9K | 36,160 | +~260 (now ~36K) |
| 2026-07-04 | hub index age | 5 weeks stale | ~6 weeks stale | Index not refreshed since 2026-05-26 |
| 2026-07-04 | Hub catalog scan count | 2,460 | 2,460 | Index unchanged; still accurate |

