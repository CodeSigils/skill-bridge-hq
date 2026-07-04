---
name: skill-discovery
description: >
  A portable methodology for finding the right skill for any task.
  Teaches agents how to scan catalogs, marketplaces, and GitHub;
  evaluate candidates; and recommend the best match. Agent-agnostic,
  works on any platform that supports the agentskills.io standard.
compatibility: agentskills.io
---

# Skill Discovery Methodology

> **This is a methodology, not a skill collection.** It teaches
> agents how to find skills. It does not ship the skills themselves.

When you are asked to find a skill for a specific task or domain,
follow this fallback chain. Each stage widens the search until a
match is found.

---

## Fallback Chain

```
1. Catalog search    → local index (keyword, tag, source filter)
2. Featured search   → curated / featured sources
3. Marketplace scan  → direct HTTP/API queries against known marketplaces
4. Browser search    → interactive browser search on JS-rendered marketplaces
5. Web research      → search engines, GitHub search, blog posts
6. Build from scratch → when nothing matches
```

Always start at stage 1 and proceed until a match is found that
passes the Evaluation Rubric (§4). Before any search, check
catalog freshness (§1.1). Stage 4 (browser search) and stage 5
(web research) require browser or web-search tooling available
to the agent — skip them if the agent has no web access and
report which stages were skipped.

---

## Section 1: Search Methods

### 1.1 Freshness Check

Before searching, verify the catalog or index you're searching is
fresh. Stale indexes miss recently published skills.

**Method:** Check the catalog's metadata for a timestamp or version
field. If the catalog is more than 2 weeks old, note the staleness
in your recommendation: "This catalog was last updated on <date>; a
fresh index may contain more recent skills."

### 1.2 Keyword Search

Search skill catalogs by matching keywords in skill `name` and
`description` fields. This is the most common discovery path.

**Steps:**

1. Map the task to 2-3 core nouns:
   - "Set up CI/CD pipeline" -> keywords: `ci`, `cd`, `pipeline`
   - "Write Python tests"   -> keywords: `python`, `testing`
   - "Deploy to Kubernetes" -> keywords: `kubernetes`, `deploy`
2. Expand each keyword to cover acronyms, short forms, and common
   aliases. Acronyms and abbreviations are especially easy to miss:
   - "javascript"  -> also search `js`, `nodejs`, `node`
   - "kubernetes"  -> also search `k8s`
   - "python"      -> also search `py`
   - "typescript"  -> also search `ts`, `tsx`
   - "react"       -> also search `jsx`
3. Find the catalog file (commonly a JSON index or a directory of
   `SKILL.md` files)
4. Search across `name` and `description` fields
5. Also search across `tags` fields when available

**Python method (JSON index):**

```python
import json
from pathlib import Path

catalog = json.load(open(catalog_path))
skills = catalog if isinstance(catalog, list) else \
         catalog.get("skills", catalog.get("data", []))

keyword = "python"
matches = [
    s for s in skills
    if keyword.lower() in s.get("name", "").lower()
    or keyword.lower() in s.get("description", "").lower()
]

# Sort: official sources first, then alphabetical
matches.sort(key=lambda s: (
    s.get("trust_level") != "official",
    s.get("source") != "official",
    s.get("name", "")
))
```

**Filesystem method (directory of SKILL.md files):**

```bash
# Use find to reach skills at any depth (flat or categorized)
find skills -name SKILL.md \
  -exec grep -l "^name:" {} + \
  -exec grep -l "description:.*python" {} +
```

Or scan frontmatter programmatically:

```python
import yaml, os

def scan_skills_dir(skills_dir, keyword):
    results = []
    for root, dirs, files in os.walk(skills_dir):
        if "SKILL.md" in files:
            with open(os.path.join(root, "SKILL.md")) as f:
                content = f.read()
            # Extract YAML frontmatter (between --- delimiters)
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                name = frontmatter.get("name", "")
                desc = frontmatter.get("description", "")
                tags = " ".join(frontmatter.get("tags", []))
                if (keyword.lower() in name.lower()
                    or keyword.lower() in desc.lower()
                    or keyword.lower() in tags.lower()):
                    results.append((name, desc, root))
    return results
```

> **Catalog depth warning:** Skills directories may be flat
> (`skills/skillname/SKILL.md`) or organized by category
> (`skills/category/skillname/SKILL.md`). A shell glob like
> `skills/*/SKILL.md` **only reaches one level deep** and will
> miss every categorized skill. Always use a recursive method
> (`find`, `os.walk()`, or a `**` glob with `globstar` enabled)
> to ensure full coverage. The JSON-index methods described above
> are depth-independent since they read from a flat list;
> the filesystem methods are the ones that need depth awareness.

