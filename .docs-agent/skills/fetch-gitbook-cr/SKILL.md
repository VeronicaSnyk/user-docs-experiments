---
name: fetch-gitbook-cr
description: Read a GitBook change request and its reviewer comments (annotated with the page title and nearest heading each comment sits under), and optionally apply verified markdown edits back to CR pages. Use whenever you need to pull every comment on a GitBook CR for triage or response, find a GitBook space ID or change-request ID, or act on review feedback left in GitBook rather than GitHub. Reading is always safe; applying edits is gated behind an explicit check step.
license: Proprietary
compatibility: Requires Python 3.x, requests, python-dotenv, and GITBOOK_API_TOKEN in .docs-agent/.env
metadata:
  author: veronica.cernea
  version: "1.0.0"
  category: documentation
---

# Fetch GitBook CR

**Trigger:** Use when working with a GitBook **change request** — pulling its
reviewer comments (with the page + section each is anchored to), discovering space
/ CR IDs, or applying agreed edits to CR pages.

GitBook reviewers often leave comments in the GitBook editor, not on the GitHub PR.
This skill reads those comments so they can be triaged and answered, and (carefully)
applies verified fixes back to the CR.

> ⚠️ **Editing GitBook content via the API is lossy.** The content API strips
> internal page links and shifts heading levels. Prefer fixing content in the Git
> repo (Git Sync) or the GitBook editor. Use `apply_cr_edits.py` only for small,
> verified string replacements, and always run its `check` step first. Reading
> (comments, listing) is always safe.

## Setup

Requires a GitBook API token (create at <https://app.gitbook.com/account/developer>,
looks like `gb_api_…`) in `.docs-agent/.env`:

```
GITBOOK_API_TOKEN=gb_api_your_token
```

Install deps: `pip3 install requests python-dotenv`.

## Workflow

### Step 1: Find the space and change-request IDs

```bash
# List orgs + spaces you can access (find the SPACE_ID):
python .docs-agent/skills/fetch-gitbook-cr/scripts/list_gitbook.py

# List change requests in a space (find the CR ID / number):
python .docs-agent/skills/fetch-gitbook-cr/scripts/list_gitbook.py <SPACE_ID>
```

The IDs are also visible in a GitBook URL:
`app.gitbook.com/o/<ORG_ID>/s/<SPACE_ID>/~/changes/<CR_NUMBER>/…`

### Step 2: Fetch the CR's comments

```bash
python .docs-agent/skills/fetch-gitbook-cr/scripts/fetch_cr_comments.py <SPACE_ID> <CR_ID_OR_NUMBER>
# filter to one reviewer:
python .docs-agent/skills/fetch-gitbook-cr/scripts/fetch_cr_comments.py <SPACE_ID> <CR> --author "Name"
```

Each comment comes back annotated with the page title and the nearest heading, so you
can locate exactly what it refers to. Summarize the comments and decide which are
actionable before touching content.

### Step 3 (optional, gated): Apply verified edits

Only for small, agreed markdown fixes. Define the target string replacements, then:

```bash
# 1. verify every target string matches exactly — no writes:
python .docs-agent/skills/fetch-gitbook-cr/scripts/apply_cr_edits.py check
# 2. only if check passes, apply page by page and re-verify:
python .docs-agent/skills/fetch-gitbook-cr/scripts/apply_cr_edits.py apply
```

If `check` reports any mismatch, stop and fix the edit definitions — never force an
apply. For anything beyond a trivial fix, make the change in the Git repo instead.

## Guardrails

- Read freely; write only through the `check` → `apply` gate.
- Never bulk-edit page bodies through the API on a Git-synced space — it corrupts
  links and headings. Prefer the repo / Git Sync.
- Keep the GitBook token in `.docs-agent/.env` (gitignored); never commit it.

## Relationship to other skills

This is the GitBook-review counterpart to the GitHub-side skills. Where
`create-draft-pr` opens a PR and `address-pr-review`-style flows handle GitHub
comments, `fetch-gitbook-cr` handles feedback that lives in GitBook CRs.
