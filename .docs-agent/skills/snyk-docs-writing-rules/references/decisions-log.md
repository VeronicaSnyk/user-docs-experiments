# Decisions log

The authoritative record of every resolved conflict behind this skill. Two kinds of conflict are tracked:

- **Part A — Snyk source merge (2026-06-09):** conflicts between the two Snyk sources combined into this skill — the older `snyk-writing-rules` skill and the consolidated `snyk-style-guide.md` (by Veronica Cernea).
- **Part B — Snyk vs. Microsoft (2026-05-28):** older conflicts between Snyk's rules and the Microsoft Writing Style Guide, carried over from the original skill.

Not needed for day-to-day writing — useful when someone asks why a rule reads the way it does, or wants to reopen a decision.

Precedence for this skill: (1) these resolved Snyk rules; (2) anything else Snyk's sources cover, more specific/recent winning; (3) the Microsoft Writing Style Guide as the final fallback.

---

## Part A — Snyk source merge (resolved 2026-06-09)

| # | Topic | Decision | Source chosen | Rationale |
|---|---|---|---|---|
| A1 | Replacement for "blacklist" | **blocklist** (pair: allowlist / blocklist). Never "denylist." | Skill | Matched antonym pair; most common in security tooling. |
| A2 | "dropdown" as adjective | **dropdown** — one word, noun and adjective. | Skill | One simple rule; matches current usage. |
| A3 | Number spell-out cutoff | Spell out **zero through nine**; numerals **10+**. | Skill | Dominant technical convention. |
| A4 | AM/PM format | **AM / PM** — caps, no periods. | Skill | Matches Snyk UI and the time-range rule. |
| A5 | "pop-up" | Prefer **dialog** / **window**; keep "pop-up" (hyphenated) only for a transient popup. | Style guide | Matches MS discouragement of "pop-up." |
| A6 | "radio button" | **radio button**. | Skill | "option button" is dated. |
| A7 | "cloud native" hyphenation | **cloud-native** (adj) / **cloud native** (noun). Locked 2026-06-09 (user). | Skill | One consistent compound-adjective rule, matching open-source/real-time. CNCF's unhyphenated form was considered and rejected. |
| A8 | "open source" hyphenation | **open-source** (adj) / **open source** (noun). | Skill | Standard grammar; consistent with A7. |
| A9 | "hard coded" hyphenation | **hard-coded** (adj) / **hard coded** (noun). | Skill | Standard grammar; consistent with A7. |
| A10 | First person "we / us" | Avoid by default; use **Snyk** and **"Snyk recommends."** Allow "we" only in security/privacy alerts naming Snyk. | Hybrid | Blanket ban forces awkward alert copy; narrow exception serves UX. |
| A11 | Contractions | **No contractions** by default; exception only for casual marketing/blog/onboarding. | Style guide (+ narrow skill exception) | Cleaner for product UI and formal docs. |
| A12 | Semicolons | **Don't use** — split sentences or use an em dash. | Style guide | Simpler; "sparingly" reaches the same outcome. |
| A13 | Space before MB/GB | **No space**: 5GB, 5.25MB, 1MB. | Style guide (user's call, 2026-06-09) | House rule; consistency with the Snyk Grammarly standard. |
| A14 | Title case for headings | **Sentence case** for product/UI/docs; title case allowed only for press releases, ebooks, whitepapers, SEO metadata. | Style guide | Exception is scoped to non-product content, so both coexist. |
| A15 | "enable" | Don't use "enable" for software capability; rewrite as "you can…" or imperative. "Enable" only for activating a feature; "lets…" acceptable casually. | Skill | More precise; avoids vague "enables users to." |
| A16 | CI/CD spelled out | **continuous integration/continuous delivery** — no spaces around the slash. | Style guide | Matches the "CI/CD" acronym form. |
| A17 | IaC vs IAC | Always **IaC**. | Skill | Industry standard; settles the open question. |
| A18 | Passive voice | Active by default; passive acceptable for **alerts and notifications**. | Style guide | Matches real notification patterns. |
| A19 | fintech | Lowercase **fintech**, except at the start of a sentence. | Both agreed (clarified by user) | Both sources already lowercase; sentence-start caveat added. |

### Coverage merged in (not conflicts)

- From the style guide: the screenshots and diagrams sections, additional UI term swaps, additional inclusive-language terms, and the plain-language replacements. These live in `SKILL.md`, `references/screenshots-and-diagrams.md`, and `terms-and-pairs.md`.
- From the skill: the full Microsoft fallback, serial comma, en dash for ranges, italic placeholders for replaceable values, folder vs directory, merge request / pull request, and the fuller security-acronym list.

### Scope decision — UI copy removed (2026-06-09, user)

In-product UI copy authoring rules — UI copy length limits (button/control/title/description word counts), ALL-CAPS statuses and navigation headings, and the in-product message patterns (error/notification/placeholder/confirmation-dialog copy) — were **removed** from this skill. They are owned by the separate **`ux-copy`** skill. This skill keeps only the guidance for *referring to* the UI when documenting it (bold element names, click/select/press, navigation breadcrumbs, links). Decisions A2, A4, A5, A6 still apply as terminology when docs mention those elements.

---

## Part B — Snyk vs. Microsoft (resolved 2026-05-28)

### Em dash spacing

- **Decision:** Snyk rule — spaces on both sides of the em dash.
- MS had said: no spaces. Snyk's choice is a deliberate divergence from US convention.

### "Sign in" vs "Log in"

- **Decision:** Snyk rule — "log in" (verb) / "login" (noun).
- MS had said: always "sign in / sign out." Snyk's choice aligns with developer tooling.

### Allowlist/blocklist (one word) vs allow list/block list (two words)

- **Decision:** Snyk rule — one word ("allowlist," "blocklist"), replacing "whitelist"/"blacklist."
- MS (as of Jan 2026) had said: two words.

### "Click" vs "Select"

- **Decision:** Snyk rule — "click" for actions (buttons, links); "select" for options (check boxes, radio buttons, list items). Distinction is action vs. option, not input device.
- MS had said: prefer "select" universally as input-neutral.

### End punctuation on short headings and list items

- **Decision:** Snyk rule — complete sentences get a period; fragments don't. Length doesn't change it.
- MS had said: skip end punctuation on items of three or fewer words regardless.

### Contractions

- **Decision (updated 2026-06-09, see A11):** no contractions by default; casual-copy exception only.
- MS had said: use contractions everywhere for friendliness.

### Heading capitalization

- **Decision:** sentence-style capitalization, with Snyk product/feature names keeping canonical capitalization. (Title-case exception for formal long-form marketing added 2026-06-09, see A14.)
- MS had said: sentence-style capitalization.

---

## How to reopen a decision

1. Move the relevant entry to a new "Active conflicts" section at the top of this file.
2. State the competing options again.
3. Update the affected file(s) — `SKILL.md`, `terms-and-pairs.md`, `screenshots-and-diagrams.md`, or `ms-fallback.md`.
4. Note the change date.
