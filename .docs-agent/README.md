# Documentation Agent Skills

This directory contains Agent Skills for documentation workflows. Skills follow the [Agent Skills specification](https://agentskills.io/specification) for compatibility across AI coding assistants.

## Purpose

The `.docs-agent/` directory provides:
- **Agent Skills** - Standardized skills for fetching external documentation and creating new content
- **Content orchestration** - End-to-end workflow for creating documentation drafts from Jira tickets
- **Content retrieval** - Fetch fresh documentation from Jira, Confluence, and Google Docs
- **Style compliance** - Snyk writing rules for consistent voice, tone, and formatting
- **Quality assurance** - Link validation and style enforcement

## Directory Structure

```
.docs-agent/
├── README.md                          # This file
├── .env                               # Shared credentials for all skills (gitignored)
└── skills/                            # Individual skills (each self-contained)
    ├── fetch-confluence/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── fetch_confluence.py
    │   │   └── requirements.txt
    │   └── .env.example             # Template for Confluence credentials
    ├── fetch-google-docs/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── fetch_google_docs.py
    │   │   └── requirements.txt
    │   ├── references/
    │   │   └── google-docs-api-setup.md
    │   ├── .env.example             # Template for Google OAuth credentials
    │   └── token.pickle              # Google OAuth token (gitignored)
    ├── fetch-jira-ticket/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── fetch_jira_ticket.py
    │   │   └── requirements.txt
    │   └── .env.example             # Template for Jira credentials
    ├── ship-it-new-docs/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── extract_urls.py
    │   │   └── requirements.txt
    │   └── .env.example             # No additional credentials needed
    ├── snyk-docs-writing-rules/
    │   ├── SKILL.md
    │   └── references/
    │       ├── terms-and-pairs.md
    │       ├── screenshots-and-diagrams.md
    │       ├── ms-fallback.md
    │       └── decisions-log.md
    └── check-broken-links/
        └── SKILL.md
```

## Available Skills

### 1. ship-it-new-docs
**When to use:** When a Jira ticket has the label "ship-it-new-docs"

Orchestrates creating a first draft of new documentation from a Jira ticket. Fetches the ticket, retrieves all referenced Confluence/Google Docs URLs, searches existing Snyk documentation for context and placement, applies snyk-docs-writing-rules, then generates a clean draft ready to merge (without metadata).

**Prerequisites:** Jira/Confluence/Google Docs credentials in `.docs-agent/.env`, Snyk User Docs MCP server
**Leverages:** fetch-jira-ticket, fetch-confluence, fetch-google-docs, snyk-docs-writing-rules
**Next step:** Use `create-draft-pr` to create a GitHub pull request with metadata

### 2. fetch-jira-ticket
**When to use:** When drafting documentation from a Jira ticket

Fetches Jira ticket details including summary, description, comments, and attachments. Use when the user provides a Jira ticket key (e.g., DOC-123) or URL. Extracts all information needed for drafting documentation.

**Prerequisites:** Jira API credentials in `.docs-agent/.env`

### 2. fetch-confluence
**When to use:** When you need to retrieve documentation from Confluence

Fetches fresh Confluence pages by URL, page ID, or search query. Commonly used for style guides, documentation standards, or any Confluence reference material. Outputs Markdown for easy reading.

**Prerequisites:** Confluence API credentials in `.docs-agent/.env`

### 3. fetch-google-docs
**When to use:** When you need to access reference materials stored in Google Docs

Fetches and converts Google Docs documents to Markdown format for documentation drafts or migration work.

**Prerequisites:** Google OAuth credentials in `.docs-agent/.env`, first-time authentication

### 5. snyk-docs-writing-rules
**When to use:** When drafting, editing, or reviewing Snyk documentation

Snyk's writing style rules for user documentation. Covers voice, grammar, formatting, terminology, and screenshot guidelines. Use whenever working on Snyk docs to ensure consistency with product voice and style.

**Prerequisites:** None (reference material only)

### 6. create-draft-pr
**When to use:** After creating documentation files from a Jira ticket using `ship-it-new-docs`

Creates a GitHub pull request in draft mode with Jira metadata in the PR description. PR title matches the Jira ticket, includes placement/source/references metadata, and notifies that a Technical Writer will review when moved to Ready.

**Prerequisites:** GitHub CLI (`gh`) installed and authenticated, documentation committed to branch
**Targets:** `main` branch, always as a draft PR (stays out of the published GitBook until a Technical Writer marks it Ready)

### 7. check-broken-links
**When to use:** When verifying documentation cross-references

Systematically checks all migrated documentation for missing and broken links. Identifies text references without actual links, broken internal links, and external references needing updates.

**Prerequisites:** None (no external dependencies)

## How Agent Skills Work

Agent Skills use **progressive disclosure** in three stages:

1. **Discovery**: Agents load only the `name` and `description` of each skill
2. **Activation**: When a task matches, agents read the full `SKILL.md` instructions
3. **Execution**: Agents follow instructions, executing bundled code or loading references as needed

## Environment Setup

### Shared Environment Variables

All skills share a single `.env` file at `.docs-agent/.env`. Create it by copying from a skill-specific example:

```bash
# Create from Confluence example
cp .docs-agent/skills/fetch-confluence/.env.example .docs-agent/.env

# Or create from Google Docs example (includes both sets of credentials)
cp .docs-agent/skills/fetch-google-docs/.env.example .docs-agent/.env
```

Then edit `.docs-agent/.env` with your actual credentials. Scripts automatically check for `.env` in these locations (in order):
1. `.docs-agent/.env` (shared, **recommended**)
2. `skills/<skill-name>/.env` (skill-specific)
3. Project root `.env` (fallback)

### Python Dependencies

Install dependencies for skills that require them:

```bash
# For ship-it-new-docs skill (orchestration)
pip3 install -r .docs-agent/skills/ship-it-new-docs/scripts/requirements.txt

# For fetch-jira-ticket skill
pip3 install -r .docs-agent/skills/fetch-jira-ticket/scripts/requirements.txt

# For fetch-confluence skill
pip3 install -r .docs-agent/skills/fetch-confluence/scripts/requirements.txt

# For fetch-google-docs skill
pip3 install -r .docs-agent/skills/fetch-google-docs/scripts/requirements.txt
```

### Jira API Setup

Edit `.docs-agent/.env` and add your Jira credentials:
```
JIRA_BASE_URL=https://your-org.atlassian.net
JIRA_EMAIL=your.email@snyk.io
JIRA_API_TOKEN=your_api_token_here
```

Get API token from: https://id.atlassian.com/manage-profile/security/api-tokens

### Confluence API Setup

Edit `.docs-agent/.env` and add your Confluence credentials:
```
CONFLUENCE_BASE_URL=https://your-org.atlassian.net/wiki
CONFLUENCE_EMAIL=your.email@snyk.io
CONFLUENCE_API_TOKEN=your_api_token_here
```

Same API token works for both Jira and Confluence.

### Google Docs API Setup

1. Edit `.docs-agent/.env` and add your Google OAuth credentials:
   ```
   GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   GOOGLE_PROJECT_ID=your_project_id_here
   ```

2. Follow detailed setup instructions in [fetch-google-docs/references/google-docs-api-setup.md](skills/fetch-google-docs/references/google-docs-api-setup.md)

3. Run authentication (first time only):
   ```bash
   python3 .docs-agent/skills/fetch-google-docs/scripts/fetch_google_docs.py --auth
   ```

## Skill Resources

### ship-it-new-docs
- **Script**: `scripts/extract_urls.py` - Extract and categorize URLs from Jira tickets
- **Orchestrates**: fetch-jira-ticket, fetch-confluence, fetch-google-docs, snyk-docs-writing-rules, and Snyk User Docs MCP
- **No additional credentials needed** - Uses credentials from other skills

### fetch-jira-ticket
- **Script**: `scripts/fetch_jira_ticket.py` - Fetch Jira ticket with all details (always fresh)
- **Config**: `.env.example` - Template for Jira credentials

### fetch-confluence
- **Script**: `scripts/fetch_confluence.py` - Fetch any Confluence page by URL, ID, or search (always fresh)
- **Config**: `.env.example` - Template for Confluence credentials

### fetch-google-docs
- **Script**: `scripts/fetch_google_docs.py` - Fetch and convert Google Docs to Markdown
- **Reference**: `references/google-docs-api-setup.md` - OAuth setup guide
- **Config**: `.env.example`, `token.pickle` - Google authentication

### snyk-docs-writing-rules
- **References**: Complete Snyk writing style guide with detailed rules
- **Key files**: 
  - `references/terms-and-pairs.md` - Canonical term spellings
  - `references/screenshots-and-diagrams.md` - Visual content guidelines
  - `references/ms-fallback.md` - Microsoft Writing Style Guide fallback
  - `references/decisions-log.md` - Historical decisions and rationale
- **No dependencies** - Reference material only

### check-broken-links
- No scripts or external dependencies - uses built-in link validation logic

## Adding New Skills

To add a new skill:

1. Create a new directory in `skills/`:
   ```bash
   mkdir -p .docs-agent/skills/my-new-skill
   ```

2. Create `SKILL.md` with required frontmatter:
   ```markdown
   ---
   name: my-new-skill
   description: What this skill does and when to use it.
   license: Proprietary
   metadata:
     author: your.name
     version: "1.0.0"
     category: automation
   ---
   
   # My New Skill
   
   [Instructions here]
   ```

3. Add skill-specific resources as needed:
   ```bash
   mkdir -p .docs-agent/skills/my-new-skill/scripts
   mkdir -p .docs-agent/skills/my-new-skill/references
   mkdir -p .docs-agent/skills/my-new-skill/cache
   ```

4. Each skill is self-contained - keep all resources within the skill directory

## Best Practices

1. **Keep SKILL.md under 500 lines** - Move detailed content to skill's `references/`
2. **Use relative paths** - Reference files from skill root (e.g., `scripts/fetch.py`)
3. **Self-contained skills** - Keep all resources within each skill directory
4. **Progressive disclosure** - Tell agents when to load reference files
5. **Clear descriptions** - Help agents identify when to activate skills
6. **Skill-specific dependencies** - Each skill has its own `requirements.txt`

## Validation

Validate skills using the skills-ref library:

```bash
npm install -g @agentskills/skills-ref
skills-ref validate .docs-agent/skills/my-skill
```

## Security Best Practices

- **Never commit `.env` files** - Contains sensitive API credentials (already in .gitignore)
- **Never commit credentials.json or token.pickle** - OAuth credentials (already in .gitignore)
- **Rotate API tokens regularly** - Security best practice
- **Use read-only scopes** - Minimize risk of compromised credentials
- **Shared .env location** - Keep all credentials in `.docs-agent/.env` for easier management

## Related Documentation

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best Practices for Skill Creators](https://agentskills.io/skill-creation/best-practices)
- [CLAUDE.md](../CLAUDE.md) - Project-specific instructions for Claude Code

---

**Last Updated:** 2026-06-10  
**Maintained by:** edmond.sabou
