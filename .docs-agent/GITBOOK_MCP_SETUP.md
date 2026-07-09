# GitBook MCP — setup & usage

> **UPDATE (2026-07): now using GitBook's OFFICIAL hosted MCP.**
> We switched from the self-hosted `lucasbenevinuto/gitbook-mcp` server (described
> below) to GitBook's first-party hosted MCP. No build/clone to maintain, OAuth
> instead of a token:
>
> ```bash
> claude mcp add --scope user --transport http gitbook https://mcp.gitbook.com/mcp
> ```
> Then authenticate in an interactive `claude` session via `/mcp` (browser OAuth),
> exactly like the Atlassian MCP. Docs: https://gitbook.com/docs/getting-started/ai-documentation/gitbook-mcp
>
> The `.docs-agent/mcp/gitbook-mcp/` build is retired and can be deleted. The safety
> rule below (do NOT edit Git-synced content through any GitBook MCP — it corrupts
> links/headings; edit via the repo/Git Sync) STILL APPLIES to the official server.
> If the official MCP turns out not to expose comment/review reading, the self-hosted
> server below remains the fallback for review work.
>
> --- historical (self-hosted) setup follows ---

Connect Claude Code to GitBook so you can **read change requests, comments, reviews, and page content** directly (e.g. pull every reviewer comment on a CR, with the page + section each one is anchored to).

Server used: **[lucasbenevinuto/gitbook-mcp](https://github.com/lucasbenevinuto/gitbook-mcp)** (39 tools — spaces, pages, change requests, reviews, comments). The popular `npx gitbook-mcp` (rickysullivan) is content-only and **cannot** read comments, so don't use that one for review work.

> ⚠️ **Read the "Important limitation" section before you edit any content.** Use this MCP for *reading* (and optionally comment replies/resolves). Do **not** edit page content through it — it corrupts internal links and heading levels. Edit content through Git Sync (the repo) or the GitBook editor.

---

## Prerequisites

- Node ≥ 18, npm, git, Claude Code CLI
- A **GitBook API token** — create one at <https://app.gitbook.com/account/developer> (Settings → Developer → API tokens). It looks like `gb_api_…`.

## Setup (one time)

### 1. Clone & build the server
Keep it inside the gitignored `.docs-agent/` toolkit dir so nothing leaks into the repo:

```bash
git clone https://github.com/lucasbenevinuto/gitbook-mcp .docs-agent/mcp/gitbook-mcp
cd .docs-agent/mcp/gitbook-mcp
npm install
npm run build      # produces dist/index.js
```

### 2. Register with Claude Code (local scope = private, token never committed)

```bash
claude mcp add gitbook --scope local \
  --env GITBOOK_API_TOKEN=gb_api_YOUR_TOKEN \
  --env GITBOOK_DEFAULT_ORG_ID=-M4tdxG8qotLgGZnLpFR \
  --env GITBOOK_DEFAULT_SPACE_ID=<YOUR_USER_DOCS_SPACE_ID> \
  -- node "$(pwd)/dist/index.js"
```

- `--scope local` stores the config (and your token) in your private `~/.claude.json` — it is **not** shared or committed.
- `GITBOOK_DEFAULT_ORG_ID` / `GITBOOK_DEFAULT_SPACE_ID` are optional defaults (see "Finding IDs" below). `GITBOOK_DEFAULT_ORG_ID` above is the Snyk org — change as needed. **`GITBOOK_DEFAULT_SPACE_ID` has no single correct value for user-docs:** each top-level section (`developer-tools`, `discover-snyk`, `platform-administration`, `scan-fix-and-prevent`, `snyk-data-and-governance`) is its own GitBook space with its own space ID. Set it to the space ID of the section you are working in (see "Finding IDs" below), or omit it and pass the space ID per request.

### 3. Verify

```bash
claude mcp list      # gitbook → ✓ Connected
```

The tools (`mcp__gitbook__*`) load into a session **at startup**. If you added the server mid-session, **restart Claude Code** (or run `/mcp` and reconnect) so the tools appear.

---

## Finding the IDs

Open the page or change request in GitBook and read the URL:

```
https://app.gitbook.com/o/<ORG_ID>/s/<SPACE_ID>/~/changes/<CR_NUMBER>/...
                          └ org ┘     └ space ┘            └ CR # ┘
```

- **Org ID** — after `/o/`
- **Space ID** — after `/s/`
- **Change request** — the number after `/~/changes/` (e.g. `12`). The MCP accepts the number or the internal CR id.

## Usage examples (prompt Claude Code)

- "List the open change requests in space `<SPACE_ID>`."
- "Get change request 12 in space `<SPACE_ID>` and list every comment with its author, the page and section it's anchored to, and whether it's resolved."
- "Show the page content for `<page path>` in change request 12."

Useful tools: `list_change_requests`, `get_change_request`, `list_comments`, `list_comment_replies`, `list_reviews`, `get_page_by_path`, `search_space_content`.

> Tip: comment bodies and the page tree come back as GitBook's JSON. Ask Claude to "flatten the comment bodies to plain text and resolve each comment's `target.page.id` / `target.node.id` to a page title + nearest heading" — that gives you a clean, locate-able list.

---

## ⚠️ Important limitation — do NOT edit content through the API/MCP

GitBook's content API (`update_page` / markdown import, which the MCP's content tools use) is **not a faithful round-trip**:

- It **strips internal page links** (cross-page links become plain text). Links only survive when submitted as GitBook JSON `ref` nodes, not markdown.
- It **shifts heading levels** (the page title gets absorbed into the body, demoting every heading).

If a GitBook space is **Git-synced** (ours syncs from `github.com/snyk/user-docs`), make content edits in the **git repo** (markdown links work through Git Sync) or in the **GitBook editor** — not through this MCP. If something does get edited by mistake, GitBook's **per-page version history** in the editor restores it perfectly (text, headings, and links).

**Safe to do via the MCP:** read CRs/comments/reviews/content, post comment replies, resolve comments.
**Not safe:** editing page bodies.

---

## Paste-ready prompt for a teammate

> Set up the GitBook MCP for me in Claude Code. Clone `https://github.com/lucasbenevinuto/gitbook-mcp` into `.docs-agent/mcp/gitbook-mcp`, run `npm install` and `npm run build`, then register it with `claude mcp add gitbook --scope local` passing `GITBOOK_API_TOKEN` (I'll provide it / it's in `.docs-agent/.env`), and my org and space IDs as `GITBOOK_DEFAULT_ORG_ID` / `GITBOOK_DEFAULT_SPACE_ID`, with command `node <abs path>/dist/index.js`. Verify with `claude mcp list`, then remind me to restart Claude Code so the tools load. Do NOT use it to edit page content — only to read change requests and comments.
