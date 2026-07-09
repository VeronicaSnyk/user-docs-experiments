---
name: snyk-docs-writing-rules
description: Snyk's writing style rules for user documentation and product-facing written content — user guides, knowledge base articles, release notes, technical reference, getting-started content, and integration guides. Use this skill whenever drafting, editing, or reviewing Snyk documentation, when the user mentions Snyk and a documentation task, asks for writing "in Snyk's voice," shares a doc to clean up, or produces technical writing where Snyk conventions apply. Also covers screenshots and diagrams in Snyk docs, and the canonical spelling of Snyk, partner, and security terms. Note that in-product UI copy (button labels, error and notification text, tooltips, placeholders, dialogs, empty states) is owned by the separate `ux-copy` skill — use that for microcopy inside the Snyk platform. The Snyk rules here take precedence; for anything not covered, fall back to the Microsoft Writing Style Guide (see references/ms-fallback.md).
---

# Snyk writing rules

The style rules for Snyk **documentation** and product-facing written content: guides, reference, release notes, KB articles, and integration content. It merges Snyk's R&D documentation rules with the consolidated Snyk style guide.

**Scope note.** This skill covers *documentation*. For copy that lives inside the Snyk product UI — button labels, error and notification text, tooltips, placeholders, confirmation dialogs, empty states — use the **`ux-copy`** skill instead. This skill still tells you how to *refer to* the UI when documenting it (which verbs to use, how to format element names), but not how to author the in-product strings themselves.

Some mechanical conventions differ between the two surfaces by design. Documentation uses the date, time, and number rules below (for example, 12-hour time with AM/PM, dates like "April 15, 2026," and spelling out zero through nine). In-product strings follow `ux-copy` (24-hour time, short dates, numerals). Apply this skill's conventions to documentation; do not cross-apply the UI conventions, and do not apply these to UI strings.

**These rules override the Microsoft Writing Style Guide.** For anything not addressed here, fall back to MS style (see `references/ms-fallback.md`).

Where Snyk's own sources once disagreed, every conflict has been resolved. The decisions are baked into the rules below; the full record lives in `references/decisions-log.md`.

## How to use this skill

1. Before drafting a new page, decide where it belongs and which template fits: open `references/document-structure.md`. (Apply this whenever the task is a whole page, not a small edit.)
2. Apply the rules below to whatever is being drafted or edited.
3. For a specific term, compound word, acronym, or how to name a UI element in docs: open `references/terms-and-pairs.md`.
4. For screenshots or diagrams in docs: open `references/screenshots-and-diagrams.md`.
5. When the rules here are silent: open `references/ms-fallback.md` for the Microsoft default.
6. To trace why a rule reads the way it does: see `references/decisions-log.md`.

---

## Editing approach

When editing existing content, do not just correct errors in place. Reshape the content so it is clearer and more concise. A clean, tight draft matters more than preserving the original structure.

- **Concision first — cut words, not content.** Tighten wording and remove words that carry no information ("full URL" → "URL"; "the credentials stored in" → "credentials from"). But do not delete clauses or sentences that carry real meaning. When a sentence is long, **split it into two one-idea sentences** rather than dropping a clause. Preserve the author's information; make it tighter, not shorter by omission.
- **Restructure for clarity; don't just correct in place.** Reorganize when it helps the reader: split a dense paragraph into short chunks, lead each chunk with the point, and apply "write for scanning," "conclusion first," and "one idea per chunk" actively. Moving and reshaping text is expected, not a last resort.
- **Convert passive to active by naming the actor.** Rewrite passives so the subject does the action, naming Snyk or the user where natural: "X is called Y" → "Snyk refers to X as Y"; "credentials are never stored by Snyk" → "Snyk does not store credentials"; "connections are configured to…" → "you configure connections to…".
- **Match the product's real UI label.** Use the exact on-screen word. If the screen says "box," write "box" — do not swap in "section" or "pane."
- **No scaffolding labels.** Do not use "Before you begin:" or similar headers. State a prerequisite as a short lead sentence right after the heading: "Configure X before proceeding. Without it, …".
- **Keep one numbered sequence.** Fold setup actions into the numbered steps; nest sub-actions as bullets under a step, rather than splitting into separate prose blocks.
- **Imperative for actions; plain present tense for notes.** Steps are commands ("Navigate to…", "Save the integration"). Explanatory notes stay factual ("Snyk authenticates… You do not enter credentials here") — do not force them into commands.
- **Show restraint when content already follows the rules.** Fix only genuine errors. Do not restructure or reword text that is already clear, active, and concise.

