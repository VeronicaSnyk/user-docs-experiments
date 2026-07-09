---
name: fetch-confluence
description: Fetch documentation from Confluence pages by URL, page ID, or search query. Use when the user asks about style guides, writing standards, documentation guidelines, or needs to retrieve any Confluence content. Outputs Markdown for easy reading.
license: Proprietary
compatibility: Requires Python 3.x, Confluence credentials in .env
metadata:
  author: edmond.sabou
  version: "2.0.0"
  category: documentation
---

# Fetch Confluence Documentation

**First-time setup required:** If `.docs-agent/.env` doesn't exist, create it:
```bash
cp .docs-agent/skills/fetch-confluence/.env.example .docs-agent/.env
```
Then edit it with your Confluence credentials: `CONFLUENCE_BASE_URL`, `CONFLUENCE_EMAIL`, `CONFLUENCE_API_TOKEN` (get token from https://id.atlassian.com/manage-profile/security/api-tokens).

## Usage

Fetch by page ID (recommended):
```bash
python scripts/fetch_confluence.py 1836843231
```

Fetch by URL:
```bash
python scripts/fetch_confluence.py https://snyksec.atlassian.net/wiki/spaces/DOC/pages/1836843231/Page+Title
```

Search for pages:
```bash
python scripts/fetch_confluence.py --search "style guide"
python scripts/fetch_confluence.py --search "API documentation" --limit 5
```

Output is Markdown by default. Add `--json` for raw JSON or `--html` for HTML.

## Common Page IDs

**Snyk Style Guide Pages:**
- Writing Rules: `1836843231`
- Inclusive Language: `1836744906`
- Capitalization: `1836744935`
- Screenshots: `1836908842`

## Gotchas

- Script fails immediately if `CONFLUENCE_BASE_URL`, `CONFLUENCE_EMAIL`, or `CONFLUENCE_API_TOKEN` are missing from `.env`
- Credentials loaded from `.docs-agent/.env` (recommended), `skills/fetch-confluence/.env`, or project root `.env`
- Page URLs must include `/pages/<id>/` — shortened or redirect URLs won't work
- Search uses Confluence CQL syntax: `text ~ "query"` searches all text
- Always fetches fresh content from Confluence (no caching)
