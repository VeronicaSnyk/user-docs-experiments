# Docs promotion: internal source of truth → public frontend gate

This directory holds the pipeline that publishes documentation **content** from this
internal repo to the public [`snyk/user-docs`](https://github.com/snyk/user-docs)
repo, while keeping the "internal kitchen" (skills, scripts, workflows, the `orb/`
tree, `.docs-agent`, `.claude`) private to this repo.

## Architecture (per the AI ContentOps + Staging environment plan)

```
INTERNAL (this repo) = source of truth        PUBLIC user-docs = frontend gate
  docs/<section>/...   ── promote (PR) ──►       <section>/...    (root, no docs/ prefix)
  .docs-agent/  ┐                          ◄── ingest ──  (root sections only)
  .claude/      │  internal kitchen
  orb/          │  never leaves this repo         PUBLIC docs/  = GitBook-owned,
  promote/      ┘                                  NEVER touched in either direction
```

- **Canonical content = ROOT sections.** `developer-tools/`, `discover-snyk/`,
  `platform-administration/`, `scan-fix-and-prevent/`, `snyk-data-and-governance/`.
  On public these live at the **repo root**; internally they live under `docs/<section>`.
- **Public `docs/` is GitBook territory.** It has `.gitbook.yaml` + `SUMMARY.md` and
  is connected to GitBook Git Sync. The pipeline **never reads it in (ingest) nor
  writes to it (promote)** — protected by `--filter protect` and by syncing only the
  named sections, not the whole `docs/` subtree.
- **`tools/` excluded.** Public `tools/` is synced Go infrastructure
  (`api-docs-generator`), not docs content — never promoted or ingested.
- **One-way promotion.** Content flows internal → public via a PR; never auto-merges.
- **Allowlist, not denylist.** Only the named sections + a few root files publish, so
  the kitchen can't leak by construction.
- **Two pipelines, one repo.** If this repo also publishes the CircleCI orb from
  `orb/`, the promotion workflow is path-scoped so a docs change never triggers an orb
  publish and an `orb/` change never triggers a promotion.

## Files

| File | Purpose |
|---|---|
| `promote-to-public.sh` | Clones public repo, mirrors each ROOT section `docs/<section>` → public `/<section>`, copies allowlisted root files, commits + pushes a branch. Protects public `docs/` + GitBook plumbing. |
| `ingest-from-public.sh` | Seeds/refreshes internal `docs/<section>` from public ROOT sections. **Skips public `docs/`** (GitBook-owned). |
| `../.github/workflows/promote-to-public.yml` | Runs promotion on push to `main`, gated by quality checks, then opens the PR. |

## One-time setup

1. **Target repo variable** — set `PUBLIC_DOCS_REPO` (repo variable). While
   validating, point it at your fork (`VeronicaSnyk/user-docs-experiments`);
   flip to `snyk/user-docs` for production.
2. **Push token** — add secret `PUBLIC_DOCS_PUSH_TOKEN`: a PAT or GitHub App
   installation token with `contents:write` + `pull_requests:write` on the public repo.
3. **Wire the gate** — replace the placeholder `gate` job with `uses:` of your
   existing `docs-quality.yml`, `link-checker.yml`, `image-audit.yml`. Promotion is
   blocked unless the gate passes.

## Validate locally (safe, no push)

```bash
promote/promote-to-public.sh \
  --public-repo VeronicaSnyk/user-docs-experiments \
  --branch promote/test \
  --dry-run
```

This prints the exact `--stat` diff that *would* be pushed. Confirm:
- Section folders land at the public **root** (not under `docs/`).
- No kitchen paths (`.docs-agent`, `.claude`, `orb`, `promote`, `_planning`,
  `tools`, `user-docs-agent`) appear in the diff.

## Promotion criterion

A change is ready for real promotion when a `--dry-run` diff is clean (content only,
correct root mapping) **twice in a row**, and the quality gate passes.
