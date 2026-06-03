# Docs assistant

Turns a technical spec (PRD, one-pager, slides) into a style-guide-compliant **GitBook Change
Request (draft)**. It runs two ways:

1. **Headless pipeline** (`scripts/run-pipeline.ts`) — invoked by
   [`.github/workflows/docs-ship-it.yml`](../../.github/workflows/docs-ship-it.yml) when the
   Slack `/ship-it` workflow fires. This is the automated path.
2. **Browser UI** (`npm run dev`) — an optional manual tool for one-off drafting.

Both apply [`snyk-style-guide.md`](snyk-style-guide.md), and apply the extra
[`cli-style-rules.md`](cli-style-rules.md) whenever a generated page targets a CLI-help path.

## Pipeline flow

```
Slack /ship-it form
  └─(Webhook step)──▶ GitHub repository_dispatch (event_type: docs-ship-it)
                        │
                        ▼
   docs-ship-it.yml ─▶ run-pipeline.ts
        generate (style guide + CLI rules)
          └▶ guardrails.classifyPages   (BLOCKED / PATH_LOCKED / NEEDS_TEAM_APPROVAL / OK)
               └▶ GitBook createDraft    (only OK + NEEDS_TEAM_APPROVAL pages)
                    └▶ notify Slack + comment on Jira ticket  ──▶ draft URL
```

## Guardrails

The CLI/IDE doc guide says several pages are synced to or from other repos. The pipeline enforces
this **before** writing anything to GitBook (see [`core/guardrails.ts`](core/guardrails.ts) and
[`core/paths.ts`](core/paths.ts)):

| Verdict | Pages | Behavior |
| --- | --- | --- |
| `BLOCKED` | IDE plugin compatibility matrix | Dropped — automation owns it; never edit. |
| `PATH_LOCKED` | A synced page proposed as new/renamed | Dropped — changing a synced page's source path breaks the sync. |
| `NEEDS_TEAM_APPROVAL` | CLI help, Getting started CLI, top-level IDE READMEs (in-place update) | Drafted, but flagged with the owning team (Team CLI / Team IDE); limit to typos/formatting. |
| `OK` | Ordinary pages | Drafted normally. |

The Slack/Jira message lists every outcome so reviewers know when a draft is partial.

## Local use

```bash
npm ci

# Dry run — generate + classify, no GitBook write, no notifications:
GEMINI_API_KEY=… node --experimental-strip-types scripts/run-pipeline.ts \
  --spec "Feature: add --json output to snyk code test" --space closed-beta --dry-run

# Real run — creates a GitBook Change Request:
GEMINI_API_KEY=… GITBOOK_API_TOKEN=… node --experimental-strip-types scripts/run-pipeline.ts \
  --spec "…" --space closed-beta

# Unit tests (guardrails + path detection):
npm test
```

Copy [`.env.example`](.env.example) to `.env.local` for the browser UI. **Never commit tokens.**

## GitBook spaces

| Key | Space | ID |
| --- | --- | --- |
| `closed-beta` | Closed Beta Docs | `Y2VjeSnjL1hm69oRmP5s` |
| `public` | Public User Docs | `-MdwVZ6HOZriajCf5nXH` |

> Default to `closed-beta` for review-first drafting. Confirm these IDs against your GitBook org
> before relying on them in production.

## Required secrets (GitHub Actions)

Set these in the repo's Actions secrets — never in code:

- `GEMINI_API_KEY` — Google GenAI key for generation.
- `GITBOOK_API_TOKEN` — GitBook token used to create the Change Request.
- `SLACK_BOT_TOKEN` — bot token with `chat:write`, to post the draft URL back to Slack.
- `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` — to comment the draft URL on the ship-it ticket.

## Slack `/ship-it` integration (Workflow Builder)

`/ship-it` is a Slack **Workflow Builder** multi-step form, not an API. It already creates the
Jira ticket. To hand the spec to this pipeline and get the GitBook draft URL back onto the ticket:

1. **Add a "Send a webhook" step** to the `/ship-it` workflow, after the form collects the spec.
2. Point it at GitHub's `repository_dispatch` endpoint:
   - **URL:** `https://api.github.com/repos/<owner>/user-docs/dispatches`
   - **Method:** `POST`
   - **Headers:** `Authorization: Bearer <fine-grained PAT with "Contents: read" + "repository_dispatch" />`,
     `Accept: application/vnd.github+json`
   - **Body:**
     ```json
     {
       "event_type": "docs-ship-it",
       "client_payload": {
         "spec": "{{form spec field}}",
         "slidesUrl": "{{form slides field}}",
         "space": "closed-beta",
         "requester": "{{person who started the workflow}}",
         "slackChannel": "{{channel id}}",
         "jiraIssueKey": "{{Jira ticket key from the create-issue step}}"
       }
     }
     ```
3. The PAT lives only in Slack's webhook step config (a Slack secret), never in this repo.

### Known constraint

Workflow Builder webhook steps are **fire-and-forget** — they cannot block on our response to
feed a later step. So the draft URL is delivered **back** by the pipeline:

- It **posts to `slackChannel`** (so the requester sees it in Slack), and
- if `jiraIssueKey` is provided, it **comments the draft URL on that Jira ticket**.

If the `/ship-it` form creates the Jira ticket *after* the webhook step (so the key isn't
available yet), pass only `slackChannel` and have the requester paste the URL onto the ticket, or
move the Jira-create step before the webhook so its key can be forwarded.
