# Documentation Agent - TODO for Production

This file tracks tasks and configuration changes needed before moving `.docs-agent` to production.

## Configuration Changes

### Pull Request Settings

- [x] **Update PR target branch**: PRs now target `main` (set with `--base main --draft`) in `.docs-agent/skills/create-draft-pr/SKILL.md`

### Environment Variables

- [ ] **Production credentials**: Ensure `.docs-agent/.env` has production credentials
  - Jira API token
  - Confluence API token
  - Google Docs OAuth credentials (if needed)

## Skill Enhancements

### Ship-it-new-docs Skill

- [ ] Review metadata placement strategy (currently in PR description, not in draft)
- [ ] Validate placement suggestions work for all doc types
- [ ] Test with various Jira ticket types

### Create-draft-pr Skill

- [ ] Configure GitHub PR reviewers/teams to auto-assign
- [ ] Add PR labels based on doc type or product area
- [ ] Consider GitHub Actions integration for automated checks

## Testing Checklist

- [ ] Test full workflow with various Jira ticket types
- [ ] Verify SUMMARY.md updates work correctly for all sections
- [ ] Confirm Google Docs integration works when needed
- [ ] Test PR creation with different branch targets

## Documentation

- [ ] Update README.md with production setup instructions
- [ ] Document the complete workflow for technical writers
- [ ] Add troubleshooting guide for common issues

## Notes

- Target branch: `main` (PRs are always opened as drafts against `main`)
- Repository: `snyk/user-docs` (multi-space GitBook; documentation lives in a fixed set of top-level section folders — `developer-tools/`, `discover-snyk/`, `platform-administration/`, `scan-fix-and-prevent/`, `snyk-data-and-governance/` — each with its own `SUMMARY.md`)
