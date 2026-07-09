# How the docs-agent works: running the prompts

This guide explains how to use the docs-agent to turn a Jira ticket into a draft documentation pull request. It covers what the docs-agent is, the prerequisites, the prompts that start the workflow, what happens at each step, what you need to do, and the final outcome.

## What the docs-agent is

The docs-agent is a set of [Agent Skills](https://agentskills.io/specification) in the `.docs-agent/` directory. Together, they take a Jira ticket labeled `ship-it-new-docs`, gather every source the ticket references, find where the new content belongs in the Snyk docs, write a style-compliant draft, and open a GitHub draft PR for a Technical Writer to review.

The workflow orchestrates these skills:

| Skill | Role |
| --- | --- |
| `ship-it-new-docs` | The orchestrator. Runs the end-to-end workflow. |
| `fetch-jira-ticket` | Fetches ticket summary, description, comments, and links. |
| `fetch-confluence` | Fetches Confluence pages referenced by the ticket. |
| `fetch-google-docs` | Fetches Google Docs referenced by the ticket. |
| `snyk-docs-writing-rules` | Snyk's voice, formatting, and terminology rules. |
| `create-draft-pr` | Commits, pushes, and opens the draft PR. |
| `check-broken-links` | Validates cross-references (optional, run on demand). |

## Prerequisites

Complete these once. The fastest path is to ask the agent to *"set up the docs-agent"* and let it work through the list with you, but here is everything it checks.

### The one part you must do yourself: credentials

> **Important: the orchestrator cannot create your credentials for you.** Filling in `.docs-agent/.env` with your Atlassian API token, your Google OAuth client ID and client secret, and your Google project ID is the **only** manual prerequisite. These are personal secrets that you generate in the Atlassian and Google consoles while logged in as yourself. The agent has no way to obtain them on your behalf, and it will not ask you to paste secrets into the chat.

> **Everything else is automatable.** If you ask the agent to *"set up the docs-agent"*, it can install the Python dependencies, install and configure the GitHub CLI, fix a broken CA-certificate path, move aside a stale Google token, switch the git remote to HTTPS, and run the Google and GitHub login flows for you (you still click through the browser and enter your own passphrase or login). The split is simple:

| You do (once) | The agent can do |
| --- | --- |
| Generate the Atlassian API token | Install Python dependencies |
| Create the Google OAuth client (ID, secret, project ID) | Install and authenticate `gh` |
| Paste those values into `.docs-agent/.env` | Run `fetch_google_docs.py --auth` (you complete the browser step) |
| | Fix the CA-cert path, switch the remote to HTTPS, and more |

> Refer to [01-tokens.md](01-tokens.md) to set up the API tokens.

## How to start the workflow: the prompts

The trigger is a Jira ticket with the label `ship-it-new-docs`. With the prerequisites in place, start the workflow with a prompt like:

- **‼️ First-time setup:** `set up the docs-agent`

After this step is completed successfully, use the command(s) below.

- **Run the workflow:** `run ship-it-new-docs for DOCT-1234`
- Equivalent phrasings: `start the docs workflow for DOCT-1234`, or paste the ticket URL.

> ‼️ You do not need to invoke each skill yourself. The orchestrator calls them in order.

## What happens next, and what you do

The agent runs the steps below. Most are automatic. The "You do" column marks the points where the agent pauses for your input, which usually happens only on the first run.

| # | The agent does | You do |
| --- | --- | --- |
| 1 | Fetches the Jira ticket: summary, description, comments, labels, and any links. | Nothing. |
| 2 | Extracts referenced URLs and fetches each Confluence page and Google Doc. | Complete the Google browser login the first time only. |
| 3 | Searches existing docs to find placement and comparable pages. | Nothing. |
| 4 | Applies the Snyk writing rules. | Nothing. |
| 5 | Generates a clean, merge-ready draft (no metadata in the file). | Review the content and the proposed placement. |
| 6 | Creates the `.md` file inside the matching top-level section folder (e.g. `scan-fix-and-prevent/`) and adds an entry to **that section's** `SUMMARY.md`. | Confirm the placement looks right. |
| 7 | Commits the change to the current branch. | Nothing. |
| 8 | Pushes the branch to GitHub. | Run `gh auth login` the first time if you have not already. |
| 9 | Invokes `create-draft-pr` to open the PR in draft mode against `main`. | Nothing. |

A few things worth knowing while it runs:

- **The draft file is clean.** Metadata such as source ticket, references, and placement goes into the PR description, not the published page. Keep the page merge-ready.
- **Placement matters.** If the feature is already documented, the agent flags the overlap so you can decide whether to add a new page or fold the content into the existing one.
- **You stay in control of git.** The agent commits and pushes only as part of this workflow. It does not merge or change the Jira ticket.

## Outcome

When the workflow finishes you have:

- A new documentation page in the matching section folder (user-docs is a multi-space GitBook — documentation lives in a fixed set of top-level section folders: `developer-tools/`, `discover-snyk/`, `platform-administration/`, `scan-fix-and-prevent/`, `snyk-data-and-governance/` — each with its own `SUMMARY.md`, located via `find . -maxdepth 2 -name SUMMARY.md`; the agent never creates a new top-level folder). **Agent security** content (Snyk Studio, Agent Scan, Agent Guard) has no root folder yet and instead lives under `docs/integrations/snyk-studio-agentic-integrations/`, registered in `docs/SUMMARY.md`.
- An updated `SUMMARY.md` **in that same section folder** (or `docs/SUMMARY.md` for Agent security content) listing the new page in its table of contents.
- A commit on your branch and the branch pushed to GitHub.
- A **draft pull request** against the `main` branch, with the Jira ticket key and title, and a description containing the source ticket, references, related pages, and any reviewer notes.

A Technical Writer reviews the documentation after you move the PR from **Draft** to **Ready for review**.

### What the workflow does not do

- It does not merge the PR.
- It does not change the Jira ticket status or add a comment.
- It does not edit published docs outside the new page and its `SUMMARY.md` entry.

## Skills reference

Each skill is self-contained under `.docs-agent/skills/`. You can run the fetch skills directly when you want to inspect a source.

```bash
# Fetch a Jira ticket (formatted, or raw JSON with --json)
python3 .docs-agent/skills/fetch-jira-ticket/scripts/fetch_jira_ticket.py DOCT-1234

# Fetch a Confluence page by URL, ID, or search
python3 .docs-agent/skills/fetch-confluence/scripts/fetch_confluence.py <url-or-id>

# Fetch a Google Doc as Markdown
python3 .docs-agent/skills/fetch-google-docs/scripts/fetch_google_docs.py <google-doc-url>
```

The `snyk-docs-writing-rules` skill is reference material the agent applies automatically. Its key files are `references/terms-and-pairs.md` (canonical spellings) and `references/screenshots-and-diagrams.md` (visual guidelines).

---

**Hit an error?** See [03-troubleshooting.md](03-troubleshooting.md).
