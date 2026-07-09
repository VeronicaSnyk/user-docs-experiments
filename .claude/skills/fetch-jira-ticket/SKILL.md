---
name: fetch-jira-ticket
description: Fetch Jira ticket details including summary, description, comments, and attachments. Use when the user provides a Jira ticket key (e.g., DOC-123) or URL and needs to extract information for drafting documentation. Outputs all ticket details in Markdown format.
license: Proprietary
compatibility: Requires Python 3.x, Jira credentials in .env
metadata:
  author: edmond.sabou
  version: "1.0.0"
  category: documentation
---

# Fetch Jira Ticket

**First-time setup required:** If `.docs-agent/.env` doesn't exist, create it:
```bash
cp .docs-agent/skills/fetch-jira-ticket/.env.example .docs-agent/.env
```
Then edit it with your Jira credentials: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (get token from https://id.atlassian.com/manage-profile/security/api-tokens).

## Usage

Fetch by ticket key (recommended):
```bash
python scripts/fetch_jira_ticket.py DOC-123
```

Fetch by URL:
```bash
python scripts/fetch_jira_ticket.py https://your-org.atlassian.net/browse/DOC-123
```

Output includes:
- Ticket summary and description
- Status, priority, assignee
- All comments (with authors and timestamps)
- Attachments list
- Custom fields (if any)
- Links to related tickets

Output is Markdown by default. Add `--json` for raw JSON.

## Common Use Cases

**Drafting documentation from ticket:**
1. Fetch ticket details: `python scripts/fetch_jira_ticket.py DOC-123`
2. Review the description and comments for requirements
3. Check attachments for reference materials
4. Use gathered information to draft the documentation

**Ticket fields extracted:**
- **Summary**: Ticket title/heading
- **Description**: Main content (often contains scope, requirements)
- **Comments**: Discussion and clarifications from stakeholders
- **Attachments**: Screenshots, diagrams, reference files
- **Reporter/Assignee**: Who requested and who owns it
- **Labels/Components**: Categorization and context

## Gotchas

- Script fails immediately if `JIRA_BASE_URL`, `JIRA_EMAIL`, or `JIRA_API_TOKEN` are missing from `.env`
- Credentials loaded from `.docs-agent/.env` (recommended), `skills/fetch-jira-ticket/.env`, or project root `.env`
- Ticket keys are case-insensitive but must match the project key (e.g., DOC-123, DOCS-456)
- URLs must be from your Jira instance — external Jira URLs won't work
- Always fetches fresh content from Jira (no caching)
