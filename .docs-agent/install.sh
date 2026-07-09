#!/usr/bin/env bash
#
# install.sh — install the docs-agent into an existing user-docs clone.
# Does NOT clone the repo. Run it pointing at your clone:
#
#   bash /path/to/.docs-agent/install.sh ~/Documents/git/user-docs
#   # ...or from inside the clone with no argument:
#   cd ~/Documents/git/user-docs && bash /path/to/.docs-agent/install.sh
#
set -euo pipefail

EXPECTED_REPO="snyk/user-docs"

# --- Source: where this script (and the .docs-agent payload) lives ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Target: $1 if given, otherwise the current directory ---
TARGET_INPUT="${1:-$PWD}"
if [ ! -d "$TARGET_INPUT" ]; then
  echo "Error: target '$TARGET_INPUT' is not a directory." >&2
  exit 1
fi

# --- Verify the target is a user-docs clone ---
if ! REPO_ROOT="$(git -C "$TARGET_INPUT" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "Error: '$TARGET_INPUT' is not inside a git repository." >&2
  echo "Clone the repo first, then point this script at it:" >&2
  echo "  git clone https://github.com/${EXPECTED_REPO}.git" >&2
  exit 1
fi

ORIGIN="$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || echo '')"
if [[ "$ORIGIN" != *"$EXPECTED_REPO"* ]]; then
  echo "Error: '$REPO_ROOT' does not look like a $EXPECTED_REPO clone." >&2
  echo "  origin = ${ORIGIN:-<none>}" >&2
  exit 1
fi

DEST="$REPO_ROOT/.docs-agent"

# --- Guard against copying the folder onto itself ---
if [ "$SCRIPT_DIR" = "$DEST" ]; then
  echo "docs-agent is already installed at $DEST — nothing to do."
  exit 0
fi

# --- Copy the payload in (exclude any stray secrets, just in case) ---
echo "Installing docs-agent into $DEST ..."
mkdir -p "$DEST"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '.env' \
    --exclude '*token.pickle*' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    "$SCRIPT_DIR"/ "$DEST"/
else
  cp -R "$SCRIPT_DIR"/. "$DEST"/
  rm -f "$DEST/.env"
  find "$DEST" -name '*token.pickle*' -delete 2>/dev/null || true
  find "$DEST" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
fi

# --- Prep a ready-to-edit .env (never overwrite an existing one) ---
ENV_FILE="$DEST/.env"
ENV_EXAMPLE="$DEST/skills/fetch-google-docs/.env.example"
if [ ! -f "$ENV_FILE" ] && [ -f "$ENV_EXAMPLE" ]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "Created $ENV_FILE from the template."
fi

# --- Ensure the repo ignores .docs-agent/ so it (and your .env) is never committed ---
GITIGNORE="$REPO_ROOT/.gitignore"
if [ -f "$GITIGNORE" ] && grep -qE '^\.docs-agent/?$' "$GITIGNORE"; then
  : # already ignored
else
  printf '\n# docs-agent (local tooling + credentials, never commit)\n.docs-agent/\n' >> "$GITIGNORE"
  echo "Added .docs-agent/ to $GITIGNORE"
fi

# --- Hand off ---
cat <<EOF

Done. docs-agent installed at:
  $DEST

Next steps:
  1. Add your credentials — follow .docs-agent/setup/01-tokens.md and edit:
       $ENV_FILE
  2. Install Python dependencies:
       pip3 install requests python-dotenv markdownify google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
  3. Authenticate Google (first run only):
       python3 "$DEST/skills/fetch-google-docs/scripts/fetch_google_docs.py" --auth
  4. Run the workflow — see .docs-agent/setup/02-running-the-prompts.md
EOF
