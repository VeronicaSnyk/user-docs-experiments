# Terminal runbook — finish MCP + plugin setup

Everything below runs in the VS Code integrated terminal (or any macOS terminal).
Open a FRESH terminal first so the corporate-CA fix (NODE_EXTRA_CA_CERTS in ~/.zshrc)
is loaded. Sanity check:

    echo "$NODE_EXTRA_CA_CERTS"     # must print a path ending in corporate-ca.pem
    # if empty:  source ~/.zshrc

Current state (2026-07): atlassian ✓ connected, gitbook ! needs auth,
gitbook-documentation ✓ connected.

────────────────────────────────────────────────────────────────────────
## 1. GitBook (official) — authenticate

The server is already added. It just needs OAuth. Two ways:

### Option A — interactive (reliable)
    cd /Users/veronicacernea/Desktop/user-docs-2026
    claude
    # then in the session:
    /mcp
    # pick  gitbook  → Authenticate → finish in browser → wait for ✓ Connected
    # then /exit

### Option B — token instead of OAuth (fully non-interactive)
Create a Personal Access Token at https://app.gitbook.com/account/developer
(looks like gb_api_...), then:

    claude mcp remove gitbook -s user
    claude mcp add --scope user --transport http gitbook https://mcp.gitbook.com/mcp \
      --header "Authorization: Bearer gb_api_YOUR_TOKEN"

Verify:
    claude mcp list | grep gitbook        # want ✓ Connected

────────────────────────────────────────────────────────────────────────
## 2. skill-creator plugin — fully terminal

List marketplaces, add the official one if missing, then install:

    claude plugin marketplace list
    # if the official Anthropic marketplace isn't listed, add it:
    claude plugin marketplace add anthropics/claude-code

    # install skill-creator (use plugin@marketplace if names clash):
    claude plugin install skill-creator

    # confirm:
    claude plugin list

Then use it in a session:
    claude
    > Use skill-creator to review .claude/skills/ship-it-new-docs and suggest
      improvements; evaluate it against good and bad input examples.

────────────────────────────────────────────────────────────────────────
## 3. AlphaPatch (internal) — need endpoint from Basti

Ask Basti: "AlphaPatch MCP — endpoint URL, transport (http/sse), and auth
(OAuth or token/header)?" Then ONE of:

    # OAuth / bare endpoint:
    claude mcp add --scope user --transport http alphapatch <URL>

    # token in header:
    claude mcp add --scope user --transport http alphapatch <URL> \
      --header "Authorization: Bearer <TOKEN>"

If OAuth: authenticate via `claude` → `/mcp` → alphapatch.
Verify:  claude mcp list | grep alphapatch

────────────────────────────────────────────────────────────────────────
## 4. ask-snyk (internal) — need endpoint from Basti

Same as AlphaPatch:

    claude mcp add --scope user --transport http ask-snyk <URL>
    #   ...add --header "Authorization: Bearer <TOKEN>"  if token-based
    #   ...then /mcp to authenticate if OAuth

Verify:  claude mcp list | grep ask-snyk

Once alphapatch + ask-snyk are ✓, the gather-context skill uses them automatically.

────────────────────────────────────────────────────────────────────────
## Final check

    claude mcp list       # atlassian, gitbook, (alphapatch, ask-snyk) → ✓ Connected
    claude plugin list     # skill-creator present
