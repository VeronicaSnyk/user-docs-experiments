---
name: create-draft-pr
description: Create a GitHub pull request in draft mode for new documentation. Use after creating documentation files from a Jira ticket. Creates PR with Jira ticket metadata, targets the main branch of snyk/user-docs, and notifies reviewers.
license: Proprietary
compatibility: Requires gh CLI installed and authenticated, docs files created in correct location
metadata:
  author: edmond.sabou
  version: "1.0.0"
  category: automation
---

# Create Draft PR

**Trigger:** Use this skill after creating documentation files from a Jira ticket using `ship-it-new-docs`.

**CRITICAL: In user-docs, always create the PR as a draft against `--base main`. The draft status keeps it out of the published docs until a Technical Writer reviews and marks it Ready.**

This skill creates a GitHub pull request in draft mode with:
- PR title matching the Jira ticket title
- PR description containing Jira metadata (source, references, related pages)
- Draft status to indicate work in progress
- Notification that a Technical Writer will review when moved to Ready
- **Base branch set to `main`**

## Prerequisites

Before using this skill:
- Documentation file(s) created inside the correct top-level section folder (e.g. `scan-fix-and-prevent/`, `developer-tools/`)
- That section's `SUMMARY.md` updated with new page entries
- Changes committed to current branch
- GitHub CLI (`gh`) installed and authenticated

## Workflow

### Step 1: Verify Changes

Ensure all documentation changes are committed:

```bash
git status                          # Should show clean working tree
git log --oneline -1                # Verify last commit has the docs
```

### Step 2: Push Branch to Remote

Push the current branch to GitHub:

```bash
git push -u origin <branch-name>
```

If the branch already exists on remote, just push:

```bash
git push
```

### Step 3: Gather PR Metadata

From the Jira ticket and documentation draft, gather:
- **Jira ticket key and title** (e.g., "DOCT-429: Create CR on Container integrations recommendations")
- **Placement** in docs structure
- **Source URL** (Jira ticket link)
- **References** (Confluence, Google Docs links)
- **Related pages** in the documentation

### Step 4: Create Draft PR

**IMPORTANT:** Always use `--base main` and `--draft`.

Use the GitHub CLI to create a draft pull request:

```bash
gh pr create \
  --title "<JIRA-KEY>: <Jira Ticket Title>" \
  --body "$(cat <<'EOF'
## Documentation Changes

**Placement:** `/path/to/location/in/docs/filename.md`

**Source:** [JIRA-KEY: Title](jira-ticket-url)

**References:**
- [Confluence Page Title](confluence-url)
- [Google Doc Title](google-doc-url)

**Related Documentation:**
- [Related Page 1](docs-url)
- [Related Page 2](docs-url)

## Files Changed

- `<section>/path/to/new-file.md` - New documentation page
- `<section>/SUMMARY.md` - Updated table of contents

## Review Process

A Technical Writer will review this documentation when the PR is moved from **Draft** to **Ready for review**.

To mark as ready:
1. Review the documentation changes
2. Click "Ready for review" in the PR interface
3. Tag the Technical Writer team for review

---

Generated using ship-it-new-docs workflow from Jira ticket [JIRA-KEY](jira-url)
EOF
)" \
  --base main \
  --draft
```

**IMPORTANT:** Targets `main` in user-docs. The PR is always created as a draft so it does not publish until a Technical Writer marks it Ready.

### Step 5: Verify PR Creation

The command outputs the PR URL. Verify:
- PR is in draft mode
- Title matches Jira ticket
- Description includes all metadata
- Base branch is correct (`main`)

## PR Title Format

Use the exact Jira ticket key and title:

```
DOCT-429: Create CR on Container integrations recommendations
```

## PR Description Template

The PR description should follow this structure:

```markdown
## Documentation Changes

**Placement:** `/path/to/location/in/docs/filename.md`

**Source:** [JIRA-KEY: Title](jira-ticket-url)

**References:**
- [Reference Title](url)

**Related Documentation:**
- [Related Page](url)

## Files Changed

- `path/to/file.md` - Description

## Review Process

A Technical Writer will review this documentation when the PR is moved from **Draft** to **Ready for review**.

To mark as ready:
1. Review the documentation changes
2. Click "Ready for review" in the PR interface
3. Tag the Technical Writer team for review

---

Generated using ship-it-new-docs workflow from Jira ticket [JIRA-KEY](jira-url)
```

## Complete Example

For Jira ticket DOCT-429:

```bash
gh pr create \
  --title "DOCT-429: Create CR on Container integrations recommendations" \
  --body "$(cat <<'EOF'
## Documentation Changes

**Placement:** `/scan-fix-and-prevent/scan-with-snyk/snyk-container/snyk-container-integration-recommendations.md`

**Source:** [DOCT-429: Create CR on Container integrations recommendations](https://snyksec.atlassian.net/browse/DOCT-429)

**References:**
- [Getting value out of Snyk Container (Implementation)](https://snyksec.atlassian.net/wiki/spaces/FBK/pages/1661206529/Getting+value+out+of+Snyk+Container+Implementation) - Internal Confluence page

**Related Documentation:**
- [Container registry integrations](https://docs.snyk.io/scan-fix-and-prevent/scan-with-snyk/snyk-container/container-registry-integrations)
- [Snyk CLI for container security](https://docs.snyk.io/developer-tools/snyk-cli/snyk-cli/scan-and-maintain-projects-using-the-cli/snyk-cli-for-snyk-container)
- [Scan your Dockerfile](https://docs.snyk.io/scan-fix-and-prevent/scan-with-snyk/snyk-container/scan-your-dockerfile)

## Files Changed

- `scan-fix-and-prevent/scan-with-snyk/snyk-container/snyk-container-integration-recommendations.md` - New integration recommendations page
- `scan-fix-and-prevent/SUMMARY.md` - Added entry to table of contents

## Review Process

A Technical Writer will review this documentation when the PR is moved from **Draft** to **Ready for review**.

To mark as ready:
1. Review the documentation changes
2. Click "Ready for review" in the PR interface
3. Tag the Technical Writer team for review

---

Generated using ship-it-new-docs workflow from Jira ticket [DOCT-429](https://snyksec.atlassian.net/browse/DOCT-429)
EOF
)" \
  --base main \
  --draft
```

## Best Practices

- **Always use draft mode** for initial PR creation
- **Include all metadata** from the Jira ticket in PR description
- **List all changed files** with brief descriptions
- **Verify branch is pushed** before creating PR
- **Copy PR URL** to share with stakeholders

## Optional enhancements

Consider adding to the `gh pr create` command in this repo:

1. **Auto-assign reviewers**: Add `--reviewer @snyk/technical-writers` or the appropriate team
2. **Labels**: Add `--label documentation` or relevant labels

PRs target `main` as drafts; a Technical Writer reviews before the PR is marked Ready and merged.

## Troubleshooting

**Error: "gh: command not found"**
- Install GitHub CLI: `brew install gh` (macOS) or see https://cli.github.com/

**Error: "authentication required"**
- Run `gh auth login` and follow prompts

**Error: "pull request create failed: GraphQL: Head sha can't be blank"**
- Ensure branch is pushed to remote: `git push -u origin <branch-name>`

**PR not in draft mode:**
- Verify `--draft` flag was included in command
- Convert to draft via GitHub UI: PR page → Click "Convert to draft"
