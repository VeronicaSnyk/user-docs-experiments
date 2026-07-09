# Google Docs API Setup Guide

Quick reference for setting up Google Docs API access for the migration project.

## Prerequisites

- Google Cloud Console access
- Google account with access to relevant documents

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on project dropdown (top navigation bar)
3. Click "New Project"
4. Enter project name: `Snyk Docs Migration` (or similar)
5. Select organization: Snyk (if applicable)
6. Click "Create"

### 2. Enable Required APIs

1. In the project, navigate to "APIs & Services" → "Library"
2. Search for and enable each of these APIs:
   - **Google Docs API** - For reading Google Docs
   - **Google Drive API** - For accessing Drive metadata and permissions
   - **Google Sheets API** (optional) - For future spreadsheet access

### 3. Create OAuth 2.0 Credentials

1. Navigate to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **Internal** (for Snyk org) or **External**
   - App name: `Snyk Docs Migration`
   - User support email: Your Snyk email
   - Developer contact: Your Snyk email
   - Scopes: Add the following:
     - `https://www.googleapis.com/auth/documents.readonly`
     - `https://www.googleapis.com/auth/drive.readonly`
     - `https://www.googleapis.com/auth/spreadsheets.readonly`
   - Test users: Add your email (if External)
4. Return to "Credentials" and create OAuth client ID:
   - Application type: **Desktop app**
   - Name: `Snyk Docs Migration CLI`
5. Click "Create"
6. Download the credentials JSON file

### 4. Install Credentials

1. Rename the downloaded file:
   ```bash
   mv ~/Downloads/client_secret_*.json .docs-agent/credentials.json
   ```

2. Verify file location:
   ```bash
   ls -l .docs-agent/credentials.json
   ```

### 5. Authenticate

1. Run the authentication flow:
   ```bash
   python3 .docs-agent/scripts/fetch_google_docs.py --auth
   ```

2. This will:
   - Open your default browser
   - Prompt you to sign in with Google
   - Ask you to grant permissions
   - Save token to `.docs-agent/token.pickle`

3. Verify authentication:
   ```bash
   # Should show "Authentication successful!"
   # Token saved to: .docs-agent/token.pickle
   ```

### 6. Test Setup

Test by fetching a Google Doc:

```bash
# Use any accessible Google Doc
python3 .docs-agent/scripts/fetch_google_docs.py "https://docs.google.com/document/d/YOUR_DOC_ID/edit"
```

Expected output: Markdown version of the document

## OAuth Scopes Explained

The script requests these scopes (permissions):

| Scope | Purpose | Access Level |
|-------|---------|--------------|
| `documents.readonly` | Read Google Docs | Read-only |
| `drive.readonly` | Access Drive metadata | Read-only |
| `spreadsheets.readonly` | Read Google Sheets | Read-only |

**Why read-only?** Minimizes risk - the script can only read documents, never modify or delete them.

## Security Best Practices

### Protecting Credentials

1. **Never commit credentials**:
   - `.docs-agent/credentials.json` - OAuth client secrets
   - `.docs-agent/token.pickle` - Access token
   - Both are in `.gitignore`

2. **Rotate tokens periodically**:
   - Tokens auto-refresh when expired
   - Manually revoke and re-auth every few months
   - Revoke at: [Google Account Permissions](https://myaccount.google.com/permissions)

3. **Limit scope**:
   - Only use `.readonly` scopes
   - Never request write permissions unless absolutely necessary

### Access Control

1. **Document permissions**:
   - Ensure documents are shared with your Google account
   - Use organization access controls when possible
   - Request access if needed

2. **API quotas**:
   - Default quota: 60 requests per minute per user
   - Monitor usage in Google Cloud Console
   - Request quota increase if needed

## Troubleshooting

### Common Issues

#### "credentials.json not found"

**Cause:** OAuth credentials file not in correct location

**Solution:**
```bash
# Check file exists and is in correct location
ls -l .docs-agent/credentials.json

# If missing, download from Google Cloud Console and save to correct location
```

#### "Invalid credentials" or "Token expired"

**Cause:** Token needs refresh or credentials are invalid

**Solution:**
```bash
# Re-authenticate
python3 .docs-agent/scripts/fetch_google_docs.py --auth
```

#### "Access denied" or "403 Forbidden"

**Cause:** Document not shared with your account, or API not enabled

**Solution:**
1. Verify document is shared with your Google account
2. Check that Google Docs API is enabled in Cloud Console
3. Verify OAuth consent screen is configured correctly

#### "Redirect URI mismatch"

**Cause:** OAuth client type doesn't match

**Solution:**
1. Ensure you created a **Desktop app** OAuth client, not Web app
2. Delete existing credentials and create new Desktop app credentials

#### "Browser doesn't open during --auth"

**Cause:** Running in headless environment or browser issues

**Solution:**
1. Copy the URL shown in terminal
2. Open manually in browser
3. Complete authentication
4. Copy the authorization code back to terminal

### Debugging

Enable detailed logging:

```bash
# Set environment variable for verbose output
export GOOGLE_API_PYTHON_CLIENT_LOGGING=DEBUG
python3 .docs-agent/scripts/fetch_google_docs.py --auth
```

Check token status:

```bash
# If token.pickle exists, check modification time
ls -l .docs-agent/token.pickle

# Old token? Re-authenticate
python3 .docs-agent/scripts/fetch_google_docs.py --auth
```

## Quota and Limits

### API Quotas (Default)

- **Requests per minute per user:** 60
- **Requests per 100 seconds per user:** 600

Monitor and manage quotas:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Dashboard"
3. Select "Google Docs API"
4. View "Quotas & System Limits"

### Request Quota Increase

If you need higher limits:
1. Navigate to "Quotas & System Limits"
2. Select the quota to increase
3. Click "Edit Quotas"
4. Provide justification
5. Submit request (typically processed within 1-2 business days)

## Revoking Access

### When to Revoke

- Token compromised or exposed
- No longer need access
- Periodic security rotation

### How to Revoke

**Option 1: Via Google Account Settings**
1. Go to [Google Account Permissions](https://myaccount.google.com/permissions)
2. Find "Snyk Docs Migration" (or your app name)
3. Click "Remove Access"

**Option 2: Delete Token Locally**
```bash
# Remove local token (will require re-auth next time)
rm .docs-agent/token.pickle
```

**Option 3: Revoke in Cloud Console**
1. Go to Google Cloud Console → "APIs & Services" → "Credentials"
2. Find your OAuth client ID
3. Delete the credential (will invalidate all tokens)

## Multiple Users / CI/CD

### For Team Members

Each team member needs their own:
1. Google Cloud project OR shared project with individual auth
2. Own `credentials.json` (if using separate projects)
3. Own `token.pickle` (generated during auth)

**Never share `token.pickle`** between users - each person authenticates individually.

### For CI/CD (Future)

For automated workflows (GitHub Actions, etc.), use Service Account instead of OAuth:
1. Create Service Account in Google Cloud Console
2. Download service account key JSON
3. Grant Service Account access to documents
4. Use service account authentication in scripts

**Note:** Current script uses OAuth 2.0 (user authentication). Service account support can be added if needed.

## See Also

- [Fetch Google Docs Skill](.docs-agent/skills/fetch-google-docs.md) - Usage guide
- [Scripts README](.docs-agent/scripts/README.md) - All automation scripts
- [Google Docs API Documentation](https://developers.google.com/docs/api) - Official API docs
- [OAuth 2.0 Overview](https://developers.google.com/identity/protocols/oauth2) - OAuth concepts

---

**Last Updated:** 2026-06-08
**Maintained by:** edmond.sabou
