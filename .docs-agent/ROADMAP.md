# AI ContentOps — docs-agent roadmap

Maps the [AI ContentOps project], the [Staging environment project], and the patterns
in [Basti's harness] to concrete milestones for this repository's docs-agent, and
records what is built today versus what is still a gap.

This is a living planning doc (not published documentation). It is the shareable plan
Bastian offered to review.

## Target architecture (decided)

From the AI ContentOps design plus the Basti/Veronica call (2026-07-08), the decided
direction — which overrides the earlier Vercel/Node-bridge sketch — is:

- **Single intake:** Slack `/ship-it` (global shortcut + channel workflows in
  `#upcoming-releases` / `#ask-docs`). One form, three request types.
- **GitHub is the source of truth.** Drafts land as GitHub PRs. GitBook is being
  phased down; do not build new hard dependencies on it.
- **CI/CD runs the orchestrator** (GitHub Actions / CircleCI, on a schedule or
  `/loop`), not a hosted Vercel service.
- **Jira DOCT ticket per request**, updated with links to every draft.
- **Human-in-the-loop stays** for anything user-facing; low-risk mechanical updates
  (for example the IDE compatibility matrix) may push directly once permissions allow.

### Three request types (Miro board)

| Slack branch | Label | docs-agent behavior | Status |
|---|---|---|---|
| Add new feature docs | `ship-it-new-docs` | Draft a new page | ✅ built |
| Update/improve docs | `ship-it-doc-updates` | Edit existing page(s) | ✅ built |
| Upcoming release | `ship-it-release` | Post to `#upcoming-releases` + optional Contentful Product Update draft | ⛔ not built |

## Built today

- `.github/workflows/ship-it.yml` — issue-triggered (label `ship-it-new-docs` /
  `ship-it-doc-updates`), parses the Jira key, runs Claude Code headlessly, opens a
  draft PR against `main`, reports back on the issue.
- Skills (`.docs-agent/skills/` source + `.claude/skills/` CI copy):
  `ship-it-new-docs`, `ship-it-doc-updates`, `create-draft-pr`, `fetch-jira-ticket`,
  `fetch-confluence`, `fetch-google-docs`, `snyk-docs-writing-rules`,
  `check-broken-links`, and now `gather-context` + `update-jira-ticket`.
- **Guardrails** wired into both ship-it skills and the workflow prompts:
  source-of-truth gate, PRD-only drafting, `[ACTION REQUIRED]` placeholders,
  sensitivity gate, and a "HELD" outcome when no source link exists.

## Gaps → milestones

Ordered to match the AI ContentOps milestones (M1 done, M2/3 in progress, M4 = GA
2026-08-13) and the staging project.

### M2/3 — AI generation & multi-platform sync

1. **Jira write-back (partial).** `update-jira-ticket` skill exists and is invoked,
   but it is best-effort and needs the **Atlassian MCP** configured in the runner to
   actually post. → Register the Atlassian MCP in the CI environment; until then the
   GitHub-issue comment carries the PR link.
2. **Context enrichment (partial).** `gather-context` exists but the **AlphaPatch /
   ask-snyk** MCPs are internal and not registered here. → Wire them in the internal
   runner; the skill already degrades gracefully without them.
3. **Third intake — release announcement.** Add `ship-it-release`: structured
   `#upcoming-releases` post + optional Contentful Product Update draft. Depends on
   Contentful API access (not available today) — defer the Contentful half.
4. **GitBook multi-section CRs.** A single feature can span several GitBook site
   sections, each needing its own CR. The existing PR→CR skill covers this; keep it
   as the GitBook bridge while GitBook is still in use.

### Staging environment (parallel track)

The [Staging environment project] decisions change where drafts land:

- **Internal `user-docs-staging` repo** (ProdSec-approved: keep prod public, add an
  internal staging repo). All PRs/CRs happen in staging; a **promotion Action**
  moves passing content to public prod. Merging into staging before publish is **not**
  allowed, so promotion can be automated on tests-pass.
- **CI gates before promotion:** Vale style, broken-link + missing-section checks,
  alt-text enforcement, and **Legal approval** on Legal pages. This repo already has
  `docs-quality.yml`, `link-checker.yml`, `image-audit.yml` and the `.github/scripts`
  to build on.
- **Action:** once `user-docs-staging` exists, make `ship-it.yml`'s PR target
  configurable (staging repo/branch) instead of hard-coded `main`. Tracked as a
  config knob; **not** wired yet (only-what-runs-today).

### M4 — hardening & GA (2026-08-13)

- Run the orchestrator on a schedule / `/loop` instead of purely issue-triggered, so
  tickets that arrive without a GitHub issue are still picked up.
- Quality gate in CI that **fails a PR** when docs changes do not meet the style
  rules (Bastian's "check-docs" idea) — reuse `snyk-docs-writing-rules` + Vale.
- Skill quality: run the official **skill-creator** plugin over these skills; add
  good/bad input evals.
- Success metrics to instrument: cycle-time reduction (≥30%), AI draft acceptance
  (≥70% by month 3), adoption (≥60% by month 2), pipeline completion (≥95%).

## Deliberately out of scope (today)

- Contentful drafting (no API access here).
- The `user-docs-staging` repo and promotion Action (infra not created yet).
- A hosted Vercel/Node bridge (superseded by CI/CD per the call).

[AI ContentOps project]: https://snyksec.atlassian.net/wiki/spaces/Docs/pages/4508712971/AI+ContentOps+project
[Staging environment project]: https://snyksec.atlassian.net/wiki/spaces/Docs/pages/4737237006/Staging+environment+project
[Basti's harness]: https://snyksec.atlassian.net/wiki/spaces/IDE/pages/4835541040/Basti+s+harness
