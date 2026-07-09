---
name: gather-context
description: Enrich a documentation request with additional, verifiable context before drafting. Cross-checks a Jira ticket against extra sources (AlphaPatch, ask-snyk, Confluence, Google Docs) to confirm details and surface gaps, then reports what is confirmed vs. missing. Use from ship-it-new-docs / ship-it-doc-updates when a ticket is thin or references internal systems. Degrades gracefully when the internal MCP servers are not available.
license: Proprietary
metadata:
  author: veronica.cernea
  version: "1.0.0"
  category: documentation
---

# Gather Context

**Trigger:** Invoked by `ship-it-new-docs` / `ship-it-doc-updates` (Step 2.5), or run
directly when a documentation request needs more grounding before drafting.

This skill adapts the research fan-out pattern from Snyk's IDE support-triage harness
(AlphaPatch / ask-snyk / Confluence enrichment, with a sensitivity gate) to the docs
workflow. Its job is **verification, not invention**: it tells the drafting step what
is confirmed by a real source and what is still missing.

## Inputs

- A Jira ticket key (and the already-fetched ticket text, if available).
- Any source links the ticket references (PRD, one-pager, spec, Confluence, Google Docs).

## What it does

1. **Inventory the claims.** From the ticket and its linked sources, list the concrete
   facts a doc would need: feature name, exact UI/CLI/API surface, prerequisites,
   limits, availability (GA/beta/preview), and the release date.

2. **Confirm each claim against a source.** For every claim, try to find a source that
   states it:
   - **Confluence / Google Docs** — via `fetch-confluence` and `fetch-google-docs`.
   - **AlphaPatch MCP** — if configured, query it for engineering context on the
     feature/commit/ticket. Tools appear as `mcp__alphapatch__*` (or similar).
   - **ask-snyk MCP** — if configured, query internal Q&A / engineering docs. Tools
     appear as `mcp__ask-snyk__*` (or similar).
   - **Snyk User Docs MCP** — for what published docs already say (avoids contradiction).

   > **Availability is not guaranteed.** These internal MCP servers may not be
   > registered in every environment (they are absent in CI by default). Detect them
   > with the tool list; if a server is missing, skip it and record it as "not
   > checked" — never block or fail on a missing MCP.

3. **Apply the sensitivity gate.** Anything sourced from internal systems (AlphaPatch,
   ask-snyk, internal Confluence) must be marked internal and must NOT be copied
   verbatim into a public draft. Summarize the public-safe fact; flag anything that
   cannot be made public with `[ACTION REQUIRED: confirm public-safe wording]`.

## Output

Return a structured context report (do not write it into any doc page):

```
## Context report — <TICKET-KEY>

### Confirmed (source-backed)
- <fact> — source: <link or MCP + where>

### Unconfirmed / missing → [ACTION REQUIRED]
- <what the doc needs but no source confirms>

### Sources checked
- Confluence: <n pages> | Google Docs: <n> | AlphaPatch: checked/not-configured |
  ask-snyk: checked/not-configured | Snyk User Docs MCP: checked/not-configured

### Sensitivity notes
- <anything internal-only that must not appear in a public draft>
```

The calling skill uses the **Confirmed** list as drafting input, turns every
**Unconfirmed** item into an inline `[ACTION REQUIRED]` placeholder, and honors the
**Sensitivity notes** before finalizing.

## Guardrails

- Confirm, don't invent. If no source states a fact, it stays unconfirmed.
- Internal context never lands verbatim in a public page (sensitivity gate).
- Missing MCP servers are a "not checked" note, not an error.
