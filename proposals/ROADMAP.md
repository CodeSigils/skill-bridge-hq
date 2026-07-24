# ROADMAP

Internal proposals and investigation artifacts. Not shipped, not tracked by git.

## Implementation Discipline

When making any implementation change (new feature, bugfix, refactor, CI
change), always check whether README, docs, or references need updating.
Specifically:

  1. README "What it does in practice" — does the change affect the
     7-stage workflow? If yes, update the relevant step.

  2. README "Skill payload" — does the change affect validation output,
     the example, or the checklist? If yes, keep them in sync.

  3. README "Evidence and validation" — does the change add/remove a
     validator, CI step, or evidence source? Update the three subsections.

  4. README "Repository layout" — does the change add/remove files?
     Update the file list.

  5. References — does the change add knowledge the agent should use
     during workflow steps? Add it to the appropriate reference file
     and update SKILL.md's "Supporting references" if needed.

  6. ROADMAP — document what was done and when (Phase 1 summary pattern).

Do not treat docs as a separate task. They are part of the implementation.
A change that ships code but leaves docs stale is incomplete.

## Projects For Investigation (historical)

Research that led to Phase 1 decisions. Preserved for context.

### skill-master meta-skill: what it does better

Source: [skill-master SKILL.md](https://raw.githubusercontent.com/NeverSight/skills_feed/refs/heads/main/data/skills-md/itechmeat/llm-code/skill-master/SKILL.md) (NeverSight/skills_feed, author: itechmeat, v1.2.3)

skill-master is a meta-skill for creating and maintaining agent skills. 238 lines
in SKILL.md plus scripts/, references/, and assets/. Claude Code–leaning but the
content is largely agent-agnostic.

skill-discovery is a meta-skill for finding and evaluating skills. ~130 lines in
SKILL.md plus 4 reference files. Agent-agnostic by design.

They are complementary: CREATE vs FIND. The gaps below are where skill-discovery
assumes knowledge that skill-master teaches.

#### Gaps in skill-discovery that skill-master fills

1. SKILL.MD SPEC LITERACY
   skill-master spells out the full frontmatter schema: required fields, optional
   fields, validation rules, name constraints (1-64 chars, lowercase, no --,
   must match folder). skill-discovery assumes the agent already knows the spec.
   An agent discovering a skill cannot verify frontmatter conformance without
   loading another skill or reading the spec externally.

2. DESCRIPTION QUALITY FORMULA
   skill-master provides:
     [Product] [core function]. Covers [2-3 topics]. Keywords: [terms].
   With constraints (80-150 chars, no marketing, no filler) and good/bad
   examples. skill-discovery has nothing equivalent. Its workflow says "search
   name, description, tags" but does not teach what a good description looks
   like — relevant when evaluating whether a candidate description is
   trustworthy signal or noise.

3. SCAFFOLDING AND VALIDATION TOOLS
   skill-master ships 4 scripts:
     init_skill.py           — scaffold new skill
     quick_validate_skill.py — validate structure + frontmatter
     package_skill.py        — package for distribution
     init_copilot_asset.py   — Copilot-specific scaffolding
   skill-discovery has CI validators for its own repo (ci-check.py,
   validate-docs.py, verify-marketplace-urls.py) but no user-facing tools
   for validating a discovered or created skill.

4. TEMPLATE AND SCAFFOLD PATTERNS
   skill-master has assets/skill-templates.md with starter SKILL.md templates.
   skill-discovery has no templates. Step 7 of the workflow says "offer to
   create a minimal new skill" but provides no scaffold to create from.

5. FOLDER PURPOSE MATRIX
   skill-master has a clear table distinguishing:
     references/ — documentation for agents to READ
     examples/   — sample outputs showing expected format
     assets/     — static resources to COPY/USE
     scripts/    — executable code to RUN
   skill-discovery's repo structure follows this pattern but never teaches it.

6. DOCUMENTATION INGESTION WORKFLOW
   skill-master has a 4-phase workflow for building skills from external docs
   (scaffold, build queue, ingest loop, finalize). skill-discovery has nothing
   for this. When discovery finds a skill built from docs, there is no pattern
   for evaluating whether the ingestion was done well.

7. VERSION TRACKING PATTERNS
   skill-master distinguishes skill version from product version, shows
   release_date field, and provides a standardized README.md links section
   format. skill-discovery's freshness check says to "inspect generation
   timestamp" but does not address how skills version themselves or how to
   tell if a skill tracks an outdated product version.

8. PROHIBITION LIST
   skill-master has explicit DO NOT rules:
     - No large verbatim chunks from vendor docs
     - No non-English content
     - No secrets/paths/assumptions
     - SKILL.md under 500 lines
     - No skipped name validation
   skill-discovery has "boundaries" but no skill-authoring prohibitions.
   Relevant when evaluating whether a candidate skill was well-made.

#### What skill-discovery does better (keep these)

1. SECURITY AND TRUST FRAMEWORK — trust-review.md is thorough: provenance,
   complete payload inspection, capability enumeration, dependency analysis,
   external evidence evaluation. skill-master has zero security review.

2. PLATFORM COVERAGE — 6 clients mapped (Codex, Claude Code, Cursor,
   OpenCode, Gemini CLI, GitHub Copilot) with project + user locations.

3. AGENT-AGNOSTIC DESIGN — No platform-specific frontmatter fields promoted
   as primary.

4. CATALOG CONTRACT DOCUMENTATION — catalog-contracts.md documents skills.sh
   API, GitHub search patterns, authenticated fallbacks.

5. STRUCTURED RECOMMENDATION FORMAT — The 7-field report template
   (Need/Searched/Recommendation/Why/Trust/Compatibility/Tradeoffs) is
   production-ready.


## Improvement Ideas ✅ COMPLETE

All 5 priorities implemented 2026-07-22. See Summary below for details.

| # | Proposal | Outcome |
|---|----------|---------|
| 1 | Skill format reference | Created `references/skill-format.md` (89 lines) |
| 2 | Extract validation script | Created `scripts/validate-skill.py` (150 lines, 8 tests) |
| 3 | ~~Scaffold template~~ | Dropped — agents have built-in creation tools |
| 4 | ~~Freshness evaluation~~ | Split: format ref + trust-review.md subsection |
| 5 | Ingestion quality checklist | Folded into trust-review.md (5-line addition) |

Key decisions:
- No standalone template file (agents handle creation)
- No prohibitions reference (not needed for discovery)
- Description quality folded into format reference (Priority 1)
- Freshness and ingestion checks added to trust-review.md


## Summary — Phase 1: Skill Format & Validation ✅ COMPLETE

All 5 priorities implemented 2026-07-22.

  NEW FILE:    references/skill-format.md       ~89 lines
  NEW FILE:    scripts/validate-skill.py        ~150 lines
  NEW FILE:    scripts/test_validate_skill.py   ~141 lines (8 tests)
  APPEND:      references/trust-review.md       +19 lines (freshness + ingestion)
  UPDATE:      SKILL.md                         +2 lines (new reference)
  UPDATE:      .github/workflows/ci.yml         +2 steps (test + validate-skill)
  ─────────────────────────────────────────────
  Total: ~400 lines of new/changed content

  2 of 8 gaps are real (spec literacy, validation access) → done
  3 are folded into existing files (folder purposes, freshness, ingestion) → done
  2 are not real gaps (templates, prohibitions) → confirmed not needed
  1 is already solved (description quality) → folded into Priority 1

Additional work beyond ROADMAP:
  - README rewritten: practical example, payload section, scripts layout
  - ci-check.py regex bug fixed (double-escape in hermes path)
  - 10 new tests added to test_validators.py (PortabilityTests + ContractDriftTests)
  - .gitignore enriched with Python caches/artifacts
  - README restructured: understand → act → verify flow, no duplicates


## Phase 2: Automated Freshness

The goal: jobs that detect staleness AND fix it without human review.
Reality check — most maintenance requires judgment. Only one item is
truly self-healing. The rest detect and notify.

### Current state

  Push/PR:   validators, tests, ci-check, validate-docs (every push)
  Schedule:  verify-marketplace-urls.py weekly (Monday 6am)
  Expiry:    validate-docs.py checks `expires` field on every push

  TODO: add a "Maintenance" section to README for repo maintainers.
  Should cover: what runs automatically (CI validators, weekly URL
  check), what creates issues but needs human action (research expiry),
  and what requires manual intervention (reference file changes,
  SKILL.md budget, internal link rot). Keep it short — a table with
  3 columns: check, trigger, who acts.

### P1 — Auto-fix URL drift (fully automated)

URL drift fails the weekly CI job but creates no issue and fixes nothing.
Nobody gets notified unless watching Actions.

Fix: when verify-marketplace-urls.py detects a redirect or status change,
update `evidence-urls.json` in place and commit. ~20 lines of Python.
The manifest is the source of truth — if `agentskills.io` moved to
`skills.sh`, the script follows the redirect, updates the entry, and
pushes. Zero human involvement.

### P2 — Auto-issue on research expiry (semi-automated)

Research expiry fails CI on push but creates no reminder between pushes.
If nobody pushes for 2 weeks, expiry goes unnoticed.

Fix: add a check in verify-marketplace-urls.py (already runs weekly)
that reads `expires` from research frontmatter and creates an issue
if within 14 days. ~10 lines of Python. Human reviews the issue —
can't auto-research, that requires judgment.

### Artifact audit (2026-07-24)

All artifacts current and in use. No removals needed.

  docs/hub-marketplace-research.md              expires 2026-10-01
  docs/reference-style-links-as-anti-drift.md   expires 2027-07-15
  docs/evidence-urls.json                       13 URLs
  .github/scripts/                              4 scripts, all in CI
  scripts/                                      2 scripts, all in CI

### P3 — `last_verified` field on URL entries (one-time migration)

Nobody currently asks "which URLs haven't been checked?" but when the
auto-fix fires (P1), the first question is "is this a new drift or
has it been failing for months?" Without `last_verified`, there's no
answer.

Fix: add `"last_verified": "2026-07-24"` to each entry in
`evidence-urls.json`. One-time ~15 line migration. Zero ongoing cost —
the field updates itself whenever verify-marketplace-urls.py runs
successfully.

### P4 — Weekly repo health cron (detect-only)

Three checks that push CI can't catch — internal link rot, reference
file integrity, and SKILL.md budget creep. All live in one script
(`scripts/cron-health.py`) that runs weekly alongside the existing
URL monitor.

These are **detect-only** — the fixes require human judgment (knowing
where a moved file went, deciding what to cut from SKILL.md, etc.).

**Check 1: Internal link rot** (~20 lines Python)
README and docs link to other repo files (e.g., `skills/skill-discovery/SKILL.md`,
`references/skill-format.md`). These break silently when files move or get renamed.
Scan all markdown files for relative links, verify each resolves.

**Check 2: Reference file integrity** (~10 lines Python)
SKILL.md references 5 files in `references/`. If one gets deleted or renamed,
the agent breaks at runtime. Parse SKILL.md for `references/*.md` paths,
verify each exists.

  Design note: use `--check reference-integrity` flag so CI reports which
  specific check failed, not just "something broke". ~5 extra lines.

**Check 3: SKILL.md budget monitor** (~5 lines Python)
The 500-line limit is enforced on push, but gradual bloat goes unnoticed
between pushes. Check line count, warn if >350.

CI integration: add to the weekly schedule job in `.github/workflows/ci.yml`.
One script, one cron entry, three checks. ~35 lines total.

  Related: update README "Repository layout" with a warning that reference
  files (`references/*.md`) are load-bearing — renaming or deleting them
  breaks the agent at runtime. The weekly cron catches this in CI, but
  a human-readable warning prevents the mistake in the first place.

### What we're NOT doing

  - Tiered cadence (daily/weekly/monthly per URL) — weekly is fine
  - Freshness dashboard — CI output IS the dashboard
  - Content-hash comparison — reachability is sufficient
  - Daily cron — the weekly check + expiry warning covers the gap
  - Standalone template file — agents have built-in creation tools
  - Prohibitions reference — not needed for discovery workflow


## Phase 3: Developer Experience & Hygiene

Small quality-of-life improvements. Each is independent, low-risk,
and can ship in any order.

### P1 — Dependabot for GitHub Actions (low effort)

`actions/checkout` is SHA-pinned (security best practice) but never
updated. Dependabot auto-opens PRs when new versions drop — security
patches, Node.js runtime updates, breaking change warnings.

File: `.github/dependabot.yml` (~10 lines YAML)
Config: target `.github/workflows` directory, weekly schedule, limit
to 3 open PRs to avoid noise.

### P2 — Issue templates (low effort)

No templates today. Freeform issues lose structure — repro steps,
environment info, feature rationale all get skipped.

Files: `.github/ISSUE_TEMPLATE/bug_report.md` + `feature_request.md`
(~20 lines YAML total)
Config: structured fields for bug (steps, expected, actual, env) and
feature (what, why, alternatives). No config bot — just markdown
templates that render as issue forms.

### P3 — Markdownlint in CI (medium effort)

No markdown linting today. Trailing whitespace, inconsistent heading
levels, bare URLs, and missing blank lines around headers all slip
through.

File: `.markdownlint.json` (~15 lines config)
CI step: add `markdownlint` to the validate job (npm install + run).
Scope: only lint `README.md` and `docs/` — skip `skills/` (agent
content, not human-authored).

### P4 — Pre-commit hooks (medium effort)

Validators only run in CI. Broken formatting and trailing whitespace
get committed and pushed before anyone notices.

File: `.pre-commit-config.yaml` (~10 lines)
Hooks: markdownlint, trailing-whitespace, end-of-file-fixer,
check-yaml, check-added-large-files.
README: add setup instruction (`pip install pre-commit && pre-commit
install`).

### P5 — Automated marketplace scanning via external APIs (discussion)

Multiple agent-skill catalog websites now expose public APIs. These could
replace or augment manual marketplace research with periodic automated scans.

**Best candidates (no auth required):**
  - OpenAgentSkill (openagentskill.com) — trust scores, audits, task→skill
    resolution, quality scores. Most comprehensive read-only API.
  - SkillsHub (skillshub.wtf) — 10k+ skills, natural language resolver
    via `/api/v1/skills/resolve?task=...`.
  - Mercury Skills (skills.mercuryagent.sh) — clean JSON, simple metadata.

**Needs auth or blocked:**
  - skills.sh — Vercel OIDC API key required.
  - CrossAITools — Cloudflare blocks automated access.

**Use cases:**
  - Detect new skills that match our workflow patterns
  - Validate our recommendations against external trust/audit data
  - Refresh `docs/hub-marketplace-research.md` with live data

**Tradeoffs:**
  + Pro: automated, no manual research, catches new skills faster
  - Con: external API dependency (what if they go down or change)
  - Con: their trust/audit data may conflict with our own assessment
  - Con: scope creep — monitoring URLs + APIs grows maintenance burden

**Status:** Discussion deferred. Revisit when roadmap is next reviewed.
Add as Phase 2 or Phase 3 item based on how the project evolves.

### What we're NOT doing (Phase 3)

  - CODEOWNERS — solo project, no reviewers to assign
  - PR templates — overhead for solo work
  - Stale issue bot — low issue volume
  - CodeQL / security scanning — ~300 lines of scripts, not warranted
  - Release automation — no versions to publish


## Unified "What we're NOT doing" — All Phases

Cross-phase exclusions (no duplicates):

  Phase 1: standalone template, prohibitions reference
  Phase 2: tiered cadence, freshness dashboard, content-hash, daily cron
  Phase 3: CODEOWNERS, PR templates, stale bot, CodeQL, release automation
