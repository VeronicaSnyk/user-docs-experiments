# Run a real end-to-end ship-it test (terminal)

The Atlassian + GitBook MCPs are loaded only in a FRESH interactive `claude`
session, so the real test runs there — not in the VS Code chat panel. This is also
how the pipeline runs in production.

## Setup (once per terminal)

    # fresh terminal so NODE_EXTRA_CA_CERTS is loaded:
    echo "$NODE_EXTRA_CA_CERTS"          # should print .../corporate-ca.pem
    cd /Users/veronicacernea/Desktop/user-docs-2026/user-docs
    git checkout feat/ship-it-automation
    git switch -c test/ship-it-dry-run   # throwaway branch for the trial

## Test 1 — real Jira fetch (proves MCP works)

    claude
    # in the session:
    > Use the Atlassian MCP to fetch Jira ticket DOCT-2618 and summarize:
    > summary, description, labels, and every link in it. Don't write any files.

Expect: real ticket content. If it says the MCP isn't available, run `/mcp` and
confirm atlassian is ✓ Connected, then retry.

## Test 2 — new-docs draft, STOP before PR (the core test)

Same session (or a new one):

    > Run /ship-it-new-docs for DOCT-2618. Fetch the ticket via the Atlassian MCP.
    > Obey the source-of-truth gate and content guardrails. Decide placement with
    > the section rules. Create the page + update that section's SUMMARY.md, but DO
    > NOT commit, push, or open a PR — stop after writing the files so I can review.

Then, back in a plain terminal, inspect:

    git status
    git diff

Check:
- [ ] Placement is in a sensible section folder (not a new top-level folder)
- [ ] `[ACTION REQUIRED: ...]` appears wherever the ticket lacked detail
- [ ] No internal-only content (internal URLs, customer names, unreleased dates)
- [ ] The matching SUMMARY.md got the new entry

## Test 3 — HOLD path (guardrail)

    > Run /ship-it-new-docs for a ticket that has NO PRD/spec/Confluence/Google link
    > (invent a thin summary only). Follow the source-of-truth gate.

Expect: it STOPS with "HELD: no source-of-truth link" and writes nothing.

## Test 4 — update path

    > Run /ship-it-doc-updates for DOCT-2618, treating it as an edit to existing
    > docs. Produce the candidate-file list first, edit in place, STOP before PR.

## Clean up the trial

    git restore .
    git clean -fdn                 # dry-run: see what would be removed
    git clean -fd <new-file-dir>   # actually remove the trial page(s)
    git checkout feat/ship-it-automation
    git branch -D test/ship-it-dry-run

## After the run

Tell the chat "test done" and I'll inspect the branch/diff you produced and review
the draft quality, placement, and guardrail behavior from here.
