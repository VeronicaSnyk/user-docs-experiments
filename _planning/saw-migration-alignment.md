# SAW Docs Migration: Three-Way Alignment Analysis

Three-way alignment of the initial migration pipeline, PRD (DOCT-2343), and agreed site sections structure — with consolidated gaps and risks.

**Last updated**: April 2026
**Jira initiative**: [DOCT-2343](https://snyksec.atlassian.net/browse/DOCT-2343)

---

## 1. Agreed Site Sections (source of truth)

Derived from the approved site sections diagram (shared April 2026).

| # | Section | Status | SAW Content Lands Here |
|---|---|---|---|
| 1 | **Homepage / Discover Snyk** | ✓ Confirmed | SAW product overview, key concepts, Getting Started (7 articles) |
| 2 | **Platform Administration** | ✓ Confirmed | Managing Account (10 articles) — not SAW-owned; handoff required |
| 3 | **Scan and Fix** | ✓ Confirmed *(name TBD)* | Scanning (39), Quick How-To's (most), Asset Discovery (6), Troubleshooting (6), Authentication how-tos |
| 4 | **Developer Tools** | ✓ Confirmed *(name TBD)* | API ref, CLI ref, MCP server *(initial landing)*, CI/CD (7), Integrations (9), technical Quick How-To's |
| 5 | **AI Security tools** | ⬜ Proposed — future phase | SAW MCP + AI pen testing — **Developer Tools first**; move to this section in a separate future initiative |
| 6 | **Snyk data and governance** | ✓ Confirmed | No SAW content |

> **Section name freeze required**: "Scan and Fix" and "Developer Tools" both have "new name needed" annotations in the diagram. All file paths and pipeline configs must wait for final names, or use placeholder paths and rename atomically.

---

## 2. SAW Content Inventory → Site Section Mapping

### help.probely.com (~129 articles across 9 collections)

| Collection | Article Count | Target Site Section | Priority | Notes |
|---|---|---|---|---|
| Getting Started | 7 | **Homepage / Discover Snyk** | P0 | First-scan orientation; highest onboarding value |
| Quick How-To's | 39 | **Scan and Fix** (most) + **Developer Tools** (technical) | P0 | Not a standalone section — each article mapped individually; cross-reference audit required before splitting (see G16) |
| Scanning | 39 | **Scan and Fix** | P0 | Core product; highest expected traffic |
| Integrations | 9 | **Developer Tools** | P1 | Verify all integrations still supported in current SAW product |
| CI/CD | 7 | **Developer Tools** | P1 | Alongside CLI/API reference |
| Asset Discovery | 6 | **Scan and Fix** | P1 | Part of scanning/coverage story |
| Troubleshooting | 6 | **Scan and Fix** | P1 | Common issues subsection |
| Managing Account | 10 | **Platform Administration** (not SAW-owned) | P1 | Coordinate handoff with Platform Administration docs owners; handoff artifact required (see G11) |
| Plans and Credits | 6 | **TBD — likely not migrated as-is** | P2 | Likely superseded by Snyk platform billing docs; pipeline must filter these out until decision is logged (see G10) |
| **Total** | **~129** | | | |

### developers.probely.com (4 sections)

| Section | Target Site Section | Priority | Notes |
|---|---|---|---|
| Core Concepts | **Homepage / Discover Snyk** (overview) + **Developer Tools** (technical depth) | P0 | Split by audience depth |
| API Reference | **Developer Tools** | P0 | Evaluate future auto-generation from OpenAPI spec (out of scope v1) — decision gate required before manual migration begins (see G18) |
| CLI Reference | **Developer Tools** | P0 | Align URL structure with existing Snyk CLI docs patterns |
| MCP Server | **Developer Tools** *(initial)* → **AI Security tools** *(future)* | P0 | Strategic for agentic integrations; log a deferred migration item now (see G7) |

> **Source format note**: `developers.probely.com` is a separate site with a different export format from Intercom. A dedicated conversion stage and format assessment are required before any content work begins (see G13).

---

## 3. Migration Pipeline → PRD Milestone → Site Sections Alignment

> **Critical note**: As of April 2026, all pipeline stages listed below are **conceptual only** — no scripts, Makefiles, or workflow YAML exist for any of them. The pipeline must be built from scratch. This is the single largest unacknowledged risk in the plan (see R11).

| Pipeline Stage | PRD Milestone | Site Sections Dependency | Status |
|---|---|---|---|
| `url-inventory` | M1: IA definition | Must crawl both legacy domains before any mapping | ⚠️ Missing stage — see G3 |
| `convert-intercom` | M2: Export + draft | Covers `help.probely.com` only | ⚠️ Partial — `developers.probely.com` has no converter (see G13) |
| `convert-developers` | M2: Export + draft | Covers `developers.probely.com` | ⚠️ Missing stage — see G13 |
| `validate-conversion` | M2: Completeness check | None | ⚠️ Needs both converters before it can run |
| `rewrite-style` + Vale | M3: Rewrite + review | None (style-level) | ✅ Aligned once converters exist |
| `glossary-vale-setup` | M3: AI governance | None | ✅ Partial — governance doc not yet authored (see G9) |
| `plan-embedding` | M1: IA definition | **Must output paths under the 6 confirmed sections; requires SUMMARY.md restructure first** | ⚠️ Gap — see G1, G12 |
| `summary-restructure` | M1: IA definition | Must rebuild SUMMARY.md from 11 current sections to 6 confirmed sections | ⚠️ Missing stage — see G12 |
| `redirects-and-anchors` | M1 + M4: URL map | Front-matter aliases only — CDN redirects for 2 legacy domains not covered | ⚠️ Gap — see G2 |
| `gitbook-yaml-audit` | M1: IA definition | Existing `.gitbook.yaml` redirects must be audited for collisions before new aliases added | ⚠️ Missing stage — see G14 |
| `crossref-audit` | M2: Pre-split | Link graph across Quick How-To's must be mapped before articles are assigned to separate sections | ⚠️ Missing stage — see G16 |
| `embed-apply` | M4: Publish | **Requires correct SUMMARY.md target tree and confirmed section names** | ⚠️ Gap — see G1, G12 |
| `publish-to-test-space` | M2/M3: Staging | GitBook Test Space API stage missing; drafts go directly to production otherwise | ⚠️ Missing stage — see G5 |
| `[human sign-off gate]` | M3: Review | Required between Test Space review and production promotion | ⚠️ No gate defined |
| `link-check` | M4: Verify | Depends on correct target paths being set first | ✅ Once G1 + G12 resolved |
| `images-a11y` | M3/M4 | Images only — tables, headings, code blocks not covered (see G20) | ⚠️ Partial |
| `security-hardening-ci` | M3/M4 | None | ✅ Aligned |
| `prs-batching` | M4 | Must batch by target site section, not legacy collection | ⚠️ Gap — see G8 |
| `postmerge-monitor` | M4 | Must monitor both `help.probely.com` and `developers.probely.com` redirects; rollback procedure required | ⚠️ Gap — extend scope; see G17 |

---

## 4. Gaps (G1–G20)

### G1 — IA paths not tied to site sections `HIGH`
Pipeline proposes target paths into the current `docs/` tree (e.g., `implementation-and-setup/enterprise-setup/`), not the new site sections tree. Must be rebuilt under:
- `scan-and-fix/snyk-api-and-web/` *(name TBD)*
- `developer-tools/snyk-api-and-web/` *(name TBD)*
- `discover-snyk/snyk-api-and-web/` or `homepage/snyk-api-and-web/`

**Immediate symptom**: The 2FA (alternative OTP) article was placed under `docs/implementation-and-setup/enterprise-setup/single-sign-on-sso-for-authentication-to-snyk/` — this matches no confirmed site section. Correct target: **Scan and Fix > [SAW] > Authentication**.

### G2 — No CDN/DNS redirect stage for legacy domains `HIGH`
The pipeline generates front-matter `aliases` (intra-GitBook only) but has no stage for external DNS/CDN 301 redirect rules covering `help.probely.com` and `developers.probely.com`. These are P0 per the PRD. The pipeline must produce a `redirects.csv` artifact for the team implementing DNS/CDN rules.

### G3 — No URL inventory stage `HIGH`
PRD requires a complete URL inventory of all legacy pages before content mapping begins. No `url-inventory` pipeline stage exists. This is the P0 prerequisite for the redirect map and traffic-based prioritization.

### G4 — No Intercom analytics ingestion `HIGH`
PRD requires article view data to drive migration priority (highest-traffic first). No pipeline stage extracts or ingests this data. Without it, rewrite order is arbitrary.

### G5 — No GitBook Test Space publisher `MEDIUM`
PRD requires all initial drafts to land in a GitBook Test Space before production. The pipeline targets the docs repo directly. A `publish-to-test-space` stage (GitBook API) is missing, as is a sign-off gate before production promotion.

### G6 — Section name freeze not enforced `MEDIUM`
"Scan and Fix" and "Developer Tools" are flagged "new name needed." File paths baked into the pipeline and SUMMARY.md will need renaming once confirmed. No mechanism for this — must be a single atomic rename commit, gated on name confirmation.

### G7 — SAW MCP future migration to AI Security tools not tracked `MEDIUM`
SAW MCP content lands in Developer Tools now but moves to AI Security tools later. No placeholder issue, deferred redirect stub, or pipeline note tracks this second move. Without it, the future migration requires rediscovery of what moved.

### G8 — `prs-batching` scoped by legacy collection, not site section `MEDIUM`
PRs should be scoped by target site section (one PR per section landing), not by source Intercom collection. This makes reviews cleaner and maps to the approved IA.

### G9 — AI governance doc not authored `LOW`
Vale rules exist and style guide is enforced, but the PRD requires a published AI documentation governance doc (what AI can be used for, human review requirements, accuracy bar). Not yet created.

### G10 — Plans & Credits disposition unresolved `LOW`
6 articles have no confirmed target. The pipeline has no filter to exclude them from rewrite queues until a decision is made. Risk: rewrite work done on content that gets discarded.

### G11 — Managing Account handoff not tracked `LOW`
10 articles go to Platform Administration (not SAW-owned). No handoff artifact or assignee tracking for this slice.

### G12 — No SUMMARY.md restructure stage `HIGH`
The current SUMMARY.md has 11 top-level sections that do not map to the 6 confirmed site sections. No pipeline stage rebuilds it. Without a correct SUMMARY.md target tree, `embed-apply` has no valid structure to insert content into. This is a prerequisite for `plan-embedding` and `embed-apply`.

### G13 — No source format assessment or converter for `developers.probely.com` `HIGH`
`convert-intercom` covers `help.probely.com` only (Intercom export format). `developers.probely.com` (API ref, CLI ref, MCP, Core Concepts) is a separate site with a different format and structure. No format assessment has been done and no `convert-developers` stage exists. All P0 developer content is blocked until this is resolved.

### G14 — No `.gitbook.yaml` redirect audit stage `MEDIUM`
`.gitbook.yaml` already contains an extensive legacy redirect block. New SAW front-matter aliases could collide with or contradict existing entries. No audit stage is planned. Must be resolved before any `redirects-and-anchors` work begins.

### G15 — No content freeze signal for source domains `MEDIUM`
No pipeline stage or documented decision establishes whether `help.probely.com` is frozen during migration. If Probely continues updating articles after export, migrated content becomes stale and the redirect map drifts from the actual live URL set.

### G16 — No cross-reference graph audit before splitting Quick How-To's `MEDIUM`
39 Quick How-To articles are split across Scan and Fix AND Developer Tools. Internal links between those articles will break after splitting if not mapped first. No `crossref-audit` stage or link-graph analysis exists before section assignment.

### G17 — No rollback procedure documented `MEDIUM`
`postmerge-monitor` detects problems (404 spikes, redirect failures) but no rollback runbook exists. Without a defined procedure, the response to a bad publish is improvised under pressure.

### G18 — OpenAPI auto-generation decision gate missing `LOW`
The plan defers API ref auto-generation to a future phase but does not log a formal decision gate. If the SAW API reference is manually migrated in v1 and later replaced by auto-generation, the manual rewrite work is wasted. A recorded decision is needed before manual migration of the API reference begins.

### G19 — GitBook API access and permissions not confirmed `MEDIUM`
M1-G6 requires a GitBook Test Space and API key. No confirmation exists of who holds the key, what permission scopes are required, or whether the current GitBook account plan supports Test Space creation. This is a silent prerequisite that could block M2 start entirely.

### G20 — a11y scope limited to images only `LOW`
`images-a11y` covers alt text for images. SAW content includes tables, heading hierarchies, code blocks requiring language tags, and embedded scripts (e.g., the Google Apps Script in the 2FA article). No stage audits these for accessibility compliance.

---

## 5. Consolidated Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Section names finalized after pipeline is built — forcing bulk path rename | Med | High | Freeze names as M1 gate; use placeholder paths with atomic rename commit |
| R2 | 2FA article (and other committed articles) in wrong paths — creating redirect debt before migration starts | High | High | Immediately move 2FA article to correct Scan and Fix path; audit all previously committed SAW articles |
| R3 | CDN redirect ownership unclear — pipeline produces map but no one implements before brand sunset | Med | High | Confirm owner in M1; build redirect map as a blocking M1 deliverable |
| R4 | Intercom analytics access not confirmed — prioritization is guesswork | Med | High | Confirm access to Intercom Help Center analytics dashboard as P0 M1 blocker |
| R5 | SAW MCP in Developer Tools creates a future URL migration to AI Security tools | High | Med | Log deferred work item now; use URL structure that makes future move low-friction |
| R6 | No Test Space — drafts go directly to production without staging review | Med | Med | Confirm GitBook Test Space access and API key before M2 begins (see G19) |
| R7 | "Scan and Fix" name change mid-migration breaks SUMMARY.md and in-progress PRs | Med | Med | Gate M2 start on section name confirmation |
| R8 | Plans & Credits rewrite starts before disposition decision — wasted effort | Low | Med | Add explicit filter to pipeline to skip this collection until decision is logged |
| R9 | AI governance gap — contributors don't know the rules | Low | Low | Author `ai-docs-governance.md` as part of M3 kickoff |
| R10 | SUMMARY.md restructure is the largest mechanical risk — 156,900 bytes, 11 sections, thousands of cross-references | High | High | Add `summary-restructure` as an explicit M1 pipeline stage; gate on section name confirmation |
| R11 | No pipeline code exists — all stages are conceptual; plan treats them as existing infrastructure | High | High | Acknowledge build-from-scratch effort; scope pipeline engineering as a formal workstream before M2 |
| R12 | `.gitbook.yaml` legacy redirect block could collide with new SAW aliases | Med | High | Add `gitbook-yaml-audit` stage before any `redirects-and-anchors` work; assign owner |
| R13 | `snyk-docs-kickoff.yml` CI workflow scope untested for SAW content and new section paths | Med | Med | Validate kickoff workflow against SAW PRs before M2; extend if needed |
| R14 | `help.probely.com` updated post-export — migrated content becomes stale | Med | Med | Document source freeze decision; add staleness check to pipeline |
| R15 | Cross-reference breakage when splitting Quick How-To's across two sections | High | Med | Add `crossref-audit` stage before section assignment; map all internal links first |
| R16 | No rollback procedure — post-publish failure response is improvised | Med | Med | Author rollback runbook as part of M4 planning; define success/failure thresholds for monitor |
| R17 | GitBook API access not confirmed — could silently block M2 | Med | Med | Confirm access, scopes, and plan tier as explicit M1-G6 prerequisite |
| R18 | `developers.probely.com` has no conversion path — all P0 developer content blocked | High | High | Assess source format and build `convert-developers` stage before M2 |
| R19 | Manual API ref migration may be wasted if auto-gen is chosen later | Low | Med | Record an explicit interim-state decision before manual API ref rewrite begins |
| R20 | a11y gaps beyond images — tables, headings, code blocks, embedded scripts | Low | Low | Extend `images-a11y` stage scope or add a dedicated `content-a11y` stage in M3 |

---

## 6. M1 Gates — Must Complete Before Any Content Work Begins

| # | Gate | Owner | Blocks |
|---|---|---|---|
| M1-G1 | Confirm final names for "Scan and Fix" and "Developer Tools" | Product/Docs lead | All file path decisions; pipeline config; SUMMARY.md restructure |
| M1-G2 | Confirm CDN redirect ownership (Engineering / Infra / Docs) | PM / Eng lead | `redirects.csv` handoff and implementation |
| M1-G3 | Extract Intercom article view analytics (page views per article) | TW / PM | Priority ordering for rewrite queue |
| M1-G4 | Resolve Plans & Credits disposition (migrate / defer / drop) | PM + PMM | Scoping 6 articles in or out |
| M1-G5 | Move 2FA article to correct Scan and Fix path (unblocks audit of all early SAW commits) | TW (Veronica) | Path correctness across repo — blocked until M1-G1 confirmed |
| M1-G6 | Set up GitBook Test Space and confirm API access, scopes, and account plan tier | Docs/GitBook admin | M2 staging workflow (see G19) |
| M1-G7 | Log SAW MCP future migration as a deferred Jira item | TW / PM | Prevents orphan content post-migration |
| M1-G8 | Assess `developers.probely.com` export format and scope `convert-developers` stage | TW / Eng | All P0 developer content (API ref, CLI ref, MCP, Core Concepts) |
| M1-G9 | Audit `.gitbook.yaml` existing redirects for collision risk with new SAW aliases | TW / Eng | `redirects-and-anchors` stage; alias authoring for any SAW article |
| M1-G10 | Confirm Managing Account handoff owner in Platform Administration docs team | TW / PA docs owner | 10 articles scoped and assigned |

---

## 7. Prerequisites Map

```
M1-G1 (section names confirmed)
  └──> M1-G5 (2FA article move)
  └──> SUMMARY.md restructure stage (G12)
  └──> plan-embedding rebuilt against confirmed sections
  └──> all file path decisions unlocked

M1-G2 (CDN owner confirmed)
  └──> url-inventory stage (G3)
  └──> redirects.csv artifact build

M1-G3 (analytics extracted)
  └──> rewrite priority ordering for all 129 articles

M1-G4 (Plans & Credits decision)
  └──> pipeline filter scopes 6 articles in or out

M1-G6 (GitBook access confirmed) → G19 resolved
  └──> publish-to-test-space stage (G5)
  └──> human sign-off gate before production promotion

M1-G8 (developers.probely.com format assessed)
  └──> convert-developers stage built (G13)
  └──> validate-conversion can run against both sources

M1-G9 (.gitbook.yaml audit complete)
  └──> redirects-and-anchors stage safe to run

Critical path (nothing parallelizes around this):
  M1-G1 → SUMMARY.md restructure → plan-embedding → embed-apply → prs-batching → postmerge-monitor

Pipeline build dependency order:
  url-inventory → convert-intercom + convert-developers → validate-conversion
    → crossref-audit (before Quick How-To split)
    → rewrite-style + Vale
    → publish-to-test-space → [human sign-off]
    → embed-apply → link-check → images-a11y
    → prs-batching → postmerge-monitor (+ rollback runbook)
```

---

## 8. Resources Needed

| Resource | Type | Current Status | Gap |
|---|---|---|---|
| Section name decisions | Human / Product lead | Pending | Blocks everything — M1-G1 |
| CDN/DNS redirect owner | Engineering / Infra | Unconfirmed | R3, M1-G2 |
| Intercom analytics access | PM / TW | Unconfirmed | R4, M1-G3 |
| GitBook Test Space + API key + plan tier | GitBook admin | Unconfirmed | G19, R17, M1-G6 |
| Pipeline engineering (all stages, build from scratch) | Engineer | Not started | R11 — 3–5 weeks of build work |
| SUMMARY.md restructure | TW | Not started | G12, R10 |
| `developers.probely.com` format assessment | TW / Eng | Not started | G13, R18, M1-G8 |
| `.gitbook.yaml` redirect audit | TW / Eng | Not started | G14, R12, M1-G9 |
| Cross-reference graph audit (Quick How-To's) | TW | Not started | G16, R15 |
| Rollback runbook | TW / Eng | Not started | G17, R16 |
| Plans & Credits decision | PM + PMM | Pending | G10, R8 |
| Managing Account handoff assignee | PA docs owner | Unconfirmed | G11, M1-G10 |
| AI governance doc | TW | Not started | G9, R9 |
| SAW MCP deferred Jira item | TW / PM | Not logged | G7, R5 |
| OpenAPI interim-state decision record | PM / TW | Not recorded | G18, R19 |

**Minimum headcount**: 2 TWs (SAW content + coordination), 1 engineer (pipeline build), 1 PM (decisions + CDN + analytics), 1 GitBook admin.

---

## 9. Implementation Timeframe

| Phase | Gates Required | Work | Estimate |
|---|---|---|---|
| **M1: IA definition** | Stakeholder availability | Decisions, audits, format assessment, SUMMARY.md restructure scoped | 1–2 weeks |
| **Pipeline build** | M1 complete + format assessed | All stages built from scratch (R11) — url-inventory, both converters, crossref-audit, SUMMARY.md restructure, gitbook-yaml-audit, publish-to-test-space, rollback runbook | 3–5 weeks (engineering) |
| **M2: Export + draft** | Pipeline ready, Test Space confirmed | ~129 articles + developer docs converted, drafted, staged | 3–4 weeks |
| **M3: Rewrite + review** | M2 complete | Style rewrite, Vale pass, a11y, sign-off gate, governance doc | 3–5 weeks |
| **M4: Publish** | M3 signed off, CDN owner confirmed | SUMMARY.md final, prs-batching by section, CDN redirect cutover | 1–2 weeks |
| **Post-publish monitoring** | M4 complete | Active monitoring + rollback if triggered | 2–4 weeks ongoing |

**Total: 13–18 weeks from M1 gate completion.**

The clock has not started. All M1 blockers are human-decision gated (section names, CDN ownership, analytics access, Plans & Credits). Pipeline engineering (R11) cannot begin until M1 is fully resolved.

---

## 10. What Is Already Correct — No Changes Needed

- **Vale + `Terms.yml`** style enforcement — solid, covers this migration.
- **`rewrite-style` stage concept** — content-level, section-agnostic; ready to implement once pipeline is built.
- **`link-check` + `security-hardening-ci`** — quality gates, section-agnostic.
- **`postmerge-monitor`** — extend scope only (add 2 legacy domains + rollback trigger); structure is sound.
- **`snyk-docs-kickoff.yml`** — Vale integration and PR guidance working; validate scope for SAW PRs before M2.
- **Fork-only workflow** — no upstream PRs without explicit request; in place and working.
- **2FA (alternative OTP) article** — Vale-clean (0 warnings), style-compliant; needs only a path move to the correct Scan and Fix location once M1-G1 is confirmed.

---

## 11. Immediate Next Actions (sequenced)

1. **[Blocking — human decision]** Confirm section names and CDN redirect ownership (M1-G1, M1-G2).
2. **[Blocking — human decision]** Resolve Plans & Credits disposition and extract Intercom analytics (M1-G3, M1-G4).
3. **[Blocking — human decision]** Confirm Managing Account handoff owner in Platform Administration team (M1-G10).
4. **[Ready to action now]** Commit and push current Vale/style changes for the 2FA article to fork branch.
5. **[Ready to action now]** Log SAW MCP deferred migration as Jira item (M1-G7).
6. **[Ready to action now]** Record OpenAPI interim-state decision before any manual API ref work begins (G18).
7. **[Ready to action now]** Assess `developers.probely.com` export format (M1-G8).
8. **[Ready to action now]** Audit `.gitbook.yaml` existing redirects for collision risk (M1-G9).
9. **[After M1-G1 confirmed]** Rename 2FA article path to correct Scan and Fix location; audit all early SAW commits (M1-G5).
10. **[After M1-G1 confirmed]** Rebuild `plan-embedding` output paths against confirmed site sections; scope SUMMARY.md restructure.
11. **[After M1-G2 confirmed]** Build `url-inventory` stage and produce `redirects.csv` for CDN team.
12. **[After M1-G8 confirmed]** Build `convert-developers` stage (G13).
13. **[After M1-G9 confirmed]** Build `crossref-audit` stage for Quick How-To split (G16).
14. **[M2 start gate: M1-G6 confirmed]** Add `publish-to-test-space` stage to pipeline.
15. **[M3 kickoff]** Author `ai-docs-governance.md`; extend `images-a11y` to cover tables, headings, code blocks (G20).
16. **[M4 planning]** Author rollback runbook and define success/failure thresholds for `postmerge-monitor` (G17).

---

*File location: `_planning/saw-migration-alignment.md` — not published to docs.snyk.io.*
