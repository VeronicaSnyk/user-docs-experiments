---
name: ship-it-new-docs
description: End-to-end workflow for creating NEW documentation from a Jira ticket. Fetches the ticket, retrieves referenced Confluence/Google Docs, searches existing docs for context, generates a clean draft, commits changes, and automatically creates a GitHub draft PR with metadata. Use whenever a Jira ticket has the label ship-it-new-docs (the new-docs branch of the Slack /ship-it app), when someone asks to draft or create a new docs page from a ticket/PRD/one-pager, or when a feature launch needs a brand-new page rather than an edit to an existing one. For editing pages that already exist, use ship-it-doc-updates instead.
license: Proprietary
compatibility: Requires Python 3.x, Jira/Confluence/Google Docs credentials in .env, Snyk User Docs MCP server, GitHub CLI
metadata:
  author: edmond.sabou
  version: "1.1.0"
  category: documentation
---

# Ship It - New Docs

**Trigger:** Use this skill when a Jira ticket has the label `ship-it-new-docs`.

This skill orchestrates the complete end-to-end workflow for creating documentation from a Jira ticket:
0. Checks the local clone is current with `main` and offers to sync if behind
0.5 Source-of-truth gate: confirm a PRD/one-pager/spec link is present, or hold
1. Fetches the Jira ticket details
2. Extracts and retrieves all referenced Confluence and Google Docs URLs
2.5 (Optional) Enriches context with the `gather-context` skill
3. Searches existing Snyk documentation to understand structure and find placement
4. Generates a clean, merge-ready draft (without metadata) using ONLY the provided sources
5. Creates the file in the matching top-level product folder and updates that folder's `SUMMARY.md`
6. Commits the changes to the current branch
7. **Automatically invokes `create-draft-pr`** to create a GitHub PR in draft mode with metadata
8. **Automatically invokes `update-jira-ticket`** to write the PR link back to the ticket

## Content guardrails (must follow)

These are non-negotiable rules from the AI ContentOps project. They apply to every
step that writes content.

1. **Provided sources are the only source of truth.** Draft ONLY from the Jira
   ticket and the links it references (PRD, one-pager, spec, Confluence, Google
   Docs). Do not invent product behavior, field names, limits, or steps from prior
   knowledge or assumption.
2. **Mark gaps, never fabricate.** When the sources do not cover something the page
   needs, insert an inline `[ACTION REQUIRED: <what is missing>]` placeholder
   instead of guessing. A draft with honest gaps is correct; an invented detail is a
   defect.
3. **Sensitivity gate before finalizing.** Do not carry internal-only content into a
   public draft: internal URLs/paths, unreleased dates beyond what the ticket
   approves, customer names, or internal Confluence excerpts. When unsure, replace
   with an `[ACTION REQUIRED: confirm public-safe wording]` placeholder.

## Workflow

### Step 0: Ensure the local clone is current with `main`

Placement, deduplication, and the new branch are all derived from local state, so a stale clone causes duplicate pages, wrong placement, or merge conflicts. Run this check first.

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
4. If the count is greater than `0`, WARN the user: state how many commits behind the clone is, and show what changed in the likely product folder:
   ```bash
   git diff --stat main origin/main -- <likely-product-folder>/
   ```
   Then ASK whether to sync before continuing:
   - If the user agrees: `git pull --ff-only origin main` (updates refs AND working tree), then proceed. All later steps now read current content.
   - If the user declines: proceed on the stale clone, and have `create-draft-pr` add a line to the PR description noting the branch was cut from a clone N commits behind `origin/main`.

Only after this check do the search and placement steps (Step 3 onward) and the branch creation in Final Steps run, so they operate on current (or explicitly-acknowledged-stale) content.

### Step 0.5: Source-of-truth gate

New-feature docs require a source. Before drafting, confirm the ticket has at least
one PRD, one-pager, technical spec, Confluence page, or Google Doc link.

