#!/usr/bin/env bash
# Prepare the Atlassian MCP for authentication.
#
# This script does the parts that CAN be automated (register the server, verify it).
# It CANNOT do the OAuth login itself — that happens interactively inside `claude`
# via /mcp, which needs your browser. The script ends by telling you exactly what to
# type next.
#
# Run from anywhere:  bash .docs-agent/test/setup-atlassian-mcp.sh

set -uo pipefail
REPO="/Users/veronicacernea/Desktop/user-docs-2026"
cd "$REPO" || { echo "repo not found at $REPO"; exit 1; }

# --- Corporate SSL fix (Zscaler/Netskope TLS inspection) -----------------------
# The claude CLI runs on Node, which uses its own CA list and does NOT trust the
# corporate root certs that re-sign inspected HTTPS traffic. Without this, the CLI
# fails with "SSL certificate verification failed". We export the macOS system
# keychain (which DOES trust the corporate roots) into a PEM bundle and point Node
# at it. This is the "fix the CA-cert path" step from Basti's harness.
CADIR="$HOME/.config/claude-certs"
BUNDLE="$CADIR/corporate-ca.pem"
if [ ! -s "$BUNDLE" ]; then
  echo "0/2 · Building corporate CA bundle for Node (one-time)…"
  mkdir -p "$CADIR"
  security find-certificate -a -p /Library/Keychains/System.keychain > "$BUNDLE" 2>/dev/null
  security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain >> "$BUNDLE" 2>/dev/null
  echo "     wrote $(grep -c 'BEGIN CERTIFICATE' "$BUNDLE") certs to $BUNDLE"
fi
export NODE_EXTRA_CA_CERTS="$BUNDLE"
# Persist for future shells (idempotent).
if ! grep -q "NODE_EXTRA_CA_CERTS.*claude-certs" "$HOME/.zshrc" 2>/dev/null; then
  printf '\n# Trust corporate SSL-inspection CAs for Node CLIs like claude\nexport NODE_EXTRA_CA_CERTS="%s"\n' "$BUNDLE" >> "$HOME/.zshrc"
  echo "     added NODE_EXTRA_CA_CERTS to ~/.zshrc"
fi

echo "1/2 · Ensuring the atlassian MCP server is registered (USER scope = every dir)…"
if claude mcp get atlassian >/dev/null 2>&1; then
  echo "     already registered."
else
  # User scope so it shows in /mcp no matter which directory `claude` starts from.
  claude mcp add atlassian --scope user --transport sse https://mcp.atlassian.com/v1/sse
fi

echo
echo "2/2 · Current status (✗ is expected until you authenticate):"
claude mcp list 2>&1 | grep -E "atlassian|gitbook" || true

cat <<'NEXT'

──────────────────────────────────────────────────────────────
NEXT — do this interactively (the script can't drive your browser):

  1. Start an interactive Claude session IN THIS REPO:

        cd /Users/veronicacernea/Desktop/user-docs-2026 && claude

  2. Inside that session, type:

        /mcp

  3. Select  atlassian  →  Authenticate (Login)  →  finish in the browser
     as your @snyk.io account. Wait for  ✓ Connected.

  4. Quit that session (Ctrl-D or /exit). The token is now stored globally.

VERIFY (back in a normal shell):

        claude mcp list        # atlassian should show ✓ Connected

Then the mcp__atlassian__* tools are available to any NEW claude session in
this repo (existing sessions must restart to pick them up).
──────────────────────────────────────────────────────────────
NEXT
