# MCP servers + plugins for the docs-agent

Status of every MCP server / plugin from Basti's harness, and how to add each.
All `claude mcp add` commands use `--scope user` so the server shows in `/mcp`
from any directory. Prereq for all: the corporate CA fix must be active
(`NODE_EXTRA_CA_CERTS` in `~/.zshrc` — see setup-atlassian-mcp.sh).

Authenticate OAuth servers interactively: start `claude`, run `/mcp`, pick the
server, Authenticate, finish in the browser.

## Ready / done

| Server | Status | Notes |
|---|---|---|
| `atlassian` | ✅ Connected | Jira + Confluence. OAuth done. |
| `gitbook` (official) | ⏳ Needs auth | `mcp.gitbook.com/mcp`. Run `/mcp` → authenticate. |
| `gitbook-documentation` | ✅ Connected | Hosted read-only Snyk published docs. |

## Internal — need endpoint + auth from Basti / IDE team

These power the `gather-context` skill (enrichment). They are **internal Snyk MCP
servers**; their URLs/auth are not public, so ask Basti for them. `gather-context`
already degrades gracefully until they exist — no code change needed to add them.

### AlphaPatch

Ask Basti: *"What's the AlphaPatch MCP endpoint URL, transport (http/sse), and how
do I authenticate — OAuth or a token/header?"* Then run one of:

```bash
# OAuth or bare HTTP endpoint:
claude mcp add --scope user --transport http alphapatch <ALPHAPATCH_URL>

# Token in a header:
claude mcp add --scope user --transport http alphapatch <ALPHAPATCH_URL> \
  --header "Authorization: Bearer <TOKEN>"
```

### ask-snyk

Same ask to Basti for the ask-snyk endpoint, then:

```bash
claude mcp add --scope user --transport http ask-snyk <ASK_SNYK_URL>
# ...or with --header "Authorization: Bearer <TOKEN>" if token-based.
```

After adding either, authenticate via `/mcp` if it's OAuth, and confirm with
`claude mcp list` (look for ✓ Connected). Then `gather-context` will use them
automatically.

## skill-creator (plugin, not an MCP)

Basti's recommendation to improve/evaluate skills. Install from the official Claude
plugin marketplace in an interactive `claude` session:

```
/plugin
```

Then browse the official marketplace, find **skill-creator**, and install. Use it to
review the ship-it skills:

> Use skill-creator to review .claude/skills/ship-it-new-docs and suggest
> improvements; evaluate it against good/bad input examples.

## Verify everything

```bash
claude mcp list        # all servers; want ✓ Connected (or ! Needs authentication → run /mcp)
```
