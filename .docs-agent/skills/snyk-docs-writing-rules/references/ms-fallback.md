# Microsoft Writing Style Guide: fallback rules

Topics where Snyk's rules are silent and the Microsoft Writing Style Guide gives clear guidance. Apply these only when Snyk's own rules don't cover the situation. Where Snyk and MS conflict, **Snyk wins** — see `decisions-log.md` for the resolved decisions.

The MS guide is ~1100 pages; this is a working summary. For anything not here, refer to https://learn.microsoft.com/en-us/style-guide/.

---

## Capitalization

Sentence-style capitalization is the MS default and Snyk's: capitalize only the first word, proper nouns, and the first word after a colon. Snyk additions: keep Snyk product/feature names in their canonical capitalization; statuses/badges and navigation section headings are ALL CAPS.

Always capitalize: proper nouns and brand names; the first word of a sentence; the first word after a colon in a title; the first word after a colon mid-sentence only if it's a proper noun or starts a direct quotation.

## End punctuation

Skip end punctuation on titles, headings, subheadings, UI titles and labels, buttons, and short fragments. Keep it on body copy and list items that are complete sentences. (Snyk rule: complete sentences get a period; fragments don't.)

## Contractions

The Snyk rule overrides MS here: **avoid contractions** by default (it is, you are, cannot). Contractions are acceptable only in explicitly casual marketing/blog/onboarding copy. When you do use them, don't mix contracted and full forms in the same UI surface, never contract a noun + verb, and avoid awkward forms (there'd, it'll, they'd).

## Sentence structure

- **Start with a verb.** Edit out "You can" and "There is / are" where you can.
- **Be brief.** Replace multi-word phrases with single words: "to" (not in order to), "also" (not in addition), "help" (not facilitate), "tell" (not inform), "remove" (not extract).
- **Avoid weak verbs** (be, have, make, do, get). "Back up the file," not "Make a backup of the file."

## UI elements: detailed terminology (MS reference; Snyk decisions take precedence)

- **Click** is the Snyk default for buttons and links; **select** for options (check boxes, radio buttons, list items); **press** for keys; **tap** only for touch-specific content.
- **Check box** — two words (Snyk agrees).
- **Dropdown** — one word, noun and adjective (Snyk overrides MS's adjective-only restriction).
- **Radio button** — Snyk keeps "radio button" (MS's older "option button" is dated).
- **Dialog / window** — Snyk prefers these over "pop-up."
- **Pane** — the sub-area of a window (not "blade").
- **Log in / login** — Snyk forms (MS prefers "sign in"; Snyk overrides).
- **Allowlist / blocklist** — Snyk forms, one word each (MS prefers two words; Snyk overrides). Never "denylist."
- **Keyboard shortcuts**: plus sign, no spaces (Ctrl+S). Bold the keys. Don't say "Shift+click" — say "Select **Shift** while clicking."
- **Menu sequences**: greater-than symbol with a space on each side: **Accounts** > **Other accounts** > **Add an account**.

## Numbers (where Snyk is silent)

- Spelled out: zero through nine; at the start of a sentence; one of two adjacent numbers ("two 3-page articles"); ordinals.
- Numerals: 10 and greater; numbers in UI; measurements, time, percentages, dimensions; a round number ≥ 1 million ("5 million").
- Negative numbers: use a minus sign (−), not an en dash.
- Snyk specifics: AM/PM in caps; units with no space (5GB).

## Voice and tone (MS top-10, reconciled with Snyk)

1. Bigger ideas, fewer words.
2. Write like you speak; read it aloud.
3. Project friendliness — through word choice and rhythm, since Snyk avoids contractions.
4. Get to the point fast; front-load keywords.
5. Be brief.
6. Sentence case by default (Snyk product names keep canonical capitalization).
7. Skip periods on titles, headings, and short list items.
8. Serial comma always.
9. One space after periods. (Em dash: spaces on both sides — Snyk rule.)
10. Revise weak writing; start with verbs.

## Bias-free language (MS goes deeper than Snyk)

### Disability

- People-first or identity-first, depending on community preference (many Deaf and autistic people prefer identity-first). Default to people-first for medical conditions.
- Don't use "suffers from," "afflicted with," "victim of." Use "has" or "with."
- Don't use "normal" or "healthy" to mean non-disabled.
- Don't use disability terms metaphorically (blind to, tone-deaf, lame, crazy, OCD about).

### Race, ethnicity, nationality

- Don't assume race or nationality from a name.
- Black and White as racial descriptors are capitalized in MS style.
- For a global audience, "people in the US," not "American" as a synonym.

### Gender

- Default to singular "they." Don't gender job titles (chairperson, firefighter, police officer). Don't use "guys" for mixed groups.

### Age and socioeconomic

- Don't reference age unless relevant; don't use "elderly" (use "older adults"). "Low-income," not "poor." "People experiencing homelessness," not "the homeless."

## Specific words MS handles that Snyk doesn't

- **and/or** — don't use. Pick one or rewrite.
- **above / below** as positional references — avoid; use "earlier"/"preceding"/"following" or named cross-references.
- **insure / ensure** — "ensure" means to make certain; "insure" relates to insurance. (Snyk uses "ensure.")
- **its / it's** — "it's" = "it is/has"; "its" = possessive.
- **sorry** — OK in error messages when the product is at fault, or for serious situations like data loss. Avoid "Hmm" and "Oops."

## When MS contradicts itself

Prefer (1) the more recent guidance, (2) the rule that's clearer/shorter/more accessible, (3) the rule more specific to your case.
