#!/usr/bin/env bash
#
# package-for-sharing.sh — build a secret-free docs-agent-share.zip for the team.
# Run from the repo root:  bash .docs-agent/package-for-sharing.sh
#
# Excludes live secrets (.env, *token.pickle*), build junk (__pycache__, *.pyc),
# and this packaging script itself. install.sh and the setup/ guides ARE included.
#
set -euo pipefail

if [ ! -d ".docs-agent" ]; then
  echo "Error: run this from the repo root (no .docs-agent/ here)." >&2
  exit 1
fi

OUT="docs-agent-share.zip"
rm -f "$OUT"

zip -r "$OUT" .docs-agent \
  -x '.docs-agent/.env' \
  -x '*token.pickle*' \
  -x '*/__pycache__/*' \
  -x '*.pyc' \
  -x '*.DS_Store' \
  -x '.docs-agent/package-for-sharing.sh'

echo
echo "Built $OUT"
echo "Verify it contains no secrets before sharing:"
echo "  unzip -l $OUT | grep -E '\\.env$|token.pickle' || echo 'clean'"
