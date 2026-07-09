# /ship-it → GitHub Actions

The Slack **/ship-it** app turns an upcoming-release submission into a **draft docs PR**.
This document is the contract between that Slack app and this repository.

## Labels: base + variant

The Slack app applies the base **`ship-it`** label to every ticket it creates,
plus **one variant** depending on the workflow branch the submitter chose:

| Variant label | Workflow mode | What it does |
|---|---|---|
| `ship-it-new-docs` | **new** | Drafts a brand-new page via the `ship-it-new-docs` skill |
| `ship-it-doc-updates` | **update** | Locates and edits the existing page(s) for the feature |

The workflow triggers on **either variant** (the base `ship-it` label is
informational and not required). If both variants are somehow present, **new**
wins — creating a page is the safer default to review.

## Flow

```
Slack /ship-it  ──opens──▶  GitHub issue
                            labels: ship-it + (ship-it-new-docs | ship-it-doc-updates)
                                     │
                                     ▼  on: issues [opened, labeled]
                       .github/workflows/ship-it.yml
                                     │
              parses Jira key + mode ──▶ runs Claude Code (new page | edit existing)
                                     │
                                     ▼
                       draft PR against main  ──▶  comments link on the issue
```

The official Claude Slack app cannot own a custom slash command or dispatch a
workflow, so the trigger is an **issue**, not a Slack-to-Claude call. Your existing
`/ship-it` app is responsible only for creating the issue below.

## What the Slack app must do

When someone runs `/ship-it`, the app opens a GitHub issue in this repo:

- **Labels:** `ship-it` **plus** the variant for the chosen branch —
  `ship-it-new-docs` **or** `ship-it-doc-updates`. The variant is the trigger filter.
- **Title:** anything; `Ship It: <feature>` is conventional
- **Body:** must contain the Jira browse URL so the workflow can read the ticket key:

  ```
  Jira issue: https://snyksec.atlassian.net/browse/DOCT-2618
  ```

  The rest of the Slack submission (Feature, Description, Release Date, Category,
  Release Type, FedRAMP, Affected Product Areas, Resources, Submitted by) can be
  included verbatim — see [ISSUE_TEMPLATE/ship-it-new-docs.yml](ISSUE_TEMPLATE/ship-it-new-docs.yml)
  for the exact field layout. Only the Jira URL is required for the workflow to run.

### Creating the issue from the Slack app

Use the GitHub REST API with a token that has `issues: write` on this repo:

```http
POST /repos/<owner>/user-docs/issues
{
  "title": "Ship It: CLI v1.1306.0",
  "labels": ["ship-it", "ship-it-new-docs"],
  "body": "Feature: CLI v1.1306.0\n... \nJira issue: https://snyksec.atlassian.net/browse/DOCT-2618\n..."
}
```

Use `ship-it-doc-updates` instead of `ship-it-new-docs` for the update branch.

The workflow parses the **first** `atlassian.net/browse/<KEY>` link (falling back
to the first bare `PROJECT-####` token) and normalizes it to upper case.

## One-time repo setup

1. **Create the labels** (used as the trigger + status markers):

   ```bash
   gh label create ship-it             --color 5319E7 --description "Created by the Slack /ship-it app"
   gh label create ship-it-new-docs    --color 1D76DB --description "Variant: draft a new page"
   gh label create ship-it-doc-updates --color 0052CC --description "Variant: update existing docs"
   gh label create ship-it-processed   --color 0E8A16 --description "Workflow already ran"
   gh label create ship-it-held        --color FBCA04 --description "Held: no source-of-truth link; add one and re-label"
   gh label create ship-it-failed      --color B60205 --description "Workflow errored; needs a human"
   ```

   (Definitions also live in [labels.yml](labels.yml).)

2. **Add repository secrets** (Settings → Secrets and variables → Actions):

   | Secret | Purpose |
   |---|---|
   | `ANTHROPIC_API_KEY` | Runs Claude Code in the action |
   | `SHIP_IT_PAT` | PAT (repo + workflow scope) used to open the PR so CI checks run on it. Falls back to the default token if you prefer, but then the PR won't trigger the docs-quality checks. |
   | `JIRA_BASE_URL` | e.g. `https://snyksec.atlassian.net` |
   | `JIRA_EMAIL` | Account the Jira token belongs to |
   | `JIRA_API_TOKEN` | Atlassian API token (Jira) |
   | `CONFLUENCE_BASE_URL` | e.g. `https://snyksec.atlassian.net/wiki` |
   | `CONFLUENCE_EMAIL` | Account the Confluence token belongs to |
   | `CONFLUENCE_API_TOKEN` | Atlassian API token (same value as Jira works) |
   | `GOOGLE_TOKEN_JSON` | *(optional)* Pre-authorized Google OAuth token JSON for headless Google Docs fetches. If absent, Google Docs sources are skipped and noted in the PR. |

3. **Skills in CI:** the workflow reads the committed skills under
   [.claude/skills/](../.claude/skills/) (`ship-it-new-docs`, `create-draft-pr`,
   `fetch-jira-ticket`, `fetch-confluence`, `fetch-google-docs`,
   `snyk-docs-writing-rules`). The local, git-ignored `.docs-agent/` copy is for
   interactive runs; keep the two in sync when the skills change.

## Headless caveats (differ from an interactive run)

- **No prompts.** The interactive "sync your clone" checkpoint and the placement
  confirmation are skipped; the checkout is already current and the action states
  the chosen placement in the PR body for a human to confirm at review.
- **Google Docs** needs a pre-seeded `GOOGLE_TOKEN_JSON` because OAuth's browser
  step can't run in CI. Without it, those sources are skipped (not fatal).
- **The Snyk User Docs MCP** used interactively for doc search is not wired into
  the action. Placement uses the in-repo `SUMMARY.md` files and the skill's fixed
  section rules. To add MCP search in CI, pass `--mcp-config` in `claude_args`.

## Content guardrails

Per the AI ContentOps project, the workflow enforces:

- **Source of truth.** The ticket must reference a PRD / one-pager / spec /
  Confluence / Google Docs link. With none, the run is **held** (labeled
  `ship-it-held`, commented on the issue) rather than drafting from nothing.
- **No fabrication.** Drafts use only the provided sources; anything unspecified
  becomes an inline `[ACTION REQUIRED: …]` placeholder. The PR body reports how many
  remain.
- **Sensitivity gate.** Internal-only content is kept out of public drafts.
- **Jira write-back.** After the PR opens, `update-jira-ticket` links it on the
  source ticket (best-effort; needs the Atlassian MCP in the runner).

See [_planning/ai-contentops-roadmap.md](../_planning/ai-contentops-roadmap.md) for
the full target architecture and remaining gaps (Contentful, staging repo, internal
MCPs).

## Result

- New page in the matching section folder, that section's `SUMMARY.md` updated.
- A **draft PR against `main`**, titled `<KEY>: <title>`, body noting the source
  issue and the chosen placement.
- A comment on the triggering issue linking the PR, and the issue relabeled
  `ship-it-processed` (or `ship-it-failed` with a link to the run log).
