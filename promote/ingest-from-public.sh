#!/usr/bin/env bash
#
# ingest-from-public.sh — seed / refresh this internal repo's docs from the public
# user-docs ROOT sections, SKIPPING the public docs/ folder (GitBook-owned).
#
# Direction: PUBLIC (snyk/user-docs) -> INTERNAL (this repo, "docs-orb" model).
# This is the inverse of promote-to-public.sh and is used to:
#   - Initially seed the internal repo, or
#   - Pull down any root-section changes made on public (for example the automated
#     sync workflows) so the internal source of truth stays current.
#
# What it does:
#   1. Clones the public repo.
#   2. Copies the public ROOT sections into this repo's docs/ subtree.
#   3. NEVER ingests the public docs/ folder or GitBook plumbing.
#   4. Never touches the internal kitchen (.docs-agent, .claude, orb/, promote/, ...).
#
# Usage:
#   promote/ingest-from-public.sh [--public-repo snyk/user-docs] [--dry-run]

set -euo pipefail

PUBLIC_REPO="snyk/user-docs"
DRY_RUN="false"
WORKDIR=""

log() { printf '  %s\n' "$*" >&2; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --public-repo) PUBLIC_REPO="${2:-}"; shift 2 ;;
    --workdir) WORKDIR="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done

INTERNAL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_DOCS="$INTERNAL_ROOT/docs"

# The canonical ROOT sections on public (the tree you own). docs/ is deliberately
# absent — it is GitBook territory and must not be ingested.
ROOT_SECTIONS=(
  "developer-tools"
  "discover-snyk"
  "platform-administration"
  "scan-fix-and-prevent"
  "snyk-data-and-governance"
  # NOTE: public tools/ is synced Go infrastructure (api-docs-generator), NOT docs
  # content. Intentionally excluded so it is never ingested as if it were content.
)

WORKDIR="${WORKDIR:-$INTERNAL_ROOT/.work/ingest}"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
PUBLIC_CLONE="$WORKDIR/public"

log "cloning public repo: $PUBLIC_REPO"
git clone --depth 1 "https://github.com/$PUBLIC_REPO.git" "$PUBLIC_CLONE" >/dev/null 2>&1 \
  || die "failed to clone https://github.com/$PUBLIC_REPO.git"

RSYNC_FLAGS=(-a --delete --exclude ".DS_Store" --exclude "**/.DS_Store")
[ "$DRY_RUN" = "true" ] && RSYNC_FLAGS+=(--dry-run --itemize-changes)

for section in "${ROOT_SECTIONS[@]}"; do
  if [ -d "$PUBLIC_CLONE/$section" ]; then
    log "ingest: public /$section -> internal docs/$section"
    mkdir -p "$DEST_DOCS/$section"
    rsync "${RSYNC_FLAGS[@]}" "$PUBLIC_CLONE/$section"/ "$DEST_DOCS/$section"/
  else
    log "skip: public /$section not found"
  fi
done

log "NOTE: public docs/ folder intentionally NOT ingested (GitBook-owned)."
[ "$DRY_RUN" = "true" ] && log "dry-run: no files changed."
log "done."
