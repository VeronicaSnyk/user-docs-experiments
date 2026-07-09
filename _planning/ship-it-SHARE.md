# Ship-it docs automation — state & how to use it

**For:** Docs team + AI ContentOps stakeholders reviewing before we move to an
official Snyk org repo.
**Status:** Working pilot on a personal fork. Not merged, not yet org-hosted.
**Repo:** `VeronicaSnyk/user-docs-experiments`, branch `feat/ship-it-automation`.

---

## What this is

The docs half of the [AI ContentOps project](https://snyksec.atlassian.net/wiki/spaces/Docs/pages/4508712971/AI+ContentOps+project):
a Slack `/ship-it` request turns into a **draft docs PR**, with a Jira ticket as the
source of truth. It takes a ticket, reads its linked PRD/spec/Confluence/Google Docs,
drafts (or updates) the page in Snyk's writing style, and opens a **draft PR** for a
Technical Writer to review — so we polish instead of rewrite.

It runs two ways:
1. **In GitHub Actions** — a ship-it issue (labelled by the Slack app) triggers a
   workflow that drafts headlessly and opens the PR.
2. **Locally / in a terminal** — the same skills, run by hand against a ticket. This
   is how the pilot is tested today.

## What works today

- ✅ Two request types, driven by the Slack app's labels:
  `ship-it-new-docs` → draft a new page; `ship-it-doc-updates` → edit existing page(s).
- ✅ **Guardrails** (from the AI ContentOps must-haves): drafts only from the
  provided sources; marks gaps with `[ACTION REQUIRED: …]` instead of inventing;
  **holds** (no draft) if a ticket has no source link; keeps internal-only content
  out of public drafts.
- ✅ 10 skills committed, incl. `ship-it-new-docs`, `ship-it-doc-updates`,
  `gather-context` (context enrichment), `update-jira-ticket` (writes the PR link
  back to Jira), and the `snyk-docs-writing-rules` style guide.
- ✅ Jira + Confluence + GitBook reachable via MCP.
- ✅ Proven on one real ticket (DOCT-2619): it renamed the experimental page to GA,
  updated the section TOC, and correctly flagged the unknown access-steps as
  `[ACTION REQUIRED]` rather than guessing.

## Honest limitations (please weigh these in your review)

- ⚠️ **On a personal fork, not a Snyk org repo.** The org move happens after your
  approval. Nothing here is merged to `snyk/user-docs`.
- ⚠️ **Setup is per-person and partly manual** (see below) — not yet one-command.
- ⚠️ **Only new-docs is battle-tested.** The HOLD path, the update path, Jira
  write-back, and the full GitHub Actions run still need real-world testing.
- ⚠️ **Drafts are starting points, not finished pages** — a Technical Writer always
  reviews, and `[ACTION REQUIRED]` markers must be filled before merge.
- ⚠️ **Internal enrichment (AlphaPatch / ask-snyk) not wired** — the `gather-context`
  skill works without them; they're a later add.

## How to try it (local, ~15 min setup)

Prereqs: macOS, the `claude` CLI, Python 3, `gh` CLI, and a Snyk Atlassian account.

1. **Clone the pilot** (the `.docs-agent/` engine and `.claude/skills` come with it —
   no separate install needed; `.docs-agent/install.sh` is only for adding the agent
   to a *different* clone and will refuse a non-`snyk/user-docs` origin, so skip it):
   ```bash
   git clone https://github.com/VeronicaSnyk/user-docs-experiments.git
   cd user-docs-experiments && git checkout feat/ship-it-automation
   ```
2. **Fix corporate SSL** (Zscaler/Netskope break Node's cert trust) — one time:
   ```bash
   security find-certificate -a -p /Library/Keychains/System.keychain > ~/.config/claude-certs/corporate-ca.pem
   echo 'export NODE_EXTRA_CA_CERTS="$HOME/.config/claude-certs/corporate-ca.pem"' >> ~/.zshrc
   source ~/.zshrc
   ```
3. **Connect Jira/Confluence** (browser login):
   ```bash
   claude mcp add atlassian --scope user --transport sse https://mcp.atlassian.com/v1/sse
   claude          # then in the session: /mcp → atlassian → Authenticate
   ```
4. **Install Python deps:**
   ```bash
   pip3 install requests python-dotenv markdownify google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
5. **Sanity check:**
   ```bash
   bash .docs-agent/test/run-checks.sh      # expect all green except optional Tier 2
   ```

Full step-by-step (incl. troubleshooting): `.docs-agent/test/TERMINAL-SETUP.md`.

## Run a draft

In an interactive `claude` session in the repo:

```
Run /ship-it-new-docs for <JIRA-KEY>. Fetch the ticket via the Atlassian MCP,
obey the source-of-truth gate and guardrails, place the page per the section
rules, and open a DRAFT PR against main.
```

For an update to existing docs, use `/ship-it-doc-updates` instead. To just try it
safely without opening a PR, add: "stop after writing the files so I can review."

## The GitHub Actions path (for the eventual org repo)

`.github/workflows/ship-it.yml` triggers on an issue labelled `ship-it-new-docs` /
`ship-it-doc-updates`, drafts with Claude Code, and opens the PR. To enable it you
create the labels and add repo secrets (`ANTHROPIC_API_KEY`, `JIRA_*`, etc.) — see
`.github/ship-it-README.md`. We'll wire this up properly in the org repo.

## Where the full plan lives

- Target architecture, milestones, gaps: `_planning/ai-contentops-roadmap.md`
- Testing checklist: `_planning/ship-it-testing-checklist.md`
- Slack-app ↔ GitHub contract + secrets: `.github/ship-it-README.md`

## What I'm asking you to review

1. Does the **flow** (Slack → Jira → draft PR → TW review) match what you expect?
2. Are the **guardrails** (source-of-truth, `[ACTION REQUIRED]`, sensitivity) right?
3. Any concern before we **move this to an official Snyk org repo** and open it up?
