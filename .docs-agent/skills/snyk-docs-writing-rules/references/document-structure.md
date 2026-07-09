# Document structure

Read this when deciding *where* a doc belongs and *how* to lay it out, before writing any prose. The line-level rules in `SKILL.md` govern how each sentence reads; this file governs the shape of the whole page.

Two decisions come first, in order:

1. **Placement** — which site section the content belongs in.
2. **Content type** — which of the four page templates fits the reader's intent.

## Contents

1. Site placement
2. Choosing a content type
3. Universal structure principles
4. Feature page template
5. Implementation guide template
6. Getting started template
7. Reference page template
8. Cross-cutting devices: tables, decision-forcing, GitBook components

---

## 1. Site placement

`docs.snyk.io` groups content into six site sections (the top-level tabs). Every new page is recommended into one of them, chosen by what the reader is trying to do.

| Section | Reader intent | Typical content |
|---|---|---|
| **Discover Snyk** | "What is this and how do I start?" | Overviews, supported languages, getting started, release and product-lifecycle terms |
| **Platform administration** | "How do I manage and operate Snyk?" | Snyk hierarchy, Tenants, Groups, Organizations, user management, SSO, Broker, platform-level configuration |
| **Scan, fix, and prevent** | "How do I do my day-to-day security work?" | Finding, fixing, and preventing issues across the SDLC, prioritization, policy enforcement |
| **Developer tools** | "I need the technical reference for a tool in my stack." | Snyk CLI, IDE plugins, SCM and CI/CD integrations, partner integrations, Snyk API |
| **Agent security** | "How do Snyk's AI capabilities improve my security posture?" | Snyk Studio, Agent Scan, Agent Guard |
| **Snyk data and governance** | "How does Snyk handle my data, and what are the legal terms?" | Data processing, generative AI use, residency, compliance, test counts |

**Worked example.** The Snyk CLI lives under **Developer tools**, so any new CLI content is recommended there — not under Scan, fix, and prevent, even though the CLI performs scans. Placement follows the reader's *primary* intent (reach for a tool) over the action the tool happens to perform.

When a page could plausibly sit in two sections, place it by the reader's starting intent and cross-link from the other section rather than duplicating.

---

## 2. Choosing a content type

Pick the template by what the reader needs from the page, not by the subject matter.

| Reader need | Content type | Section it usually lives in |
|---|---|---|
| Understand and operate one feature or integration end to end | **Feature page** | Developer tools; Scan, fix, and prevent; Platform administration |
| Be guided through a multi-phase rollout, making decisions along the way | **Implementation guide** | Discover Snyk; Platform administration; Agent security |
| Get from zero to a first result fast | **Getting started guide** | Discover Snyk |
| Look up a fact, value, role, code, or support matrix | **Reference page** | Platform administration; Scan, fix, and prevent; Developer tools |

Two cross-cutting habits separate the guide types from the others:

- **Feature pages and reference pages are largely self-contained and linear** — the reader can stay on the page.
- **Implementation guides and getting started guides lead with a roadmap and cross-link out** — they orient the reader and hand off, rather than containing everything.

---

## 3. Universal structure principles

These apply to every content type (they restate and extend the core principles in `SKILL.md`):

- **Conclusion first.** Lead with what the page is for and why the reader would use it. Never open with "This guide describes…".
- **Headings are keywords.** A reader scanning the table of contents should know what each section delivers.
- **Roadmap near the top** for anything multi-step: an anchor-linked list of what the page covers, in the order the reader will hit it.
- **Cross-link rather than duplicate.** Point to the canonical page for a concept instead of restating it.
- **Establish the conceptual model before the steps.** If a procedure depends on a distinction (for example, Group-level versus Organization-level), give the reader that model — often as a comparison table — before the first instruction.

---

## 4. Feature page template

The most linear and self-contained type. Covers one feature or integration end to end. Order:

1. **Title + value proposition.** What the thing is and why you would use it. Often a short "Key features" or "allows you to" list.
2. **Prerequisites / requirements / supported environments / known limitations.** What must be true before starting. Feature availability and plan gating commonly sit here as a `{% hint style="info" %}` callout.
3. **Conceptual notes.** Scoping caveats the reader needs before acting (for example, "per user, not per Organization", or the distinction between two token types).
4. **How-to / setup.** Task-oriented, numbered steps. Break into sub-procedures with H3 headings where there is more than one path.
5. **Settings / configuration.** Options the reader can adjust afterward.
6. **Use cases / features in action.** What the reader can do once it is working, usually with screenshots.
7. **Teardown.** How to disconnect, disable, or migrate. Flag destructive consequences in a `{% hint style="warning" %}` callout.
8. **Support / troubleshooting.** Common errors and where to get help.

*Verified against the GitLab integration page, which follows this order almost section for section.*

---

## 5. Implementation guide template

A two-level, decision-driven type for multi-phase rollouts. Its signature is that it forces the reader to *decide* before acting — this is what makes it read as guidance rather than reference.

### Parent (hub) page

A sequenced hub, not a container:

1. **Title + outcome-framed intro** — "By the end of this guide, you will have…".
2. **A numbered, ordered list of the phases**, each anchor- or page-linked.
3. **One short H2 per phase** — a 2-to-4-sentence teaser plus a "To learn more, visit *[phase page]*" cross-link.
4. **Interspersed conceptual anchors** — the shared models the phases depend on (the Snyk hierarchy table, points of contact, mapping critical apps).

