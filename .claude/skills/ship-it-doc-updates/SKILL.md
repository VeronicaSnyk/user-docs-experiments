---
name: ship-it-doc-updates
description: End-to-end workflow for UPDATING existing documentation from a Jira ticket. Fetches the ticket, retrieves referenced Confluence/Google Docs, locates the existing page(s) the change affects, edits them in place following Snyk writing rules, commits, and creates a GitHub draft PR with metadata. Use when a Jira ticket has the label ship-it-doc-updates (the update branch of the Slack /ship-it app), or when a feature change modifies docs that already exist rather than needing a brand-new page.
license: Proprietary
compatibility: Requires Python 3.x, Jira/Confluence/Google Docs credentials in .env, Snyk User Docs MCP server, GitHub CLI
metadata:
  author: veronica.cernea
  version: "1.0.0"
  category: documentation
---

# Ship It - Doc Updates

**Trigger:** Use this skill when a Jira ticket has the label `ship-it-doc-updates`.

This is the **update** counterpart to `ship-it-new-docs`. Where that skill creates a
brand-new page, this skill finds the documentation that **already exists** for a
feature and edits it in place. Use it when a change modifies behavior, adds an
option, deprecates something, or otherwise touches content that already has a home.

This skill orchestrates the complete end-to-end workflow for updating documentation:
0. Checks the local clone is current with `main` and offers to sync if behind
1. Fetches the Jira ticket details
2. Extracts and retrieves all referenced Confluence and Google Docs URLs
3. **Locates the existing page(s)** the change affects
4. **Edits those page(s) in place**, applying Snyk writing rules
5. Updates the section `SUMMARY.md` **only if** a title/path/hierarchy changed
6. Commits the changes to a new branch
7. **Automatically invokes `create-draft-pr`** to create a GitHub PR in draft mode with metadata

> **New page vs. update.** If, after searching, the change genuinely has no existing
> home, stop and switch to the `ship-it-new-docs` skill instead — do not force an
> unrelated page to absorb the content. Creating a new page is the fallback, not the
> default, for this skill.

## Content guardrails (must follow)

Non-negotiable rules from the AI ContentOps project, applied to every edit:

1. **Provided sources are the only source of truth.** Base each edit ONLY on the
   Jira ticket and the links it references (PRD, one-pager, spec, Confluence, Google
   Docs). Do not invent changed behavior, new field names, or limits from prior
   knowledge.
2. **Mark gaps, never fabricate.** When the sources do not specify a detail the edit
   needs, insert an inline `[ACTION REQUIRED: <what is missing>]` placeholder rather
   than guessing.
3. **Sensitivity gate before finalizing.** Do not introduce internal-only content
   (internal URLs/paths, unreleased dates, customer names, internal Confluence
   excerpts) into public pages. When unsure, use an `[ACTION REQUIRED: confirm
   public-safe wording]` placeholder.

## Workflow

### Step 0: Ensure the local clone is current with `main`

Which existing pages you find, and the new branch, are both derived from local
state, so a stale clone causes edits to the wrong version or merge conflicts. Run
this check first.

1. Switch to `main` with a clean working tree:
   ```bash
   git switch main && git status --short   # working tree must be clean
   ```
2. Fetch and measure how far behind the clone is:
   ```bash
   git fetch origin
   git rev-list --count main..origin/main   # commits on origin/main missing locally
   ```
3. If the count is `0`, the clone is current — proceed to Step 1.
4. If the count is greater than `0`, WARN the user: state how many commits behind
   the clone is, and show what changed in the likely product folder:
   ```bash
   git diff --stat main origin/main -- <likely-product-folder>/
   ```
   Then ASK whether to sync before continuing:
   - If the user agrees: `git pull --ff-only origin main`, then proceed.
   - If the user declines: proceed on the stale clone, and have `create-draft-pr`
     add a line to the PR description noting the branch was cut from a clone N
     commits behind `origin/main`.

> **Headless (CI) note:** when running non-interactively (for example from the
> `ship-it.yml` GitHub Action), skip the questions in this step — the checkout is
> already current — and proceed straight to Step 1.

### Step 0.5: Source-of-truth gate

An update must be grounded in a source. The ticket description itself can be the
source for a small correction, but any substantive change needs a PRD / one-pager /
spec / Confluence / Google Docs link.