### Transformations at a glance

| Before | After | Why |
|---|---|---|
| "a finding is created as Not fixed" | "Snyk creates a finding with a **Not fixed** state" | Passive → active; bold the status value |
| "Snyk makes a great effort to avoid" | "Snyk avoids" | Drop hedging/filler; be assertive |
| "this functionality enables users to scan" | "you can scan" | No "enable" for capability; second person |
| "the steps below will not work" | "the following steps do not work" | No spatial reference; present tense |
| "Once the feature is enabled" | "After you enable the feature" | "after," not "once" |
| "go to Settings > Scan Settings" | "Navigate to **Settings** > **Scan Settings**" | "Navigate to"; bold UI path |
| "consider changing the state" | "change the state" | Imperative, not advisory |
| "using TLS 1.2 may be acceptable" | "using TLS 1.2 is acceptable" | No "may/should/might" — state it |
| "you should have Account Owner permissions" | "you must have Account Owner permissions" | "must," not "should" |
| "**Concurrent reviews:** Your team…" (list label bolded) | "Concurrent reviews: Your team…" | Don't bold list labels — only UI/status values |
| "the relevant box (section)" | "the **Private package registries** box" | Match the real UI label; bold it |
| "Snyk API & Web finds… Snyk API & Web investigates…" | "Snyk finds… Snyk investigates…" | Full product name once, then "Snyk" |

For full before/after worked examples across content types (procedure, conceptual prose, security states, troubleshooting), see `references/editing-examples.md`.

---

## Audience first

Snyk addresses developers as peers — straightforward, professional, human. Match the reader: a developer new to security needs the basics explained clearly; a CISO evaluating SAST tools wants Snyk's edge, not definitions. If you don't know who the audience is, ask before drafting anything substantive.

Reflect Snyk's product attributes in copy: dev-first, automated, scalable, collaborative, continuous. And its core values: relevant (only what the user needs now), simple ("fix with a click"), respectful of the user's time (concise), and consistent (reuse existing terms and patterns).

## Core principles

- **Write for scanning.** People scan; they do not read. Short paragraphs, clear headings, lists where they help.
- **Conclusion first.** Lead with the answer or key point. Supporting detail comes after.
- **Headings are keywords.** A heading should make the topic clear at a glance. Avoid "This guide describes…" openers.
- **Sentence-style capitalization** for headings, titles, and dialog names. Capitalize only the first word, proper nouns, and Snyk product/feature names (Snyk Code, Snyk Container, Priority Score, Snyk Projects). Title Case Like This Is Wrong. (Exception: formal long-form marketing — press releases, ebooks, whitepapers, SEO metadata — may use title case.)
- **Cut filler.** "Follow these steps to change your password," not "Follow these steps in order to change your password."
- **One idea per chunk.** White space between paragraphs helps people locate what they need.

## Document structure

Before drafting a whole page, make two decisions in order. Full templates and the worked detail are in `references/document-structure.md`; the essentials:

**1. Placement — which site section.** `docs.snyk.io` groups content into six sections, chosen by reader intent: **Discover Snyk** (what it is, getting started, release terms), **Platform administration** (manage and operate: hierarchy, Tenants, Groups, Orgs, users, SSO, Broker), **Scan, fix, and prevent** (day-to-day security work), **Developer tools** (technical reference for the CLI, IDE plugins, SCM and CI/CD integrations, API), **Agent security** (Snyk Studio, Agent Scan, Agent Guard), and **Snyk data and governance** (data handling, legal terms, test counts). Place by the reader's primary intent: the Snyk CLI lives under **Developer tools**, so new CLI content goes there even though the CLI runs scans.

**2. Content type — which template.** Pick by what the reader needs, not by subject:

- **Feature page** — operate one feature end to end. Linear and self-contained: value prop → prerequisites → conceptual notes → how-to → settings → use cases → teardown → support.
- **Implementation guide** — a multi-phase rollout. Two-level (a sequenced hub page plus child phase pages) and decision-driven. Its signature is forcing a decision *before* the steps, so the content reads as guidance, not reference.
- **Getting started guide** — zero to a first result, fast. Lightest type: "what you'll do here" → informal `{% hint %}` prerequisites → task sections in first-encounter order → orienting tables → one concrete procedure → handoff links.
- **Reference page** — look up a fact, role, code, or matrix. Defining intro → categorized list of entities → short "how they relate" section → lookup tables (the core) → link to the related task. Keep prose minimal.

