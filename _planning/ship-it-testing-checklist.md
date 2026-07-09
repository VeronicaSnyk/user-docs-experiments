# Ship-it — testing checklist

Turns the ship-it automation into work you can actually run and verify. Two phases:
**A) local dry-run** (prove the drafting works, no push/secrets/Slack), then
**B) GitHub Actions** (the real pipeline). The branch for all of this is
`feat/ship-it-automation` (pushes to `origin` = the `user-docs-experiments` fork).

The self-checking harness lives at `.docs-agent/test/run-checks.sh` (local-only,
git-ignored). Run it from the repo root any time:

    bash .docs-agent/test/run-checks.sh

---

## Phase A — local dry-run (do this first)

- [ ] **A1. Static checks pass.** Run `bash .docs-agent/test/run-checks.sh` — expect
      skills present, YAML valid, label→mode logic green, key-parse + gate green.
      (Tier 2 shows "skipped" until credentials exist — that's expected.)
- [ ] **A2. Drive the draft with a mock ticket (no credentials).** In an interactive
      `claude` session in this repo:
      > Run /ship-it-new-docs using `.docs-agent/test/mock-DOCT-2618.md` as the
      > ticket. Obey the source-of-truth gate and guardrails, place the page per the
      > section rules, but DO NOT push or open a PR — stop after writing the draft +
      > SUMMARY.md so I can review the diff.
- [ ] **A3. Review the trial output.** `git status && git diff` — check placement,
      that `[ACTION REQUIRED]` appears where the mock lacks detail, and that no
      internal-only content leaked in.
- [ ] **A4. Test the HOLD path.** Repeat A2 with a ticket that has **no** source link
      (delete the "Sources" section from a copy of the mock) — expect it to stop with
      "HELD: no source-of-truth link" and write nothing.
- [ ] **A5. Test the update path.** Run /ship-it-doc-updates against a mock describing
      a change to an existing page; confirm it edits in place and lists changed files.
- [ ] **A6. Clean up trial drafts.** `git restore . && git clean -fdn` (dry-run first),
      then `git clean -fd <trial-dir>` to remove.

## Phase B — GitHub Actions (real pipeline)

Prereqs — you provide (the agent can't create these):

- [ ] **B1. Credentials.** Fill `.docs-agent/.env` (Atlassian token) OR authenticate
      the Atlassian MCP in a terminal `claude` session via `/mcp`. Re-run
      `run-checks.sh` — Tier 2 should now pass and the real fetch works:
      `python .docs-agent/skills/fetch-jira-ticket/scripts/fetch_jira_ticket.py DOCT-2618`
- [ ] **B2. Push the branch to the fork.**
      `git push -u origin feat/ship-it-automation`  (goes to user-docs-experiments)
- [ ] **B3. Create the labels** in the fork (commands in `.github/ship-it-README.md`):
      `ship-it`, `ship-it-new-docs`, `ship-it-doc-updates`, `ship-it-processed`,
      `ship-it-held`, `ship-it-failed`.
- [ ] **B4. Add repo secrets** (Settings → Secrets → Actions):
      `ANTHROPIC_API_KEY`, `SHIP_IT_PAT`, `JIRA_*`, `CONFLUENCE_*`, optional
      `GOOGLE_TOKEN_JSON`. (Full table in `.github/ship-it-README.md`.)
- [ ] **B5. Smoke-test the trigger.** Open a test issue in the fork with label
      `ship-it-new-docs` and a body containing a real DOCT browse URL. Watch the
      Actions run; confirm it comments in-progress → opens a draft PR → comments the
      link and labels `ship-it-processed`.
- [ ] **B6. Verify the guardrails live.** Open a second issue with NO source link →
      expect `ship-it-held` + a comment asking for a link, and no PR.
- [ ] **B7. Jira write-back (if MCP configured in the runner).** Confirm the draft
      PR link is posted back on the Jira ticket; if not configured, confirm it's
      noted (not failed).

## Known blockers (documented, not surprises)

- **Interactive `/mcp` needs a terminal**, not this chat surface — see B1.
- **AlphaPatch / ask-snyk** MCPs are internal; `gather-context` degrades gracefully
  without them.
- **Contentful, `user-docs-staging` repo, promotion Action** — future work, tracked
  in `ai-contentops-roadmap.md`, not part of this test.

## Roll back everything

The whole feature is isolated on `feat/ship-it-automation` and in `.claude/skills`,
`.github/*ship-it*`, `.github/labels.yml`, `.github/ISSUE_TEMPLATE`. To abandon:
`git checkout quality-improvements` and delete the branch; nothing was pushed until B2.