1. Fetch the ticket (Step 1) far enough to inspect its description, comments, and links.
2. If **no** usable source link is present:
   - **Interactive:** tell the submitter the request is on hold and ask for a PRD /
     one-pager / spec link before continuing. Do not draft from the summary alone.
   - **Headless (CI):** stop with a clear message ("held: no source-of-truth link")
     and have the workflow relabel the issue and comment asking for a link. Do not
     draft a page with no source.
3. If a source link **is** present, continue. Everything drafted must trace back to
   these sources (see **Content guardrails** above).

This mirrors the "Tech validated? if No → hold + notify submitter" gate in the
AI ContentOps design.

### Step 1: Fetch Jira Ticket
```bash
python .docs-agent/skills/fetch-jira-ticket/scripts/fetch_jira_ticket.py <TICKET-KEY>
```

Review the ticket for:
- **Summary**: What documentation is needed
- **Description**: Requirements, scope, target audience
- **Comments**: Stakeholder clarifications and context
- **Attachments**: Screenshots, diagrams, reference materials
- **URLs**: Links to Confluence pages or Google Docs with additional context

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

### Step 2.5: (Optional) Enrich context

If the ticket is thin or references internal systems, invoke the `gather-context`
skill to cross-check the ticket against additional sources (AlphaPatch / ask-snyk /
Confluence) and surface gaps. It degrades gracefully: when those MCPs are not
configured it simply reports what it could and could not confirm. Anything it finds
that the sources do not confirm becomes an `[ACTION REQUIRED]` placeholder, never an
invented detail, and its output passes through the sensitivity gate before use.

### Step 3: Search Existing Documentation

Use the Snyk User Docs MCP server to:
1. **Search for related topics** to understand existing content:
   ```
   Use mcp__snyk-user-docs__searchDocumentation with queries based on ticket keywords
   ```

2. **Get specific pages** for style reference:
   ```
   Use mcp__snyk-user-docs__getPage to read similar existing pages
   ```

3. **Determine placement** - Identify where in the docs structure this new page fits:
   - Which product area? (Snyk Code, Snyk Open Source, etc.)
   - Which section? (Getting Started, Guides, Reference, etc.)
   - Related pages that should link to/from this new doc

### Step 4: Apply Snyk Writing Rules

Before drafting, review the **snyk-docs-writing-rules** skill to ensure compliance with Snyk's style:
- Voice and tone (active voice, present tense, imperative for actions)
- Formatting (sentence case headings, bold UI elements)
- Terminology (product names, technical terms)
- Screenshots and diagrams guidelines

Key references from snyk-docs-writing-rules:
- Main rules: `SKILL.md` - Core writing conventions
- Terms: `references/terms-and-pairs.md` - Canonical spellings
- Screenshots: `references/screenshots-and-diagrams.md` - Visual guidelines

### Step 5: Generate First Draft

Create the first draft combining:
- **Content from Jira ticket**: Requirements, scope, user stories
- **Context from Confluence/Google Docs**: Additional details, technical specs
- **Style from existing docs**: Heading structure, voice, formatting patterns
- **Snyk writing rules**: Apply conventions from snyk-docs-writing-rules skill
- **Placement suggestion**: Where in the docs hierarchy this belongs

## Draft Structure

Your draft should be clean and ready to merge, without metadata at the top. Metadata will be added to the PR description by the `create-draft-pr` skill.

```markdown
# [Title from Jira Summary]

[Brief introduction based on ticket description and search of existing docs]

## Prerequisites

[If applicable, based on ticket requirements]

## [Main Content Sections]

[Based on ticket description and referenced materials]

## Next steps

[If applicable, link to related workflows]
```

**IMPORTANT:** Do NOT add metadata (placement, source, references) in the documentation file. This metadata will be included in the GitHub PR description when using the `create-draft-pr` skill. Keep the documentation clean and ready to merge.

## Style Guidelines

