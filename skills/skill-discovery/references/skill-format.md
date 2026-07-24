# Skill Format Reference

This document outlines the standard format for agent skills, serving as a reference for evaluating whether a candidate skill is well-made.

## 1. Frontmatter Specification

Skill metadata is defined in the frontmatter section of the `SKILL.md` file.

**Required Fields:**

- `name`: (String) Unique identifier for the skill.
  - Constraints: 1-64 characters, lowercase `a-z0-9-`, no double hyphens (`--`), no leading or trailing hyphens. Must exactly match the skill's folder name.
  - Examples:
    - Valid: `pdf-processing`, `data-analysis`, `code-reviewer`
    - Invalid: `PDF-Processing`, `-pdf`, `pdf--processing`, `pdf-`
- `description`: (String) A concise summary of the skill's purpose and capabilities.
  - Constraints: 1-1024 characters, target 80-150 characters for optimal display.

**Optional Fields:**

- `license`: (String) The license under which the skill is distributed (e.g., `MIT`, `Apache-2.0`).
- `compatibility`: (String) A comma-separated list of agent platforms the skill is known to be compatible with.
  - Constraints: Maximum 500 characters.
- `metadata`: (Object) Contains additional structured information about the skill.
  - `author`: (String) The author or organization responsible for the skill.
  - `version`: (String) The semantic version (e.g., `1.0.0`) of the skill itself. This is distinct from any product version the skill might interact with, which should be tracked in a separate `README.md` if applicable.
  - `argument-hint`: (String) A brief hint for skill invocation arguments.

**Field Order (Recommended):**

1. `name`
2. `description`
3. `license`
4. `compatibility`
5. `metadata`
6. Any other custom fields

## 2. Description Quality

A high-quality skill description is crucial for discoverability and effective agent utilization.

**Formula:**
`[Product] [core function]. Covers [2-3 topics]. Keywords: [terms].`

**Constraints:**
- Target length: 80-150 characters.
- Maximum length: 1024 characters.
- No marketing adjectives: Avoid words like "powerful," "comprehensive," "modern."
- No filler phrases: Avoid "this skill," "use this for," "helps with."
- All skill content, including the description, must be in English.

**Examples:**
- **Good:** "Turso SQLite database. Covers encryption, sync, agent patterns. Keywords: Turso, libSQL, SQLite."
- **Good:** "Docker Compose generator for isolated dev environments. Covers networking, volumes, profiles. Keywords: Docker, Compose, containers."
- **Bad:** "A powerful solution for all your database needs with modern features."
- **Bad:** "This skill helps you work with Docker by providing comprehensive container management."

**Judgment Checklist (for evaluation):**
- Do description keywords appear in the `SKILL.md` body?
- Can you tell what the skill does without reading further?
- Are there any marketing adjectives or unnecessary filler?

## 3. Folder Purposes

The standard folder structure within a skill helps agents and developers understand the purpose of each file and directory.

| Folder      | Purpose                                    |
| :---------- | :----------------------------------------- |
| `references/` | Documentation for agents to READ           |
| `examples/`   | Sample outputs showing expected format     |
| `assets/`     | Static resources to COPY/USE               |
| `scripts/`    | Executable code for agents to RUN          |

This structure aligns with the existing repository patterns.

## 4. Client Extensions

Some agent platforms may utilize platform-specific frontmatter fields. These fields are generally safe to ignore by other clients. The primary risk is a skill shipping platform-specific fields as if they were universally portable.

| Client            | Example Agent-Specific Fields |
| :---------------- | :---------------------------- |
| Codex             | `codex-hooks`                 |
| Claude Code       | `claude-specific-field`       |
| Cursor            | `cursor-rules`                |
| OpenCode          | `opencode-plugin`             |
| Gemini CLI        | `gemini-config`               |
| GitHub Copilot    | `copilot-feature`             |

(Refer to [`platform-locations.md`](platform-locations.md) for client-specific paths and documentation.)