Two habits separate the types: feature and reference pages are self-contained and linear; implementation and getting started guides lead with a roadmap and cross-link out rather than containing everything. Snyk docs render in GitBook — use the real components (`{% hint %}`, `{% stepper %}` / `{% step %}`, `{% details %}`, `{% tabs %}`) rather than generic "callout" or "expandable" language. See the reference file for which component does what.

## Voice and tone

### Active voice

Subject does the action.

- Good: You can change your password.
- Bad: Passwords can be changed by users.

### Present tense

Avoid future tense ("will be") and vague time words ("currently"). Use present participle only for transitional states ("Importing…", "Updating configuration…").

- Good: After you click **Start**, the start screen appears.
- Bad: After you click Start, the start screen will appear.

### Pronouns

- Default to second person ("you") or imperatives ("Click **Start**").
- **Refer to the company as "Snyk," not "we."** Keep focus on the customer. Use **"Snyk recommends,"** not "we recommend." Exception: privacy and security messaging where Snyk must be named as the speaker ("We've detected a critical vulnerability in your repository…").
- Never first-person singular ("I").
- **Neutral pronouns**: "they/them/their" as the default. Never "he/she," never "one" as a pronoun.

### Contractions

**Avoid contractions.** Write "it is," "you are," "do not," "cannot." This is the default for documentation, security advisories, compliance, and reference material. Contractions are acceptable only in explicitly casual marketing, blog, or onboarding copy where they avoid sounding stiff.

### Avoid weakening words

- **Modals (may, should, might): avoid them — they are ambiguous.** Replace with a definite statement, a conditional, or "can"/"must". "Snyk identifies vulnerabilities," not "Snyk may identify vulnerabilities." "You must have Account Owner permissions," not "you should have." "A vulnerability is not relevant when your system has the latest patches," not "may not be relevant." Use "can" only for genuine capability ("Static analysis can increase false positives").
- **"Please," "sorry," "thank you"**: drop them. Reserve "please" for genuine inconvenience (an outage, a long wait) or when Snyk is at fault.
- **Subjective/empty words** (simply, easy, fast, just, actually, literally, currently): cut them.

### Brand possessives

Avoid them. Don't use the possessive of the company name unless grammar requires it.

- Good: The Priority Score feature in Snyk Code ranks vulnerabilities.
- Bad: Snyk Code's Priority Score ranks vulnerabilities.

### Punctuation in tone

- **No exclamation points** except for genuinely exciting messages. In running prose, replace "!" with ".".
- **No semicolons.** Split into two sentences, or use an em dash where a connector is needed.

---

## Global, inclusive, bias-free

Snyk's audience is global, including many non-native English speakers.

- **Gender-neutral terms.** "Chairperson," not "chairman." "Salesperson," not "salesman." "Humanity/people," not "mankind." "Effort/capacity," not "manpower." Use "they/them" as the default.
- **People-first for disability.** "People with disabilities," not "the disabled." Don't use disability terms metaphorically ("crazy," "insane," "blind to," "tone-deaf").
- **Inclusive technical terms.** "Allowlist" and "blocklist," not "whitelist" and "blacklist." "Leader/follower," not "master/slave." "Main/controller," not "master." "Retrospective" or "incident retro," not "postmortem."
- **Note:** do not modify "whitelist"/"blacklist" when they appear inside software, commands, or config the user actually runs.
- **No slang, idioms, or US-centric metaphors.** No "home run," "ballpark figure," "demilitarized zone."
- **No Latin abbreviations.** "For example" (not e.g.), "that is" (not i.e.), "and so on" (not etc.), "through"/"using" (not via), "note" (not N.B.).
- **US English spelling.** "Analyze," "color," "favorite," "gray," "afterward."

## Accessibility

- **Alt text on everything non-text.** Graphics, video, decorative icons. (See `references/screenshots-and-diagrams.md` for alt-text rules.)
- **All copy must be live text**, not embedded in images.
- **Don't rely on color alone.** "Click the green button" excludes color-blind readers. Name the button instead.
- **Don't rely on direction alone.** "In the dialog on the left" fails for screen-reader users. Name the dialog or its title.
- **Don't rely on spatial references.** Use "earlier"/"later" or "preceding"/"following," not "above"/"below."
- **Descriptive link text.** Avoid "Learn more" and "Click here." Use text that says where the link goes ("Read the Snyk Code documentation").
- **Document keyboard shortcuts** for anyone who can't use a mouse.

---

## Lists

- **Bulleted** when order doesn't matter; **numbered** for procedures (a sequence of steps).
- **Imperative mood** for procedure steps: "Click **Start**." Not "You should click the Start button."
- **Parallel construction**: if one item starts with a verb, all items start with a verb in the same tense.
- **Capitalization and end punctuation**: complete sentences get a capital and a period; fragments completing the intro sentence are lowercase with no end punctuation.
- **No commas or semicolons** at the ends of list items.

