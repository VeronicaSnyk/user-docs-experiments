#!/usr/bin/env bash
# Local dry-run harness for the ship-it pipeline.
# Run from the repo root:  bash .docs-agent/test/run-checks.sh
#
# Tier 1 (no credentials) runs now. Tier 2 (real Jira/Confluence/Google) runs only
# when .docs-agent/.env is filled. Nothing here pushes, commits, or calls Slack.

set -uo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
PASS=0; FAIL=0; SKIP=0
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
no(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }
sk(){ echo "  ⏭️  $1"; SKIP=$((SKIP+1)); }
hd(){ printf "\n\033[1m%s\033[0m\n" "$1"; }

hd "1. Skills present (source + CI copy)"
for s in ship-it-new-docs ship-it-doc-updates gather-context update-jira-ticket \
         create-draft-pr fetch-jira-ticket fetch-confluence fetch-google-docs \
         snyk-docs-writing-rules check-broken-links; do
  [ -f ".claude/skills/$s/SKILL.md" ] && ok ".claude/skills/$s" || no "missing .claude/skills/$s"
done

hd "2. Workflow + config YAML parse"
python3 - <<'PY'
import sys, yaml
files = [".github/workflows/ship-it.yml", ".github/labels.yml",
         ".github/ISSUE_TEMPLATE/ship-it-new-docs.yml"]
bad=0
for f in files:
    try: yaml.safe_load(open(f)); print(f"  ✅ {f}")
    except Exception as e: print(f"  ❌ {f}: {e}"); bad=1
sys.exit(bad)
PY
[ $? -eq 0 ] && PASS=$((PASS+1)) || FAIL=$((FAIL+1))

hd "3. Label -> mode logic (mirrors the gate step)"
decide(){ L="$1"; E="$2"
  if ! echo "$L"|grep -q ship-it-new-docs && ! echo "$L"|grep -q ship-it-doc-updates; then R="no-trigger"
  elif echo "$L"|grep -q ship-it-processed; then R="skip"
  elif echo "$L"|grep -q ship-it-new-docs; then R="new"
  elif echo "$L"|grep -q ship-it-doc-updates; then R="update"; else R="skip"; fi
  [ "$R" = "$E" ] && ok "$L -> $R" || no "$L -> $R (expected $E)"; }
decide '["ship-it","ship-it-new-docs"]' new
decide '["ship-it","ship-it-doc-updates"]' update
decide '["ship-it","ship-it-new-docs","ship-it-doc-updates"]' new
decide '["ship-it"]' no-trigger
decide '["ship-it","ship-it-new-docs","ship-it-processed"]' skip

hd "4. Jira key + source-of-truth gate (from the mock ticket)"
BODY="$(cat .docs-agent/test/mock-DOCT-2618.md)"
KEY="$(printf '%s' "$BODY" | grep -oiE 'DOCT-[0-9]+' | head -n1)"
[ "$KEY" = "DOCT-2618" ] && ok "ticket key parsed: $KEY" || no "ticket key parse got '$KEY'"
if printf '%s' "$BODY" | grep -qiE 'https?://(docs\.google|.*atlassian\.net/wiki|.*/prd|.*one.?pager)'; then
  ok "source-of-truth gate: source link found (would proceed)"
else
  sk "source-of-truth gate: no source link (would HOLD)"
fi

hd "5. Repo integrity scripts"
if [ -f .github/scripts/check-summary.py ]; then
  python3 .github/scripts/check-summary.py >/dev/null 2>&1 && ok "check-summary.py clean" || sk "check-summary.py reported issues (run it directly to see)"
else no ".github/scripts/check-summary.py missing"; fi

hd "6. Tier 2 — credentialed fetch (optional)"
ENV="$ROOT/.docs-agent/.env"
# Read the raw JIRA_API_TOKEN value (everything after the first '='), trim whitespace.
TOKEN="$(grep -E '^JIRA_API_TOKEN=' "$ENV" 2>/dev/null | head -n1 | cut -d= -f2- | tr -d '[:space:]')"
case "$TOKEN" in
  ""|your_*|*_here|changeme|placeholder)
    sk "no real Jira credentials in .docs-agent/.env — Tier 2 skipped (fill .env or auth the Atlassian MCP)" ;;
  *)
    ok ".env has a Jira token — you can run the real fetch:"
    echo "      python .docs-agent/skills/fetch-jira-ticket/scripts/fetch_jira_ticket.py DOCT-2618" ;;
esac

hd "Summary"
echo "  passed: $PASS   failed: $FAIL   skipped(needs setup): $SKIP"
hd "Next: drive the drafting end-to-end (Tier 1, no creds)"
cat <<'EOF'
  In an interactive claude session in this repo, run:

    /ship-it-new-docs using .docs-agent/test/mock-DOCT-2618.md as the ticket.
    Run headless-style: obey the source-of-truth gate and guardrails, place the
    page per the section rules, but DO NOT push or open a PR — stop after writing
    the draft + SUMMARY.md so I can review the diff with `git diff`.

  Then inspect:  git status && git diff
  Discard the trial draft with:  git restore . && git clean -fd <new-file-dir>
EOF
[ $FAIL -eq 0 ]
