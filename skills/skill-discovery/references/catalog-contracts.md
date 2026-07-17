# Catalog and source-search contracts

Prefer provider CLIs and documented APIs. Verify this file against provider
documentation when a query depends on exact authentication or response fields.

## skills.sh

For interactive/local discovery, use the official installer CLI:

```bash
npx --yes skills find '<query>'
npx --yes skills add <owner/repository> --list
```

Programmatic search uses the documented v1 endpoint:

```text
GET https://skills.sh/api/v1/skills/search?q=<query>&limit=<n>
Authorization: Bearer <Vercel OIDC token>
```

The response places results in `data`. Authentication and rate limits are part
of the contract; see <https://www.skills.sh/docs/api>. Do not rely on the legacy
unauthenticated `/api/search` endpoint even if it happens to respond.

## GitHub source search

GitHub code search requires authentication. Prefer the dedicated `gh search`
subcommand which supports structured qualifiers:

```bash
gh search code '<query>' filename:SKILL.md path:skills/ --limit 10
```

The `path:skills/` qualifier filters out SKILL.md files used as project
documentation (not agent skills). If the authenticated CLI is available, this is
the preferred path — one call, scoped results, no dedup needed on the client
side.

When `gh` is installed but not authenticated, try a curl-based web search that
needs no token. GitHub serves a browsable HTML page for code search queries:

```bash
curl -sSfL \
  'https://github.com/search?q=<url-encoded-query>+filename%3ASKILL.md+path%3Askills%2F&type=code'
```

Extract result URLs from the HTML response. Signal that authentication was
missing; a degraded path with HTML scraping is slower and more fragile than the
authenticated API.

When `curl` is also unavailable, fall back to a general web search using
`site:github.com <query> SKILL.md skills/`. Report the missing authenticated and
curl stages.

Verify the current contract in the
[GitHub REST search documentation](https://docs.github.com/en/rest/search/search#search-code).

## Other marketplaces

Treat every third-party marketplace as volatile:

1. open its current documentation or help output;
2. verify authentication, rate limits, pagination, and response shape;
3. distinguish a successful HTTP response from a semantically valid result;
4. inspect the source repository rather than trusting marketplace metadata;
5. record the query timestamp and failure mode.

Never infer safety from ranking, featured placement, download totals, or a 200
status code.