---

## Punctuation and formatting

### Placeholders (replaceable values)

Use *italics* for values the user must replace.

- Example: `git clone https://github.com/`*your-username*`/`*your-repo*`.git`
- Example: Navigate to **Settings** > **Organization** > *your-org-name*.

### Spacing

One space after a period.

### Specific marks

| Mark | Rule |
|---|---|
| `&` (ampersand) | Don't use. Spell out "and". |
| `'` (apostrophe) | Don't use in plurals of abbreviations or decades. "APIs," "1990s." |
| `:` (colon) | Use to introduce a list or definition. After a colon mid-sentence, the next word is lowercase unless it's a proper noun. In a title, capitalize the first word after the colon. |
| `,` (comma) | Serial (Oxford) comma. Avoid comma splices. |
| `-` (hyphen) | Combines words: client-side, read-only. Don't hyphenate adverbs ending in -ly. |
| `–` (en dash) | Ranges meaning "through": pages 37–59, 8:00 AM–5:00 PM. |
| `—` (em dash) | Strong break in a sentence. **Put spaces on both sides.** Use the em dash, not a double hyphen (`--`). Do not use an em dash to introduce a list — use a colon. |
| `!` | Only for genuinely exciting messages. |
| `;` | Don't use. Split the sentence or use an em dash. |

### Plurals

Don't use "(s)" to indicate a plural. Use the plural form, or "one or more."

- Good: …displays one or more repositories.
- Bad: …displays the repository(s).

---

## Numbers, dates, and time

- **Spell out** zero through nine. **Numerals** for 10 and greater.
- **Numerals always** for measurements, time, percentages, and any list where one item needs a numeral.
- **Spell out numbers that begin a sentence.**
- **Spell out ordinals**: "first," not "1st."
- **Thousands separators**: comma for 4+ digits (1,000).
- **Decimals**: period, not comma. 5.25MB.
- **Units**: no space between number and unit — 5GB, 5.25MB, 1MB.
- **Drop trailing zeros** unless they convey precision ("5%," not "5.0%").
- **Dates**: prefer words + numbers (April 15, 2026). For a numerical form, use forward slashes (04/15/2026); avoid the purely numerical form for international audiences.
- **Times**: colon-separated (1:49 PM), with **AM/PM in caps, no periods**.
- **Time ranges**: en dash, no spaces (8:00 AM–5:00 PM).

---

## Word choice

### Simple beats complex

Prefer the plain word: use (not utilize), start (not commence), before (not prior to), if (not in the event that), ensure (not make sure), about (not with regard to), because (not due to the fact that), must (not is required to), can (not is able to / has the ability to), now (not at this time), contact (not reach out), continue (not go ahead), find (not seek out). Cut redundancy: "return" (not return back), "revert" (not revert back), "total" (not a total of). The full list is in `references/terms-and-pairs.md`.

### Tricky usage

- **"After," not "once"** to mean a sequence ("once" is ambiguous).
- **"Only"** goes immediately before the thing it limits.
- **"Navigate to," not "go to."**
- **"Visit," not "see"** when referring a reader to a page (better for screen readers).

### Snyk-specific terminology (these distinctions carry meaning)

- **Vulnerability vs. issue.** Use **vulnerability** for security problems. Use **issue** only for licensing problems (or a mixed group that includes a license problem). Never swap them.
- **Plan, not tier.** Snyk offerings are plans: Free, Team, Business, Enterprise.
- **Container, not Docker.** "Container" is generic; Docker is one engine among many. Same for "container registries," not "Docker registries."
- **Git repo for repositories; SCM integration for the integration.** Use "Git repo" / "Git repository" for the repository itself (and "hosted Git repo" for on-prem). Use **"SCM integration," not "Git integration,"** when referring to the integration that connects Snyk to a source code management system (GitHub, GitLab, Bitbucket, and so on).
- **SCA ≠ static code analysis.** SCA is software composition analysis. Don't abbreviate "static code analysis" as SCA.
- **IaC**, always — never "IAC."
- **"Enable" — be careful.** Don't use "enable" for what software lets a user do ("enables users to scan…"); rewrite as "you can…" or an imperative. "Enable" is fine for activating a feature ("Enable two-factor authentication"). "Allow" means giving permission. "Lets…" is an acceptable casual alternative.
- **CI/CD.** Spell out as "continuous integration/continuous delivery" (no spaces around the slash) by default. "Deployment" is acceptable for customers/partners who use that form.
- **fintech** — lowercase, except at the start of a sentence.
- **Capitalize Snyk-defined nouns**: Project, Projects, Organization, Group. Where possible, avoid the generic forms; prefer "company" over a generic "organization."

