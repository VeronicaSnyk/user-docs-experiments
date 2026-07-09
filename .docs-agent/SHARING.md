# Installing the docs-agent from the shared archive

You received `docs-agent-share.zip`. This guide gets it into your local `user-docs` clone.

## Prerequisite: a clone of the repo

The installer does **not** clone for you. If you do not already have the repo:

```bash
git clone https://github.com/snyk/user-docs.git
```

## Install (recommended: the script)

1. Unzip the archive wherever it landed — this creates a `.docs-agent/` folder:

   ```bash
   cd ~/Downloads        # or wherever you saved it
   unzip docs-agent-share.zip
   ```

2. Run the installer, passing the path to your clone:

   ```bash
   bash ~/Downloads/.docs-agent/install.sh ~/Documents/git/user-docs
   ```

   (Or `cd` into your clone first and run it with no argument.)

   The script verifies the target is a `snyk/user-docs` clone, copies `.docs-agent/` into the repo root, and creates a ready-to-edit `.env` from the template.

## Install (manual fallback)

If you would rather not run the script, unzip directly into the **root of your clone** so you end up with `<your-clone>/.docs-agent/`, then:

```bash
cp .docs-agent/skills/fetch-google-docs/.env.example .docs-agent/.env
```

## Then: configure and run

1. **Add your credentials** — follow [setup/01-tokens.md](setup/01-tokens.md) to fill in your own Atlassian and Google values in `.docs-agent/.env`.
2. **Install Python dependencies:**

   ```bash
   pip3 install requests python-dotenv markdownify google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

3. **Authenticate Google** (first run only) to mint your own `token.pickle`:

   ```bash
   python3 .docs-agent/skills/fetch-google-docs/scripts/fetch_google_docs.py --auth
   ```

4. **Run the workflow** — see [setup/02-running-the-prompts.md](setup/02-running-the-prompts.md). For first-run errors, see [setup/03-troubleshooting.md](setup/03-troubleshooting.md).

> The archive ships **without** secrets — no `.env` and no `token.pickle`. Each person uses their own credentials.