**IMPORTANT:** Apply the **snyk-docs-writing-rules** skill when drafting. Key conventions:

### Voice & Grammar (from snyk-docs-writing-rules)
- **Active voice**: "Snyk scans your code" (not "your code is scanned")
- **Present tense**: "Snyk creates" (not "will create")
- **Imperative for actions**: "Navigate to Settings" (not "You should navigate")
- **Second person**: "You configure" (not "users configure")
- **No hedging**: "Snyk avoids" (not "Snyk makes an effort to avoid")

### Formatting (from snyk-docs-writing-rules)
- **Sentence case** for headings: "Configure the integration" (not "Configure the Integration")
- **Bold UI elements**: "Navigate to **Settings** > **Integrations**"
- **Short paragraphs**: 3-4 sentences max, one idea per chunk
- **Numbered lists** for procedures, bullet lists for options
- **Code blocks** with language tags
- **No scaffolding labels**: No "Before you begin:" headers

### Terminology (from snyk-docs-writing-rules)
- Check `references/terms-and-pairs.md` for canonical spellings
- Product names: "Snyk Code", "Snyk Open Source" (exact capitalization)
- No "please" or other unnecessary words
- "Navigate to" (not "go to")
- "After" (not "once")

### Screenshots & Diagrams (if needed)
- See `references/screenshots-and-diagrams.md` for guidelines
- Light mode only, zoom on relevant parts, no annotations

## File Creation and TOC Update

**Repository structure (user-docs):** This repository is a multi-space GitBook repo. Documentation lives in a **fixed set of top-level section folders** at the repository root, each of which is its own GitBook space with its own `SUMMARY.md` (table of contents). These map to the reader-facing tabs on `docs.snyk.io`:

- `developer-tools/`
- `discover-snyk/`
- `platform-administration/`
- `scan-fix-and-prevent/`
- `snyk-data-and-governance/`
- **Agent security** — published as its own `docs.snyk.io` tab (Snyk Studio, Agent Scan, Agent Guard), but it has **no dedicated root folder yet**. Its pages currently live under the legacy `docs/` space at **`docs/integrations/snyk-studio-agentic-integrations/`**, registered in `docs/SUMMARY.md` under the `## Integrations` heading.

There is no single shared `SUMMARY.md`. Confirm the current sections with `find . -maxdepth 2 -name SUMMARY.md`.

> **`docs/` rule:** Do **not** place new pages in the legacy `docs/` space — **except** Agent security content, which today belongs under `docs/integrations/snyk-studio-agentic-integrations/` and is registered in `docs/SUMMARY.md`. If an `agent-security/` root folder later exists (it will appear in `find . -maxdepth 2 -name SUMMARY.md`), prefer it.

After generating the draft:

1. **Identify the correct section:**
   - Match the ticket's feature to the one section that best fits (for example, scanning/remediation content goes in `scan-fix-and-prevent/`, CLI/API/IDE content in `developer-tools/`, org/group/settings in `platform-administration/`).
   - **Agent security / agentic AI content** (Snyk Studio, Agent Scan, Agent Guard, MCP/AI-assistant integration guides) goes under `docs/integrations/snyk-studio-agentic-integrations/` and is registered in `docs/SUMMARY.md` (unless an `agent-security/` root folder now exists).
   - **Never create a new top-level folder.** The section set is fixed — always place the page inside the closest existing one.
   - Use the Snyk User Docs MCP search and browse the relevant `SUMMARY.md` to find the most fitting subsection.

2. **Create the file inside that section:**
   - Place the new page within the matching section, nested to mirror how sibling pages are organized (sections nest pages several levels deep, e.g. `scan-fix-and-prevent/scan-with-snyk/snyk-container/<filename>.md`).
   - Example: a new Snyk Container page → `scan-fix-and-prevent/scan-with-snyk/snyk-container/<filename>.md`

