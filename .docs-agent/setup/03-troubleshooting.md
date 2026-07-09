# Troubleshooting

These are the errors you are most likely to hit, with the fix that works.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` from Jira or Confluence | Wrong or missing API token, or the email does not match the token owner | Regenerate one token at id.atlassian.com and paste it into both `JIRA_API_TOKEN` and `CONFLUENCE_API_TOKEN`. Confirm `JIRA_EMAIL` is your account. |
| Google fetch returns `403` or `404` | The saved token belongs to another user who cannot read your doc | Move `.docs-agent/skills/token.pickle` aside and run `fetch_google_docs.py --auth` as yourself. |
| Google `--auth` hangs | The browser flow is waiting for you | Complete the login in the browser window that opened. It blocks until you finish. |
| `Could not find a suitable TLS CA certificate bundle` | A CA-bundle environment variable (for example `REQUESTS_CA_BUNDLE`, `SSL_CERT_FILE`) points to a path that does not exist | Point the variable at your real certificate, or symlink the expected path to the actual file. This affects pip and every `requests`-based script. |
| `git@github.com: Permission denied (publickey)` | Your SSH key is not loaded, or is passphrase-protected | Run `ssh-add ~/.ssh/id_ed25519`, or switch the remote to HTTPS (`git remote set-url origin https://github.com/snyk/user-docs.git`) and let `gh` handle credentials. |
| `gh: command not found` | The GitHub CLI is not installed | `brew install gh`, then `gh auth login`. |
| `pull request create failed: Head sha can't be blank` | The branch is not pushed | `git push -u origin <branch-name>` first. |

## How PRs are created

The `create-draft-pr` skill opens the PR as a **draft against `main`** (`--base main --draft`). The draft status keeps it out of the published GitBook until a Technical Writer reviews it and moves it to **Ready for review**. See `.docs-agent/skills/create-draft-pr/SKILL.md` for the full configuration.

## Related documentation

- [01-tokens.md](01-tokens.md) — create your credentials and `.docs-agent/.env`
- [02-running-the-prompts.md](02-running-the-prompts.md) — run the workflow end to end
- [../README.md](../README.md) — directory structure and per-skill setup
- [ship-it-new-docs SKILL.md](../skills/ship-it-new-docs/SKILL.md) — the orchestration workflow
- [create-draft-pr SKILL.md](../skills/create-draft-pr/SKILL.md) — PR creation details
- [snyk-docs-writing-rules SKILL.md](../skills/snyk-docs-writing-rules/SKILL.md) — writing style rules