- If the change is substantive and **no** source link is present: hold and ask for
  one (interactive), or stop with "held: no source-of-truth link" and have the
  workflow comment on the issue (headless). Do not invent the changed behavior.
- If a source is present (link or a sufficiently specific ticket description),
  continue. Every edit must trace to it (see **Content guardrails** above).

### Step 1: Fetch Jira Ticket
```bash
python .docs-agent/skills/fetch-jira-ticket/scripts/fetch_jira_ticket.py <TICKET-KEY>
```

Review the ticket for what actually changed:
- **Summary**: The feature or behavior that changed
- **Description**: What is new, changed, or removed — and the user impact
- **Comments**: Stakeholder clarifications, scope changes, late additions
- **Attachments**: Updated screenshots, diagrams, before/after states
- **URLs**: Links to Confluence pages or Google Docs with the detailed spec

### Step 2: Fetch Referenced URLs

Extract all URLs from the ticket description and comments that point to:
- Confluence: `https://snyksec.atlassian.net/wiki/...`
- Google Docs: `https://docs.google.com/document/...`

For each Confluence URL:
```bash
python .docs-agent/skills/fetch-confluence/scripts/fetch_confluence.py <URL>
```

For each Google Docs URL:
```bash
python .docs-agent/skills/fetch-google-docs/scripts/fetch_google_docs.py <URL>
```

> If a Google Docs URL is referenced but Google auth is not configured (for example
> in CI without a pre-seeded token), skip that source and note the omission in the
> PR body — do not fail the run.

### Step 2.5: (Optional) Enrich context

If the ticket is thin, invoke the `gather-context` skill to cross-check it against
AlphaPatch / ask-snyk / Confluence and surface what is confirmed vs. missing. It
degrades gracefully when those MCPs are absent. Unconfirmed details become
`[ACTION REQUIRED]` placeholders, and its output passes the sensitivity gate.

### Step 3: Locate the existing page(s) to edit

This is the core of the update workflow. **Find the documentation that already
covers this feature before you change anything.**

**Repository structure (user-docs):** a multi-space GitBook repo. Documentation
lives in a fixed set of top-level section folders, each its own GitBook space with
its own `SUMMARY.md`. Confirm the current sections with:
```bash
find . -maxdepth 2 -name SUMMARY.md
```

Search widely, then narrow:

1. **Search by feature/product/command/UI names** from the ticket:
   ```bash
   # Prose, headings, and command names
   grep -ril "<feature name>" developer-tools discover-snyk platform-administration \
     scan-fix-and-prevent snyk-data-and-governance docs 2>/dev/null
   # CLI flags, API fields, config keys mentioned in the ticket
   grep -rin -- "--<flag>" .            # exact flag/option
   ```
2. **Use the Snyk User Docs MCP** (`mcp__snyk-user-docs__searchDocumentation`,
   `mcp__snyk-user-docs__getPage`) to search published docs by topic and read
   candidate pages. (Not available in CI; there, rely on `grep`/`Glob` and the
   `SUMMARY.md` files.)
3. **Check the relevant `SUMMARY.md`** for the section to see how pages are titled
   and nested, which surfaces sibling pages the change may also touch.

Produce a short, explicit **candidate list** of files before editing, for example:
```
scan-fix-and-prevent/scan-with-snyk/snyk-container/analyze-and-fix-container-images.md
scan-fix-and-prevent/scan-with-snyk/snyk-container/README.md
```
State which page is the primary target and which are secondary. If the search
returns nothing plausible, this is a new-page case — see the callout at the top and
switch to `ship-it-new-docs`.

### Step 4: Apply Snyk Writing Rules

Before editing, review the **snyk-docs-writing-rules** skill so the edited text
matches Snyk's style:
- Voice and tone (active voice, present tense, imperative for actions)
- Formatting (sentence case headings, bold UI elements)
- Terminology (product names, technical terms — see `references/terms-and-pairs.md`)
- Screenshots and diagrams (`references/screenshots-and-diagrams.md`)

### Step 5: Edit the existing page(s) in place

Make **scoped, surgical edits** — change only what the ticket describes.

