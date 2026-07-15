# Security Policy

## Supported Versions

This repo ships one skill methodology with supporting reference files. There are
no versioned releases — always use the latest commit from `main`.

## Reporting a Vulnerability

The shipped methodology has no runtime dependency of its own and this repository
runs no network-facing service. The workflow it teaches does access external
catalogs and inspect third-party skills, which may contain scripts or request
powerful tools. Treat every discovered skill as untrusted until its complete
contents, provenance, dependencies, and requested capabilities have been
reviewed. If you find an issue with the content or CI configuration, please open
a public issue on GitHub.

Do **not** open a public issue if the vulnerability involves the GitHub
Actions workflow (e.g., leaked secrets in CI logs). Report privately to the
repository owner via GitHub's security advisory tool.

## Commit Signing

Maintainer commits beginning with `0166f96` on 2026-07-05 are SSH-signed.
Earlier commits, including two commits from that date, may be unsigned and are
retained to avoid rewriting public history.