3. **Update that section's `SUMMARY.md`:**
   - Open the `SUMMARY.md` in the **same top-level section folder** (for example `scan-fix-and-prevent/SUMMARY.md`), not a shared one.
   - Add the new page entry under the correct section heading, following the existing indentation and link format.
   - Use the path relative to that `SUMMARY.md` (for example `* [Page Title](scan-with-snyk/snyk-container/<filename>.md)`).

4. **Verify the placement:**
   - Confirm the entry is nested under the correct section in that space's `SUMMARY.md`.
   - Check the relative path from `SUMMARY.md` to the new file resolves.
   - Maintain logical ordering within the section.

5. **Save metadata for PR creation:**
   - Keep track of: Jira ticket key/title/URL, placement path, references (Confluence/Google Docs URLs), related pages.
   - This metadata is used by the `create-draft-pr` skill to populate the PR description.
   - Do NOT include this metadata in the documentation file itself.

## Validation Checklist

Before finalizing the draft:
- [ ] Confirmed local main is current with origin/main (or recorded the staleness caveat)
- [ ] All URLs from Jira ticket have been fetched and reviewed
- [ ] Searched existing docs for related content
- [ ] Identified correct placement in docs structure
- [ ] **Applied snyk-docs-writing-rules** (active voice, present tense, sentence case, etc.)
- [ ] **Checked terminology** against `snyk-docs-writing-rules/references/terms-and-pairs.md`
- [ ] Draft follows Snyk docs style and patterns
- [ ] Included all required information from ticket
- [ ] **Documentation file is clean** without metadata at the top
- [ ] **Created .md file in the docs folder** at the suggested placement location
- [ ] **Updated SUMMARY.md** to include the new page in the table of contents
- [ ] **Saved metadata** (placement, source, references) for PR creation with `create-draft-pr` skill

## Final Steps: Commit and Create PR

After completing the documentation draft, **automatically proceed** to create a GitHub pull request:

1. **Create a branch off `main`** and commit the changes:
   ```bash
   git checkout -b <jira-key>-<slug> main
   git add <section-folder>/<path>/new-file.md <section-folder>/SUMMARY.md
   git commit -m "Add [title] documentation for [JIRA-KEY]"
   ```

2. **Push the branch** to remote:
   ```bash
   git push -u origin <branch-name>
   ```

3. **Automatically invoke the `create-draft-pr` skill** to create the GitHub pull request in draft mode with all metadata

The `create-draft-pr` skill will:
- Create PR with Jira ticket title
- Include placement, source, references, and related pages in PR description
- Set PR to draft mode
- Add review instructions for Technical Writers

4. **Automatically invoke the `update-jira-ticket` skill** to write the PR link back
   to the source ticket, so tracking is centralized (per the AI ContentOps outcome
   "Automated Jira ticket per request, updated with links to all drafts"). This step
   is best-effort: if the Atlassian MCP is not configured it is skipped and noted,
   never failing the run.

## Gotchas

- The workflow reads the local clone, not remote main; Step 0 guards against stale clones but only fast-forwards when you approve.
- Not all Jira tickets will have URLs - focus on ticket description/comments if none
- Confluence and Google Docs may require separate authentication
- The Snyk User Docs MCP server searches published docs, not drafts in progress
- Always check ticket comments for late additions or clarifications
- If placement is unclear, search for the product/feature name in existing docs

## Example

**Jira ticket DOC-456 with label "ship-it-new-docs":**
- Summary: "Document new SBOM export feature"
- Description contains link to Confluence spec
- Comments mention related GitHub issue

**Orchestration steps:**
1. Fetch DOC-456 → get summary, description, comments
2. Extract Confluence URL → fetch spec document
3. Search Snyk docs for "SBOM" → find existing SBOM pages
4. Get page `scan-fix-and-prevent/scan-with-snyk/snyk-open-source/manage-vulnerabilities/sbom-and-licensing.md` for style reference
5. Generate draft combining all context
6. Suggest placement in the `scan-fix-and-prevent/` section (under the matching subsection)