- Edit the primary page first, then any secondary pages the change affects.
- Preserve the page's existing structure, heading levels, front matter
  (`description:`), includes, and asset references. Do not reflow or reformat
  unrelated sections.
- Update procedures, tables, option lists, prerequisites, and examples to match the
  new behavior. Remove content the ticket deprecates.
- Keep the diff minimal and reviewable — a Technical Writer should be able to see
  exactly what changed and why.
- If the change renames a page, moves it, or adds/removes a page, update that
  section's `SUMMARY.md` accordingly (relative path, indentation, and ordering
  matching the siblings). If only body content changed, `SUMMARY.md` needs no edit.

**IMPORTANT:** Do NOT add metadata (source ticket, references, placement) into the
documentation files. That metadata goes in the PR description via `create-draft-pr`.

### Step 6: Save metadata for PR creation

Track, for the PR description:
- Jira ticket key / title / URL
- **Every file changed and a one-line reason for each**
- References (Confluence / Google Docs URLs)
- Whether this was a pure content update or also changed `SUMMARY.md`
- Any source skipped (for example Google Docs without auth) or any staleness caveat

## Validation Checklist

Before finalizing:
- [ ] Confirmed local main is current with origin/main (or recorded the staleness caveat)
- [ ] All URLs from the Jira ticket fetched and reviewed
- [ ] Produced an explicit candidate list and confirmed the correct page(s)
- [ ] Edits are scoped to the ticket — no unrelated rewrites
- [ ] **Applied snyk-docs-writing-rules** (active voice, present tense, sentence case, etc.)
- [ ] **Checked terminology** against `snyk-docs-writing-rules/references/terms-and-pairs.md`
- [ ] Preserved existing structure, front matter, includes, and asset references
- [ ] Updated `SUMMARY.md` only if a title/path/hierarchy changed
- [ ] Confirmed no broken internal links were introduced (see `check-broken-links`)
- [ ] **Saved metadata** (files changed + reasons, source, references) for `create-draft-pr`

## Final Steps: Commit and Create PR

After completing the edits, **automatically proceed** to create a GitHub pull request:

1. **Create a branch off `main`** and commit the changes. Name the branch
   `ship-it/<JIRA-KEY>` (the ticket key, matching the `ship-it.yml` workflow, which
   creates and looks up the branch as `ship-it/<TICKET>`):
   ```bash
   git checkout -b ship-it/<JIRA-KEY> main
   git add <changed files...>
   git commit -m "Update [area] documentation for [JIRA-KEY]"
   ```

2. **Push the branch** to remote:
   ```bash
   git push -u origin ship-it/<JIRA-KEY>
   ```

3. **Automatically invoke the `create-draft-pr` skill** to open the PR in draft mode
   against `main` with all metadata. In the PR description, include the list of files
   changed and the reason for each so the Technical Writer can review the scope.

**Headless (CI) outcome contract:** when running non-interactively (from
`ship-it.yml`), after the draft PR is opened, write `done` to a file named
`.ship-it-outcome` at the repo root. If instead you held at the source-of-truth gate
(no source for a substantive change), write `held` to `.ship-it-outcome` and stop.
The workflow reads this file to decide whether to report success or hold.

4. **Automatically invoke the `update-jira-ticket` skill** to write the PR link back
   to the source ticket. Best-effort: skipped and noted if the Atlassian MCP is not
   configured, never failing the run.

## Gotchas

- The workflow reads the local clone, not remote `main`; Step 0 guards against stale
  clones but only fast-forwards when you approve.
- Do not create a new page to hold an update — find the existing home first, and fall
  back to `ship-it-new-docs` only when there truly is none.
- Keep the diff small; large incidental reformatting hides the real change from review.
- The Snyk User Docs MCP searches published docs, not drafts in progress, and is not
  available in CI — use `grep`/`Glob` and the `SUMMARY.md` files there.
- A change can touch more than one page (a feature page plus a README or an overview);
  check siblings before finalizing.
- Always check ticket comments for late scope changes.

## Example

**Jira ticket DOCT-2618 with label `ship-it-doc-updates`:**
- Summary: "CLI v1.1306.0 adds a `--json-file-output` flag"
- Locate the existing CLI reference pages under `developer-tools/` that document the
  scan command options, add the new flag to the options table and an example, and open
  a draft PR listing exactly which pages changed.