### 1.3 Tag-Based Discovery

When you have a broad category or domain, search by tag. Tags are
wider than keywords and catch skills that use different terminology.

```python
tag = "devops"
matches = [
    s for s in skills
    if tag.lower() in [t.lower() for t in s.get("tags", [])]
]
```

**Common tags found across skill catalogs:**

| Tag             | What it covers                       |
|-----------------|--------------------------------------|
| python          | Python development, testing, packaging|
| javascript      | JS/TS, frontend, Node                |
| programming     | General coding best practices        |
| devops          | CI/CD, deployment, infra             |
| security        | Auth, scanning, hardening            |
| data            | Analysis, pipelines, ETL             |
| testing         | TDD, unit tests, integration         |
| api             | REST, GraphQL, endpoints             |
| automation      | Workflows, bots, scripts             |
| writing         | Content, copywriting, documentation  |
| research        | Literature review, discovery         |
| cloud           | AWS, Azure, GCP                      |

### 1.4 Source Filtering

When you find matches across multiple sources, filter by source
trust level. This prioritizes officially maintained skills over
community ones.

```python
# Prefer official sources
source = "official"  # also: "github", "community"
matches = [
    s for s in skills
    if source in s.get("source", "").lower()
]
```

**Source trust tiers (best practice):**

| Tier  | Source type     | Examples                   |
|-------|-----------------|----------------------------|
| 1     | Official        | Platform-bundled, maintained |
| 2     | GitHub/verified | Community repos, transparent |
| 3     | Aggregator      | Marketplaces, third-party collections |

### 1.5 Stack-Based Discovery

Given a user's tech stack, discover skills across multiple
keywords:

```text
Stack: Kubernetes + Python + PostgreSQL
Keywords: "kubernetes", "python", "database"
→ kubernetes-best-practices, python-development, postgres-migrations
```

This pattern works best when you search each keyword separately
and intersect the results by relevance.

---

## Section 2: External Marketplace Scan

When local/searchable catalogs and featured/curated sources return
nothing, scan external marketplaces. The following sources are
known to index agent skills. **Verify reachability at query time**
-- URLs drift.

### 2.1 Marketplace Fallback Order

