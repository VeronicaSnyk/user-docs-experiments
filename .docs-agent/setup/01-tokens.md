# Start here: tokens

Filling in `.docs-agent/.env` with your credentials is the **only** manual prerequisite. These are personal secrets you generate while logged in as yourself — the agent cannot create them for you, and it will not ask you to paste secrets into the chat.

## Credentials in `.docs-agent/.env`

> ⚠️ All skills read a single shared `.env` file at `.docs-agent/.env`. It is **gitignored**, which means it is never pushed to the GitHub repo.

Create it from the most complete template:

```bash
cp .docs-agent/skills/fetch-google-docs/.env.example .docs-agent/.env
```

Then edit `.docs-agent/.env`:

```
JIRA_BASE_URL=https://your-org.atlassian.net
JIRA_EMAIL=your.email@snyk.io
JIRA_API_TOKEN=your_atlassian_api_token

CONFLUENCE_BASE_URL=https://your-org.atlassian.net/wiki
CONFLUENCE_EMAIL=your.email@snyk.io
CONFLUENCE_API_TOKEN=your_atlassian_api_token

GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_secret
GOOGLE_PROJECT_ID=your_project_id
```

- `JIRA_EMAIL` and `CONFLUENCE_EMAIL` must be the exact account the token belongs to, or you get a `401`.
- `GOOGLE_CLIENT_SECRET` always starts with `GOCSPX-`. Watch for stray characters when you paste it.

## Where and how to create the credentials

### Atlassian API token (Jira and Confluence)

The same token authenticates both.

1. Sign in to Atlassian as your `@snyk.io` account.
2. Go to [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
3. Click **Create API token**, give it a label such as `docs-agent`, and copy the value. You see it only once.
4. Paste the same value into both `JIRA_API_TOKEN` and `CONFLUENCE_API_TOKEN` in `.docs-agent/.env`.
5. Set `JIRA_EMAIL` and `CONFLUENCE_EMAIL` to the account you used to create the token.

### Google OAuth credentials (client ID, client secret, project ID)

Create these in the Google Cloud Console. The full walkthrough is in [google-docs-api-setup.md](../skills/fetch-google-docs/references/google-docs-api-setup.md); the summary:

1. Open the [Google Cloud Console](https://console.cloud.google.com/) and create a project (for example, `Snyk Docs`). Its ID is your `GOOGLE_PROJECT_ID`.
2. Navigate to **APIs & Services** > **Library** and enable the **Google Docs API**, **Google Drive API**, and **Google Sheets API**.
3. Navigate to **APIs & Services** > **Credentials**. Configure the OAuth consent screen if prompted (User type **Internal** for the Snyk org), and add the read-only scopes for Docs, Drive, and Sheets.
4. Click **Create Credentials** > **OAuth client ID**, choose application type **Desktop app**, and create it.
5. From the created client, copy the **Client ID** into `GOOGLE_CLIENT_ID` and the **Client secret** into `GOOGLE_CLIENT_SECRET`. The secret starts with `GOCSPX-`.

After the values are in `.docs-agent/.env`, the agent can run the browser login for you (see [02-running-the-prompts.md](02-running-the-prompts.md)).

## Reference links

- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) — create the Jira/Confluence token
- [Google Cloud Console](https://console.cloud.google.com/) — create the project, enable APIs, create the OAuth client
- [google-docs-api-setup.md](../skills/fetch-google-docs/references/google-docs-api-setup.md) — the detailed, step-by-step OAuth setup, plus scopes, quotas, and how to revoke access
- [Google account permissions](https://myaccount.google.com/permissions) — revoke the app's access later if needed

---

**Next:** [02-running-the-prompts.md](02-running-the-prompts.md) — run the workflow. If you hit errors, see [03-troubleshooting.md](03-troubleshooting.md).
