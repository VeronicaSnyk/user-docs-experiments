---
name: update-jira-ticket
description: Write documentation artifact links back to the source Jira ticket after a draft PR is created. Adds a comment (and, where configured, updates a field) linking the GitHub PR / GitBook CR to the ticket so tracking is centralized. Use at the end of ship-it-new-docs / ship-it-doc-updates. Best-effort — skips cleanly when the Atlassian MCP is not configured.
license: Proprietary
metadata:
  author: veronica.cernea
  version: "1.0.0"
  category: automation
---

# Update Jira Ticket

**Trigger:** Invoked at the end of `ship-it-new-docs` / `ship-it-doc-updates`, after
`create-draft-pr` has produced a PR URL.

Delivers the AI ContentOps outcome *"Automated Jira ticket per request, updated with
links to all drafts"*: once a draft exists, the source ticket should point to it so
Product Ops and the Docs team can track a request without hunting across platforms.

## Inputs

- Jira ticket key (for example `DOCT-2618`).
- The draft PR URL (and any GitBook CR URL, if one was created).
- A one-line summary of what was drafted (new page vs. update; files touched).

## What it does

1. **Detect the Atlassian MCP.** Look for `mcp__atlassian__*` (or the configured
   Jira MCP) in the available tools.
   - **If present:** add a comment to the ticket, and if the project defines a
     "Docs draft" / "PR link" field, set it.
   - **If absent:** skip. Record "Jira not updated (Atlassian MCP not configured)"
     so the calling skill notes it in the PR body. Never fail the run.

2. **Post a concise, public-safe comment** on the ticket:

   ```
   📝 Docs draft ready
   - PR: <github-pr-url> (draft, targets main)
   - GitBook CR: <cr-url or "n/a">
   - Scope: <new page | update> — <short summary>
   - [ACTION REQUIRED] items in the draft: <count or "none">
   A Technical Writer reviews after the PR is moved from Draft to Ready.
   ```

3. **Do not change ticket status or assignee.** Commenting/linking only — status
   transitions stay with the human process (matches the harness rule that the
   workflow "does not change the Jira ticket status").

## Guardrails

- Best-effort and idempotent: if a "Docs draft ready" comment with the same PR URL
  already exists, do not post a duplicate.
- Public-safe: the comment must not contain internal-only content that the
  sensitivity gate flagged.
- Never blocks the pipeline — a Jira failure is reported, not fatal.

## Notes

The Atlassian MCP requires interactive OAuth in some environments and may be absent
in headless CI. When unavailable, the PR link is still surfaced by the comment the
`ship-it.yml` workflow posts on the triggering GitHub issue, so tracking is not lost.