1. **skills.sh** (https://skills.sh/) -- Primary public leaderboard.
   Supports agent type filtering, install via `npx skills add`.
2. **agentskill.sh** (https://agentskill.sh/) -- Broad marketplace
   with quality scores, security audits, and role/platform filters.
3. **SkillsMP** (https://skillsmp.com/) -- Broad aggregator with
   occupation and category maps. Claims 270K+ indexed files.
4. **ClawHub** (https://clawhub.ai/) -- OpenClaw skills and plugins
   marketplace. Higher risk -- inspect source before use.
5. **skilldock.io** (https://skilldock.io/) -- Versioned skill
   registry with publish/install workflow. V2 in development.
6. **Direct GitHub search** -- Search for `<tool> SKILL.md`,
   `<tool> agent skill`, or `<tool> agentskills.io`.

### 2.2 GitHub Source Search

When marketplaces don't have what you need, search GitHub directly.
Do not rely on hand-maintained repo lists or star counts — repository
membership, popularity, and format details drift.

**Recommended searches:**

```text
"SKILL.md" "<domain>"
"agentskills.io" "<domain>"
"<agent-name>" "skill"
site:github.com SKILL.md "<task keyword>"
```

Evaluate each discovered repo using §4:

- Does it contain `SKILL.md` files or an agentskills.io-compatible format?
- Is the source transparent and inspectable?
- Does recent activity suggest the repo is maintained?
- Does the skill match the user's task, or only the broad domain?
- Are install/discovery instructions compatible with the current agent?

Prefer official/vendor repos first, then transparent GitHub repos, then
aggregators or marketplaces. Treat star counts as freshness hints only —
verify the actual files before recommending a skill.

### 2.3 Ecosystem Directories

For agent-ecosystem-specific searches (not general skill
catalogs), check:

- **hermesatlas.com** -- Community directory that lists repos
  by category and star ranking. Most thorough ecosystem directory
  for discovering agent repos across platforms.
- **awesome-copilot** (github.com/github/awesome-copilot) --
  ~36K stars, community-curated Copilot resources.
- **anthropics/claude-plugins-official** -- Official Claude
  Code plugins and extensions repo.

### 2.4 Browser-Based Marketplace Search

Many marketplaces (skills.sh, agentskill.sh) are JavaScript-rendered
single-page applications. A simple `curl` probe only checks whether
the server responds; it cannot search for skills, extract results,
or read SKILL.md content from rendered pages. When HTTP/API probes
return no usable data, use a browser to search interactively.

**Workflow:**

1. Verify the marketplace is reachable (section 7), then navigate
   to its search URL with your keyword as a query parameter:
   ```
   browser_navigate("https://skills.sh/search?q=<keyword>")
   ```
2. If the page is a JS SPA, the search box may be pre-filled but
   results not yet loaded. Press Enter or click the search button
   to trigger the search.
3. **Read the results from the rendered snapshot.** Each result
   typically shows rank, skill name, repository name, and install
   count — enough for a first pass tier classification (section 4.2).
4. **Click through to top candidates** to inspect the full SKILL.md
   content, security audit badges, and install command.
5. **Read the raw SKILL.md** from the source repository when the
   marketplace page only shows a summary. Most marketplaces link
   to the source repo; use `curl` or the browser to fetch:
   ```
   curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/SKILL.md"
   ```
6. **Apply the evaluation rubric (section 4)** to each candidate —
   same criteria as catalog search results.

**Pitfalls:**
- Bot detection varies. If a marketplace blocks the browser session,
  fall back to curl/API methods or try a different marketplace.
- Some marketplaces have a search API even if the main page is a
   SPA. Check `https://skills.sh/api/search?q=<keyword>` or similar
  before falling through to the browser.
- Results are sorted by install count, which biases toward older
  skills. Check the last few pages for newer entries.

### 2.5 General Web Research

When structured marketplaces return nothing, use general-purpose
web research to find skills through search engines, blog posts,
documentation, and community discussions. This is the widest net
and the final fallback before building from scratch.

**Search patterns:**

```
"<domain>" SKILL.md
"<domain>" agent skill
"<domain>" agentskills.io
site:github.com "<domain>" SKILL.md
"<domain>" terminal multiplexer  (when the exact domain term is obscure)
best agent skill for "<domain>"
```

**Sources to check:**

| Source | Search method | Notes |
|--------|---------------|-------|
| GitHub code search | API or browser | Search for `SKILL.md` + keyword. Some repos don't use agentskills.io format but still contain useful instructions. |
| GitHub topic search | `https://github.com/topics/<topic>` | Browse repos by topic tag (e.g., `agent-skill`, `claude-skill`). |
| Blog posts / tutorials | Browser search engine | Agents and their skills are often described in blog posts that link to or describe the skill. |
| Platform documentation | Vendor docs (curated) | Official skill registries (Anthropic, OpenAI Codex, Gemini CLI) may list skills not indexed by third-party marketplaces. |
| Community discussion | Discord/forum archives | New skills often appear in community channels before they reach marketplaces. |

**Workflow:**

1. Search for `"<keyword>" SKILL.md` across multiple sources
2. For each result, evaluate whether it contains agentskills.io
   frontmatter or usable skill instructions
3. Apply the evaluation rubric (section 4)
4. If the best result is a blog post that describes a skill without
   providing a SKILL.md file, note the approach for section 3
   (skill creation fallback) rather than recommending the post
   directly

---

## Section 3: Skill Creation Fallback

When no existing skill matches the task, build one from scratch.

### 3.1 Minimal SKILL.md Template

```yaml
---
name: my-skill-name
description: What this skill does and when to use it.
---
# My Skill Name

## Purpose
One paragraph explaining the problem this skill solves.

## Instructions
Step-by-step instructions the agent should follow.

## Commands
Any relevant CLI commands, code blocks, or examples.

## Pitfalls
Known issues, gotchas, or edge cases to watch for.
```

### 3.2 Placement

Copy the skill directory to your agent's skills directory:

| Agent            | Skills directory         |
|------------------|--------------------------|
| agentskills.io    | `.agents/skills/` (cross-platform) |
| Claude Code      | `.claude/skills/`                 |
| Codex CLI        | `.codex/skills/`                  |
| Gemini CLI       | `.gemini/skills/`                 |
| Cursor           | `.cursor/rules/`                  |

Check your agent's documentation -- discovery paths vary.

---

## Section 4: Evaluation Rubric

Before proposing a skill to the user, evaluate each candidate
against these criteria.

### 4.1 Checklist

- [ ] **Name:** Is it descriptive enough to understand the domain?
- [ ] **Description:** Does it explicitly mention the user's task or
      domain? (Not just a generic match)
- [ ] **Source trust:** Official > GitHub/verified > community > unknown
- [ ] **Freshness:** When was the catalog last updated? Note staleness
      if >2 weeks.
- [ ] **Keyword expansion:** Did you search for acronyms, short forms,
      and aliases alongside the primary keyword? (e.g., "js" alongside
      "javascript", "k8s" alongside "kubernetes")
- [ ] **Search depth:** Did the search method reach all levels of
      the skills directory? (Filesystem methods only — JSON indexes
      are depth-independent)
- [ ] **Alternatives:** Check if multiple skills cover the same
      territory. Prefer the one with clearer instructions.
- [ ] **Format check:** Does it follow the agentskills.io standard?
      (Must have `name` + `description` frontmatter)
- [ ] **Compatibility:** Does the skill declare a `compatibility` field
      that might limit which agents can use it?

### 4.2 Tiered Recommendation

Classify each candidate into one of three tiers:

| Tier | Criteria | Action |
|------|----------|--------|
| **Direct hit** | Name and description clearly match the task. Source is trusted. | Recommend first. |
| **Partial match** | Covers a related domain but isn't a precise match. | Consider if no direct hit exists. Note the gap. |
| **Off-domain** | Unrelated to the task. | Skip. Document as excluded with brief reason. |

### 4.3 Recommendation Template

```
I searched [source] for "[keyword]" and found [N] matches.

Top recommendation: `[skill-name]`
  What it does: [description]
  Source trust: [official / github / community]
  Why: [reason it fits this task]

Alternatives: [other-matching-skills]

If none fit, I can build a minimal skill from the methodology's
creation fallback (Section 3).
```

### 4.4 Project-Portfolio Mapping

When evaluating a pool of candidates against active projects:

1. Inventory active projects and their primary purpose
2. Map each skill to a specific project
3. Check if an existing installed skill already covers this territory
4. Tier by impact: direct need > useful improvement > already covered
5. Recommend with project-specific rationale

---

## Section 5: Discovery Patterns

### Pattern 1: Task-to-Keyword Mapping

```
Task: "Set up CI/CD pipeline"
Keywords: "ci", "cd", "pipeline", "github actions"
```

Map the task to 2-3 core nouns. Avoid filler words ("how to",
"show me", "all the").

**Then expand each keyword** for acronyms, abbreviations, and short
forms (see §1.2 step 2). This is the most commonly missed step in
the methodology — it turns a zero-result search into a match.

### Pattern 2: Category Expansion

When you find one skill in a domain, expand to find related ones:

```
Found: github-pr-workflow
Expand search for: "github", "pull-request", "code-review", "git"
```

### Pattern 3: Stack-Based Discovery

For multi-stack tasks, use §1.5: search each stack component
separately, then prefer skills that cover the intersection. If no
multi-stack skill exists, recommend one skill per stack component.

### Pattern 4: Depth Verification

After a filesystem search returns zero results, verify depth
coverage before concluding no matches exist:

1. **Count the SKILL.md files discovered:**
   ```bash
   find skills -name SKILL.md | wc -l
   ```
2. **Compare against total files in the directory:**
   ```bash
   find skills -name SKILL.md | wc -l
   # vs
   ls -d skills/*/SKILL.md skills/*/*/SKILL.md 2>/dev/null | wc -l
   ```
   If the counts mismatch, your glob is too shallow (see §1.2
   catalog depth warning).
3. **Test with a known-present skill:** if you know a specific
   skill exists (e.g., `node-inspect-debugger`), search for its
   exact name. If it doesn't appear, your search depth is wrong.
4. **Expand your search method** before falling back to higher
   stages of the fallback chain.

### Pattern 5: Web Research Fallback

When all structured sources return nothing, research the web
using search engines, GitHub topic pages, and vendor docs:

```
Task: "find ssh skill"
Marketplace returns: 40 results but all are off-domain or partial
→ Web research search terms:
  "ssh terminal multiplexer SKILL.md"
  "ssh remote access agent skill"
  site:github.com "ssh" "SKILL.md"
→ Check vendor skill registries:
  https://github.com/anthropics/claude-plugins-official (search repo for "ssh")
  https://github.com/openai/skills (browse catalog)
  https://github.com/topics/agent-skill (browse by topic)
```

For each web result, apply the same evaluation rubric (§4). A blog
post describing a skill approach without providing SKILL.md is a
signal for §3 (skill creation fallback), not a recommendation.

---

## Section 6: Task-to-Search-Term Examples

These are user-task keywords, not necessarily catalog tags. Use them
to seed name/description searches when structured tags are absent or
sparse.

| Task keyword    | Also try               | What to find                          |
|-----------------|------------------------|---------------------------------------|
| python          | `py`                   | Python dev, debugging, testing skills |
| javascript      | `js`, `node`, `nodejs` | JS/TS, Node.js, frontend development |
| docker          | —                      | Container best practices, deployment  |
| api             | `rest`, `graphql`      | REST API design, endpoints, GraphQL   |
| security        | `auth`, `hardening`    | Auth, secrets scanning, hardening     |
| testing         | `tdd`, `unit`          | TDD, unit tests, integration tests    |
| database        | `sql`, `postgres`      | SQL, Postgres, migrations             |
| react           | `jsx`, `frontend`      | React best practices, frontend design |
| typescript      | `ts`, `tsx`            | TypeScript development, type safety   |
| cli             | `shell`, `terminal`    | Command-line tools, shell scripting   |
| git             | —                      | Git workflows, branching strategies   |
| cloud           | `aws`, `azure`, `gcp`  | Cloud infrastructure, deployment      |
| data            | `pandas`, `etl`        | Data analysis, pipelines              |
| video           | `ffmpeg`               | Video processing, encoding            |
| audio           | `transcription`        | Audio processing, speech-to-text      |
| automation      | `workflow`, `ci`, `cd` | Workflow automation, CI/CD            |
| writing         | `docs`, `content`      | Content writing, documentation        |

---

## Section 7: Runtime Verification

External sources drift. Before relying on a marketplace or source
URL, verify it is reachable.

**Method:** Use the agent's native HTTP/query capability to check each
source before searching it. If shell access is available, one example is:

```bash
curl -s -o /dev/null -w "%{http_code}" <url>
```

A 200 or 3xx response means the source is reachable. 4xx or 5xx means
skip or fall back.

**URLs to verify (best-effort, last checked 2026-07-01):**

| Source        | URL                            | Status |
|---------------|--------------------------------|--------|
| skills.sh     | https://skills.sh/             | 200    |
| agentskill.sh | https://agentskill.sh/         | 200    |
| SkillsMP      | https://skillsmp.com/          | 200    |
| ClawHub       | https://clawhub.ai/            | 200    |
| skilldock.io  | https://skilldock.io/          | 200    |
| agentskills   | https://agentskills.io/        | 200    |

**Note:** External source status can change between sessions. Treat
recorded HTTP statuses as examples only; verify every source at query
time before relying on it.

### When All Sources Are Exhausted

If no source returns a match and the search was thorough:

1. Report what was searched (catalog, featured, marketplaces,
   browser searches, web research) and which stages were skipped
   due to missing tooling
2. Check if you have browser tooling that wasn't used — many
   marketplaces require a browser to render search results
   (see §2.4)
3. Offer to build a minimal skill (Section 3)
4. If the skill already exists somewhere not indexed, note the gap
   for future catalog ingestion

---

## Section 8: Sources & Methodology Evidence

This methodology was built from live research on 2026-07-01:

- **Hub catalog scan:** 2,460 indexed skills across 7 sources
- **agentskills.io client count:** 42 confirmed via home page carousel
- **External marketplaces:** 6 reachable, 1 Showcase page (resolved 404→200 same day)
- **`hub-explorer` skill (archived):** Source for the search/evaluate/recommend
  pipeline (Hermes-specific references removed for portability)

This methodology is designed to be self-verifying — it teaches you
how to check source freshness at runtime rather than relying on
hand-maintained tables that rot.

---

## Section 9: What This Skill Does NOT Do

- Does **not** ship a collection of skills
- Does **not** hardcode catalog paths or source URLs (it teaches
  runtime verification instead)
- Does **not** include platform-specific adapter files
- Does **not** generate indexes or catalogs
- Does **not** maintain an external source table that drifts

Its only job is to teach any agent the discovery pipeline. The
agent executes the pipeline using its own tools.

---

## Appendix: Reference Skills

These are known, maintained skills that the methodology references or
recommends. This is not a catalog — it's a short list of skills this
methodology has evaluated and can point to as known-good examples.
Add entries here when a skill is consistently needed across sessions.

- **[tmux](https://www.skills.sh/steipete/clawdis/tmux)** —
  Tmux terminal multiplexer skill: session/panel management, send keys,
  capture output, prompt checks. 5.1K installs. Security-audited (Gen AI
  Trust Hub, Socket, Snyk). Source: `steipete/clawdis` on GitHub. Install
  via `npx skills add https://github.com/steipete/clawdis --skill tmux`.

- **[CodeSigils/agents-markdown-formatter/markdown-formatter](https://github.com/CodeSigils/agents-markdown-formatter)** —
  GFM/MDX Markdown formatter with table, pipe, and fence structural
  guards. Zero npm dependencies. Install by adding the repo's skill
  directory to your agent's skills path (see §3.2).
