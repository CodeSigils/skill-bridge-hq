---
status: reference
date: 2026-07-08
purpose: >
  Anti-drift note: reference-style Markdown links ([label] in prose,
  [label]: url at bottom) reduce URL maintenance surfaces from N to 1.
  Particularly valuable for agent-authored docs that repeat spec/tool
  references frequently.
---

# Reference-Style Markdown Links as an Anti-Drift Pattern

When a term like `GFM`, `CommonMark`, or `node:test` appears in multiple
places in a document, each inline URL is a maintenance surface:

```markdown
<!-- Bad: N inline URLs, N places to update -->
Zero-dependency [GFM](https://github.github.io/gfm/) and MDX formatter...

Align [GFM](https://github.github.io/gfm/) table columns...

empty cells per [GFM](https://github.github.io/gfm/)...
```

**Each of these is a drift surface.** If the URL changes, every occurrence
must be found and updated. Agents searching for `github.github.io/gfm` to
refactor it will only catch the literal string — any variance breaks the
find.

Reference-style links consolidate this:

```markdown
<!-- Good: one definition, N references -->
Zero-dependency [GFM] and MDX formatter...

Align [GFM] table columns...

empty cells per [GFM]...

[GFM]: https://github.github.io/gfm/
```

Now a single edit at the bottom fixes every reference. The prose stays
readable — no inline URLs breaking line wrapping or agent text generation.

## When to use in skill docs

- Spec references (`[GFM]`, `[CommonMark]`, `[RFC 2119]`)
- Tool names (`[remark]`, `[node:test]`)
- Any term linked 2+ times to the same URL

## Caveat

Some renderers (Obsidian, certain VS Code extensions) may not resolve
reference links in all contexts (table cells, nested list items). Test your
target platform. GitHub and npm README renderers handle them correctly.

## Source

Full analysis: `CodeSigils/agent-concepts-study` → `2026-07-08-reference-style-markdown-links.md`
