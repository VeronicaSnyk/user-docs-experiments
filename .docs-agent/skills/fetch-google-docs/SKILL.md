---
name: fetch-google-docs
description: Fetch and convert Google Docs documents to Markdown format for reference during migration work. Use when you need to access reference materials stored in Google Docs or when migrating content that references Google Docs.
license: Proprietary
compatibility: Requires Python 3.x with google-auth, google-api-python-client packages
metadata:
  author: edmond.sabou
  version: "1.0.0"
  category: integration
---

# Fetch Google Docs Skill

## Prerequisites

### First-Time Setup

1. **Enable Google Docs API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable: Google Docs API, Google Drive API, Google Sheets API (optional)

2. **Create OAuth 2.0 Credentials**:
   - In Google Cloud Console, go to "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Download the credentials file

3. **Save credentials**:
   ```bash
   mv ~/Downloads/client_secret_*.json .docs-agent/credentials.json
   ```

4. **Authenticate** (first time only):
   ```bash
   python3 scripts/fetch_google_docs.py --auth
   ```

## Usage

### Basic Usage

Fetch a document by URL:
```bash
python3 scripts/fetch_google_docs.py "https://docs.google.com/document/d/1ABC123/edit"
```

Fetch a document by ID:
```bash
python3 scripts/fetch_google_docs.py 1ABC123
```

### Options

- `--auth` - Authenticate with Google (first-time setup or re-authentication)
- `--json` - Output raw JSON instead of Markdown

### Examples

```bash
# Authenticate (first time)
python3 scripts/fetch_google_docs.py --auth

# Fetch document as Markdown
python3 scripts/fetch_google_docs.py "https://docs.google.com/document/d/1ABC123/edit"

# Save to file
python3 scripts/fetch_google_docs.py 1ABC123 > reference.md
```

## Typical Migration Workflow

1. **Identify Google Docs references** in Intercom articles or external resources
2. **Extract document ID** from URLs
3. **Fetch document** using the script
4. **Review content** for relevance to migration
5. **Reference or integrate** into migrated documentation as needed

## Markdown Conversion

### Supported Elements
- **Headings** (H1-H6)
- **Bold**, *italic*, and __underline__ text
- **Links** - converted to `[text](url)` format
- **Tables** - converted to Markdown table format
- **Paragraphs** - basic text paragraphs

### Limitations
- **Images** are not downloaded (handle separately)
- **Complex formatting** may not convert perfectly
- **Comments** and **Suggestions** are not included

## Troubleshooting

**"credentials.json not found"**
- Download OAuth credentials from Google Cloud Console and save to `.docs-agent/credentials.json`

**"Token expired" or "Invalid credentials"**
- Re-authenticate using `--auth` flag

**"Access denied" or "403 Forbidden"**
- Check that the document is shared with your Google account

## Security

1. **Never commit credentials**:
   - `.docs-agent/credentials.json` contains OAuth client secrets
   - `.docs-agent/token.pickle` contains access tokens
   - Both are in `.gitignore`

2. **Use read-only scopes**:
   - The script uses `.readonly` scopes to minimize risk

## Script Location

The fetch script is available at:
```
scripts/fetch_google_docs.py
```

See `scripts/requirements.txt` for Python dependencies.