### Child phase page

Each phase page repeats this skeleton:

1. **Title + "why this milestone matters" intro.**
2. **"As you work through this page, you will:"** — a numbered, anchor-linked roadmap of the sub-tasks.
3. **A comparison table that establishes the conceptual model before the steps** (for example, Group-level versus Organization-level SCM).
4. **Task sections that force a decision before the procedure** (see the invariant below).
5. **"Use cases for X" / "Use cases for Y" sections** that help the reader choose between approaches (for example, direct registry integration versus CI/CD).

### The decision-forcing invariant

Surface the decision and its trade-offs **before** the procedural steps, never after. The reader chooses, then acts. This device appears in at least two component forms — use whichever fits, but keep the invariant:

- **Stepper + "Key decision" callout.** Build the task with `{% stepper %}` / `{% step %}`. Each step opens with a bold title, then a `{% hint style="success" %}` callout labeled **"Key decision:"** prompting the choice, then the numbered procedural steps, and closes with a summary table of options and trade-offs.
- **Question headings + expandable branches.** Frame each decision as a question-style H2 ("Do you want to auto-update the Snyk CLI?"), with expandable `{% details %}` blocks for each answer (Yes / No) describing the resulting actions. Pair this with a concrete worked example (an "Example company" that states its decisions, then a numbered rollout) so the reader sees one full path.

*The first form is described in Snyk's written rules; the second is the form used on the Snyk Studio "Distribution at scale" page. Both are correct.*

---

## 6. Getting started guide template

The lightest type. Gets a new user from zero to a first result, then hands off. Order:

1. **Title + a one-line "what you'll do here"** — often an anchor-linked list of the methods covered (for example, the four scan paths, each linked).
2. **Environment / prerequisite preamble**, delivered as `{% hint %}` callouts (supported browsers, JavaScript required, plan limits, "set your region first") rather than a formal "Prerequisites" heading.
3. **A sequence of H2 task sections in first-encounter order** — for example: create or log in to an account, set up an integration, obtain an API token, import a Project, set up Essentials, review results and fix. Each is a short procedure or orientation ending in a "For more information, see…" link.
4. **Orienting comparison tables** — a feature matrix (Web UI versus CLI versus API versus PR Checks) and command tables to help a newcomer pick a path. These orient; they do not force a decision (contrast with the implementation guide's decision tables).
5. **Numbered steps for the one concrete procedure** — for example, a single five-step `curl` walkthrough with a code block.
6. **Closing handoff** — branch-out links by scenario (per product, per language, per next phase) plus a support contact line.

---

## 7. Reference page template

For lookup content: roles, supported languages, error codes, permission scopes, support matrices. The reader arrives to confirm a fact, not to be walked through a task. Order:

1. **Title + concept-defining intro.** One or two sentences stating what the thing is and how it is used, then the entry point into the data ("The pre-defined roles Snyk provides are as follows:").
2. **A categorized list of the entities**, each with a short gloss (the roles, languages, error categories, or scopes), grouped by their natural dimension (level, product, severity).
3. **A short conceptual section on how the entities relate** when the relationships are not obvious (for example, how Organization, Group, and Tenant roles combine, or how a viewer role inherits permissions).
4. **Lookup tables — the core of the page.** Permission matrices, language- or feature-support grids, error-code tables. Keep columns consistent and let the data carry the page.
5. **Cross-links to the related task**, where one exists (for example, from "Pre-defined roles" to "Create a custom role").

Keep prose minimal. A reference page that needs long explanatory passages is usually a feature page or a guide wearing the wrong template — re-evaluate the content type.

*Verified against the Pre-defined roles page: defining intro, categorized role list, a "Role types" conceptual section, then Organization-, Group-, and Tenant-level permission tables.*

---

## 8. Cross-cutting devices

### Tables play different roles by content type

The same component carries different intent. Be deliberate about which one a table is doing:

- **Decision / trade-off tables** (implementation guides) — options against their consequences, to drive a choice between approaches.
- **Orienting feature-matrix tables** (getting started guides) — capabilities against paths (Web UI / CLI / API), to help a newcomer locate themselves.
- **Lookup tables** (reference pages) — the data is the deliverable; the table *is* the content, not a support for it.

### Decision-forcing belongs to implementation guides

Decision callouts and question-branch blocks are the signature of implementation guides and appear *before* steps. Do not scatter them into feature or reference pages, where they would imply a choice the reader does not need to make.

### GitBook components — name them, do not improvise

Snyk docs render in GitBook. Use the real components rather than generic "callout" or "expandable" language:

- `{% hint style="info" %}` / `warning` / `success` / `danger` — callouts. `success` is the "Key decision" device in implementation guides; `warning` flags destructive actions in teardown sections.
- `{% stepper %}` / `{% step %}` — sequenced procedures.
- `{% details %}` / `<details><summary>` — expandable branches (decision answers, optional deep-dives, long sample scripts).
- `{% tabs %}` / `{% tab %}` — parallel variants of the same task (for example, per operating system).
- `{% code %}` — code blocks; add `overflow="wrap"` for long lines.
- `<figure><img><figcaption>` — screenshots with captions. Alt text and capture rules are in `references/screenshots-and-diagrams.md`.
