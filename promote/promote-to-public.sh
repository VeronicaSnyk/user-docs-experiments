#!/usr/bin/env bash
#
# promote-to-public.sh — publish internal docs content to the public user-docs repo.
#
# Repurposed-docs-orb model:
#   - This (internal) repo is the source of truth: docs content + the "internal
#     kitchen" (skills, scripts, workflows, the orb/ tree, .docs-agent, .claude).
#   - The public repo (snyk/user-docs) is a content-only frontend gate. The kitchen
#     never leaves this repo.
#
# What this script does:
#   1. Clones the public target repo into a scratch dir.
#   2. Mirrors THIS repo's docs/ subtree onto the public repo ROOT (the public repo
#      keeps sections at root: developer-tools/, discover-snyk/, ... — NOT under docs/).
#   3. Copies an explicit allowlist of publishable root files (README, SUMMARY, etc.).
#   4. Excludes the entire kitchen by construction (allowlist, not denylist).
#   5. Commits on a branch and pushes; opening the PR is done by the caller / Action.
#
# It is deliberately one-way (internal -> public) and never merges. A human + CI on
# the public side review the PR. Safe to run repeatedly: rsync --delete keeps the
# public tree an exact mirror of the internal docs/ subtree.
#
# Usage:
#   promote/promote-to-public.sh \
#     --public-repo snyk/user-docs \
#     --branch promote/2026-07-10 \
#     [--internal-docs-dir docs] \
#     [--dry-run]
#
# Requires: git, rsync, and (for the caller's PR step) gh with a token that can push
# to the public repo.

set -euo pipefail

PUBLIC_REPO=""
BRANCH=""
INTERNAL_DOCS_DIR="docs"
DRY_RUN="false"
WORKDIR=""

log() { printf '  %s\n' "$*" >&2; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --public-repo) PUBLIC_REPO="${2:-}"; shift 2 ;;
    --branch) BRANCH="${2:-}"; shift 2 ;;
    --internal-docs-dir) INTERNAL_DOCS_DIR="${2:-}"; shift 2 ;;
    --workdir) WORKDIR="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done

[ -n "$PUBLIC_REPO" ] || die "--public-repo is required (e.g. snyk/user-docs)"
[ -n "$BRANCH" ]      || die "--branch is required (e.g. promote/2026-07-10)"

# Resolve internal repo root (this script lives in <root>/promote/).
INTERNAL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DOCS="$INTERNAL_ROOT/$INTERNAL_DOCS_DIR"
[ -d "$SRC_DOCS" ] || die "internal docs dir not found: $SRC_DOCS"

# --- Canonical ROOT sections (allowlist) ------------------------------------
# The content you own. These live under internal docs/<section> and publish to the
# public repo ROOT as /<section>. The public docs/ folder is GitBook-owned and is
# deliberately absent here, so it is never written. Keep in sync with
# ingest-from-public.sh's ROOT_SECTIONS.
ROOT_SECTIONS=(
  "developer-tools"
  "discover-snyk"
  "platform-administration"
  "scan-fix-and-prevent"
  "snyk-data-and-governance"
  # NOTE: public tools/ is synced Go infrastructure (api-docs-generator), NOT docs
  # content. It is intentionally excluded so this pipeline never overwrites it.
)

# --- Publishable ROOT files (allowlist) -------------------------------------
# Kitchen dirs (.docs-agent, .claude, orb, tools, promote, _planning, user-docs-agent)
# are NOT listed, so they can never leak into public. Add publishable root files here.
ROOT_ALLOWLIST=(
  "README.md"
  "SECURITY.md"
  "catalog-info.yaml"
)

# --- Paths that must NEVER be written to public, even if they appear internally ---
# Defense-in-depth on top of the allowlist. CRITICAL: the public repo's docs/ tree
# is GitBook-owned (has .gitbook.yaml + SUMMARY.md and is connected to GitBook Git
# Sync). This promotion targets the public ROOT sections only and must leave GitBook
# territory completely untouched. `--filter` protects those paths from --delete too.
RSYNC_EXCLUDES=(
  --exclude ".DS_Store"
  --exclude "**/.DS_Store"
  --exclude ".git/"
)

# Protect GitBook-owned paths at the public root from being deleted or overwritten,
# even though we rsync onto the root. `P` = protect from deletion, `-` after excludes
# them as sources. Order matters: protect rules come before the transfer.
GITBOOK_PROTECT=(
  --filter "protect /docs/***"
  --filter "protect /.gitbook/***"
  --filter "protect /.gitbook.yaml"
  --filter "protect /SUMMARY.md"
)

WORKDIR="${WORKDIR:-$INTERNAL_ROOT/.work/promote}"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
PUBLIC_CLONE="$WORKDIR/public"

log "cloning public repo: $PUBLIC_REPO"
git clone --depth 1 "https://github.com/$PUBLIC_REPO.git" "$PUBLIC_CLONE" >/dev/null 2>&1 \
  || die "failed to clone https://github.com/$PUBLIC_REPO.git"

cd "$PUBLIC_CLONE"
git checkout -b "$BRANCH" >/dev/null 2>&1 || git checkout "$BRANCH" >/dev/null 2>&1

# 1) Mirror ONLY the canonical ROOT sections, one at a time, internal -> public root.
#    Section-scoped (not a whole-docs/ mirror) so GitBook plumbing stored inside the
#    internal docs/ (docs/.gitbook/, docs/SUMMARY.md, docs/.gitbook.yaml) is never
#    dragged to the public root. --delete is per-section, so a page removed from a
#    section internally is removed from that section on public — and nothing else.
#    GITBOOK_PROTECT is retained as defense-in-depth.
for section in "${ROOT_SECTIONS[@]}"; do
  if [ -d "$SRC_DOCS/$section" ]; then
    log "mirroring docs/$section -> public /$section"
    mkdir -p "$PUBLIC_CLONE/$section"
    rsync -a --delete "${GITBOOK_PROTECT[@]}" "${RSYNC_EXCLUDES[@]}" \
      "$SRC_DOCS/$section"/ "$PUBLIC_CLONE/$section"/
  else
    log "skip: internal docs/$section not present"
  fi
done

# 2) Copy allowlisted root files (these live at internal root, not under docs/).
for f in "${ROOT_ALLOWLIST[@]}"; do
  if [ -f "$INTERNAL_ROOT/$f" ]; then
    log "copying root file: $f"
    cp "$INTERNAL_ROOT/$f" "$PUBLIC_CLONE/$f"
  fi
done

# 3) Show what changed.
git add -A
if git diff --cached --quiet; then
  log "no changes to promote — public is already up to date."
  exit 0
fi

log "changed files:"
git --no-pager diff --cached --stat >&2

if [ "$DRY_RUN" = "true" ]; then
  log "dry-run: not committing or pushing."
  exit 0
fi

git -c user.name="docs-promotion-bot" \
    -c user.email="docs-bot@users.noreply.github.com" \
    commit -m "docs: promote content from internal source of truth" >/dev/null

log "pushing branch $BRANCH to $PUBLIC_REPO"
git push -u origin "$BRANCH" --force-with-lease

log "done. Open a PR: gh pr create --repo $PUBLIC_REPO --head $BRANCH"
