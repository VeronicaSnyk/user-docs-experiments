# Writing CLI and IDE documentation — supplemental rules

These rules are applied **in addition to** `snyk-style-guide.md` whenever a generated page targets
a CLI-help or synced page. Source: Snyk internal guide "Writing CLI and IDE documentation".

Most CLI/IDE pages are written like any other user-docs page. The pages below are exceptions:
they use a specific template and/or are synced to or from other GitHub repos.

## CLI help pages — formatting conventions

Applies to `developer-tools/snyk-cli/commands/**` and
`developer-tools/snyk-cli/cli-commands-and-options-summary.md`.

The CLI help is pulled from GitBook into each release of the CLI by Team CLI automation, so it
**must render properly in a terminal**. Follow the "Snyk CLI Help command" template and these
conventions:

- **Heading level one** is the top-level section heading in GitBook. Rationale: in GitHub the
  GitBook page `<Title>` is the only H1, so H1 headings on GitBook pages become H2 in GitHub.
- Command page structure (per existing `commands/test.md`): H1 = command name; H2 sections
  **Usage** (command syntax in a code span, for example `` `snyk test [<OPTIONS>]` ``),
  **Description**, **Exit codes** (bold code + meaning, hard line breaks), and **Options**.
- Use the term **"option"**. Use "argument" or "value" only where required — for example, the
  single argument for `snyk policy`, supported key values for `snyk configure`, and the optional
  arguments for `snyk iac describe`.
- Document each option as `--option` followed by a paragraph (one sentence is fine) that **starts
  with an imperative verb** (for example, *use* or *include*) and states what the option
  accomplishes.
- Give defaults as: `Default: Value or explanation.`
- **Links to information outside the help files:** phrase as "For more information about <topic>
  see <hyperlinked-page-title>" or "For more information see <hyperlinked-page-title>". Use
  **absolute** links. Put the link at the **end of a sentence**. **Do not** put a period after a
  link. Rationale: this format works in the CLI help and on the web.
- **Links to other CLI help files:** use **relative** links and state `command --help` (where
  `command` is the CLI command). Rationale: live links in GitBook, on the web, and in the `cli`
  repo; in the CLI itself there are no links to help — only `command --help`.

## Synced pages — ownership guardrails (blocking)

Do **not** make significant changes to these pages, and **never** change anything that affects the
source-file path (including renaming parent pages — that breaks the sync and causes errors).
Fixing typos and formatting is fine.

| Page | Synced with | Approval | Links |
| --- | --- | --- | --- |
| `developer-tools/snyk-cli/getting-started-with-the-snyk-cli.md` | `cli` repo `README.md` | Team CLI | External only (target pages do not exist in the `cli` repo); relative links within the same page are OK |
| `developer-tools/snyk-cli/commands/**`, `cli-commands-and-options-summary.md` | `cli` repo (pulled into releases) | Team CLI | Per CLI-help link rules above |
| Top-level IDE plugin/extension pages (Eclipse, JetBrains, Visual Studio, Visual Studio Code) | each plugin/extension repo `README.md` | Team IDE | External only; relative within the same page is OK |
| IDE plugin compatibility matrix | user-docs repo (automation) | — | **Do not edit in GitBook or in PRs.** Automation owns updates. |
