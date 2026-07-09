# Mock ticket — DOCT-2618 (local dry-run fixture)

This is a stand-in for a real Jira fetch, so you can exercise the ship-it drafting
pipeline **without** Jira/Confluence/Google credentials. It mirrors the real Slack
`/ship-it` release payload. When credentials are configured, replace this with:

    python .docs-agent/skills/fetch-jira-ticket/scripts/fetch_jira_ticket.py DOCT-2618

---

**Key:** DOCT-2618
**Summary:** CLI v1.1306.0 — unified IDE configuration dialog becomes GA
**Type:** Feature Enhancement
**Release type:** General Availability (GA)
**Expected release date:** 2026-07-09
**FedRAMP:** No
**Affected product areas:** Platform (CLI, IDE), Developer tools

**Description:**
The unified IDE configuration dialog (previously experimental) is now generally
available across the supported IDE plugins. Users configure Snyk scan settings from a
single dialog instead of per-scan-type screens.

**Sources / resources:**
- One-Pager: https://docs.google.com/presentation/d/13Yr2K37a3nOZqcHRe1WqKD1WmxWV9jPtYfEU0Mp2eEM/edit
- PRD: n/a
- Product Updates Draft: https://app.contentful.com/spaces/x1zq7m1y7a34/environments/master/entries/7MBDWuJlm8XUQnXdleKakt

**Submitted by:** @matt.dolan