For the full term list, security acronyms, verb/noun pairs, and compound-word rules, see `references/terms-and-pairs.md`.

---

## Referring to the UI in documentation

This is about how docs *describe* the UI, not how in-product strings are written (that's the `ux-copy` skill).

### Format

- **Bold** for UI element names. Match the product's capitalization exactly. Don't use quotation marks.
  - Good: Click **Start** to scan for vulnerabilities.
  - Bad: Click "Start" to scan for vulnerabilities.
- **Bold state, status, and badge values too** — when they appear in the UI, CLI, or IDE. Treat them like UI element names: "the finding has a **Not fixed** state"; "change the state to **Invalid**".
- **Bold only UI/CLI/IDE elements and status values.** Do not bold lead-in labels in a bulleted list, defined terms, or words for emphasis. Bold is reserved for things the reader sees on screen.

### Be direct

Drop the noun naming the element type unless it's needed for clarity.

- Good: Click **Update**. / Open **Settings**.
- Bad: Click the **Update** button. / Open the **Settings** menu.

### Action verbs

- **Click** an action — buttons and links: "Click **Save**." (Desktop, developer-first audience.)
- **Select** an option — check boxes, radio buttons, list items, menu items: "Select the **Enable** check box."
- **Press** a keyboard key: "Press **Enter**."
- The distinction is action vs. option, not input device.

### Navigation

- "Navigate to," not "go to."
- Greater-than symbol with spaces between sequential steps: Navigate to **Settings** > **Notifications**.

### Links

Build the hyperlink into the sentence, with descriptive text.

- Good: Learn more in the Snyk IaC documentation.
- Bad: Click here to learn more about Snyk IaC.

---

## Abbreviations and acronyms

- Spell out an acronym only the **first time it appears on a page**, with the acronym in parentheses: "static application security testing (SAST)." After that first occurrence, use **only the acronym** for the rest of the page — don't spell it out again.
- Universally known acronyms (API, HTML, URL) don't need spelling out at all.
- **CI/CD** uses a slash, no spaces.

---

## Quick reference: things people get wrong

- "Allowlist" / "blocklist" — one word each. Never "whitelist," "blacklist," or "denylist."
- "Log in" (verb) / "login" (noun) — not "sign in."
- "Set up" (verb) / "setup" (noun). "Back up" (verb) / "backup" (noun).
- "Dropdown" — one word, noun and adjective.
- Hyphenate the adjective form: "open-source" (adj) / "open source" (noun); "cloud-native" / "cloud native"; "real-time" / "real time"; "hard-coded" / "hard coded"; "client-side" / "client side."
- Em dash — spaces on both sides. No semicolons. No "!".
- "After," not "once." "Navigate to," not "go to." "Visit," not "see" (a page).
- "For example," not "e.g."
- **vulnerability** for security, **issue** for licensing — never swap.
- **plan**, not "tier." **container**, not "Docker." **Git repo** for a repository; **SCM integration** for the integration (not "Git integration").
- **IaC** (not "IAC"). **JavaScript** (not "JS"). **Google Cloud** (not "GCP").
- **Vulnerability DB**, not "VulnDB." **SBOM**, never "SBoM."
- "30-day trial" — always hyphenated.
- Numbers: spell out 0–9, numerals 10+. AM/PM in caps. Units with no space (5GB).
- Sentence case for headings (title case only for press releases/ebooks/whitepapers/SEO).
- "Snyk recommends," not "we recommend."

---

## Bundled references

- `references/terms-and-pairs.md` — Full term list: verb/noun pairs, compound words, hyphenation, Snyk and partner product names, security acronyms, and how to name UI elements in docs.
- `references/editing-examples.md` — Full before/after worked examples across content types. Read when you want a model to follow for a procedure, concept, security/states topic, or troubleshooting page.
- `references/document-structure.md` — Where a page belongs (the six site sections) and how to lay it out: the four content-type templates (feature page, implementation guide, getting started guide, reference page), plus tables, decision-forcing, and GitBook components.
- `references/screenshots-and-diagrams.md` — When and how to use screenshots and diagrams in Snyk docs.
- `references/ms-fallback.md` — Microsoft Writing Style Guide rules for topics Snyk doesn't cover.
- `references/decisions-log.md` — Record of every resolved conflict and how each was decided.
