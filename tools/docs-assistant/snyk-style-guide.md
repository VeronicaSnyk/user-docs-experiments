# Snyk Style Guide — consolidated writing rules

**Purpose.** Single source of truth for how Snyk technical content is written. Consolidated from the UX Copy guide, Capitalization rules, Inclusive Language guide, Snyk terms (correct spelling), Using screenshots, Using diagrams, and the Grammarly Snyk Style Guide CSV.

**How to use.** Every time Claude writes or rewrites Snyk content, this guide is the initial input. Where the source documents conflict, the most recently updated source wins; specific conflicts are flagged inline with `⚠ CONFLICT`.

**Source dates resolved against.** All `WS-*` and `Docs-*` PDFs were exported 20 May 2026\. The Grammarly Style Guide CSV is dated 27 April 2026\. Where the Grammarly CSV conflicts with a PDF, the PDF wins.

---

## 1\. Audience and product principles

Snyk content addresses developers as peers. Every word should reflect Snyk's core values:

- **Relevant.** Provide only what the user needs for the current task.  
- **Simple.** Aim for "fix with a click."  
- **Value user time.** Be concise.  
- **Consistent.** Reuse existing terminology and patterns.

Developers interact with Snyk in two modes: (1) as a checkpoint required by their company, and (2) as a tool they actively choose to improve their code. Both should inform tone.

Reflect these product attributes in copy: **dev-first**, **automated**, **scalable**, **collaborative**, **continuous**.

## 2\. Tone and voice

- **Address users as peers.** Straightforward, professional, human.  
- **Use active voice.** *"Fix the vulnerability"* — not *"the vulnerability was fixed."* Reserve passive voice for alerts and notifications.  
- **Use second person.** Use *you / your* to refer to the user.  
- **Use neutral pronouns.** *they / their / them* — never *he/she*, never *one*.  
- **Snyk is Snyk.** Refer to the company as *Snyk*, not *we*.  
- **Avoid fluff.** No *please*, *sorry*, or *thank you* unless the user is being asked to do something significantly inconvenient.  
- **Don't apologize.** Drop *sorry* unless the situation involves serious data loss.  
- **Take it seriously, not too seriously.** Snyk is loyal, friendly, understanding, caring, protective.  
- **No contractions.** Write *it is*, *you are*, *cannot* — not *it's*, *you're*, *can't*.  
- **Avoid meaningless emphasis.** Drop *actually*, *literally*, *simply*, *just*, *currently*.  
- **No exclamation points** except for genuinely exciting messages. In running prose, replace `!` with `.`.

## 3\. Grammar and sentence construction

- **Present tense by default.** Describe what the user can do now.  
- **Avoid future tense.** Replace *will be* with present tense.  
- **Present participle is for transitional states only.** *Updating configuration…*, *Importing…*  
- **No gerunds in descriptions.** Use *Enable*, not *Enabling*.  
- **Page titles use nouns.** Controls use nouns or verbs depending on context.  
- **Avoid semicolons.** Break into two sentences. Use a dash instead where a connector is needed.  
- **Use em dash (`—`) not double-hyphen (`--`).**  
- **Use colon (`:`) instead of em dash to introduce a list or definition.**  
- **Replace `(s)` with `s`.** Easier to parse.  
- **Replace `&` with `and`.**  
- **Replace `and / or` with `and`.**  
- **Spell out ordinals.** *first*, not *1st*.  
- **Spell out numbers one through ten.** Use numerals for 11 and above. Use `1,000` (with comma) for thousands.  
- **Use American spelling.** *color*, *favorite*, *gray*, *afterward*.  
- **Time:** *a.m.* / *p.m.* (lowercase with periods).  
- **Units:** `5 GB` (space between number and unit, except `1MB` per Snyk house style — ⚠ CONFLICT: most style guides use a space; verify before publishing).

### Plain-language replacements

Prefer the right column.

| Replace | With | Reason |
| :---- | :---- | :---- |
| In order to | to | Shorter |
| Prior to / In advance of | before | Simpler |
| Once | after | Avoids ambiguity |
| Within | in | Shorter |
| In the event that / in the event of | if | Shorter |
| As long as | if | Shorter |
| Accordingly | so | Shorter |
| Due to / due to the fact that | because | Cause and effect |
| Since (for cause) | because | Reserve *since* for time |
| With regard to | about | Shorter |
| With the exception of | except | Shorter |
| On behalf of | for | Shorter |
| As well as | and | Shorter |
| In advance of | before | Shorter |
| Commence / Commencement | start | Simpler |
| Utilize / utilization / usage | use | Plainer |
| Is able to | can | Shorter |
| Has the ability to | can | Shorter |
| Is required to | must | Shorter |
| You need to | you must | Stronger |
| It is recommended that | Snyk recommends | Active voice |
| This functionality enables the users to | you can | Active, 2nd person |
| First of all | first | Shorter |
| A lot | many | More precise |
| At this time | now | Shorter |
| Will be | (present tense) | Avoid future tense |
| via | through / using / by means of | Avoid Latinisms |
| e.g. | for example | Avoid Latinisms |
| i.e. | that is | Avoid Latinisms |
| etc. | and so on | Avoid Latinisms |
| N.B. | note | Avoid Latinisms |
| reach out | contact | Clearer |
| go ahead | continue | Shorter |
| on the other hand | but | Shorter |
| seek out | find | Simpler |
| not only … but also | also | Simpler |
| return back | return | Redundant |
| revert back | revert | Redundant |
| cancel out | cancel | Redundant |
| a total of | total | Redundant |
| go to | navigate to | UI convention |
| see (a page) | visit | Better for screen readers |
| above / below (in a page) | earlier / later, preceding / following | Accessibility — screen readers don't have spatial context |

## 4\. Capitalization

- **Sentence case for almost everything** — titles, headings, descriptions, buttons. *"Snyk Code provides developer-first security"*, not *"Snyk Code Provides Developer-First Security"*. Sentence case is the software industry standard, reduces cognitive load, and makes product names stand out.  
- **Capitalize company and product names.** *Snyk*, *Snyk Code*, *Custom Rules*, *PR* (when product feature).  
- **Capitalize team names; lowercase "team".** *the Snyk Marketing team*.  
- **Capitalize job titles, lowercase general roles.** *Ravi Maira, Director of Snyk Product Marketing* vs. *Ravi Maira is a director at Snyk*.  
- **Capitalize Snyk-specific nouns:** *Project*, *Projects*, *Organization*, *Group*. Where possible avoid the generic *project / organization / group* to reduce confusion — prefer *company* over the generic *organization*.  
- **Statuses and badges: ALL CAPS** — e.g. `CONNECTED`.  
- **Navigation headings: ALL CAPS.** Menu links inside those sections use sentence case.  
- **Exception for formal long-form content.** Press releases, ebooks, whitepapers, journal articles, and SEO page metadata may use title case.

## 5\. Punctuation

- **Periods** only at the end of full-sentence descriptions. No periods on titles, fragments, buttons, or short notifications.  
- **Exclamation points** only for truly exciting messages.  
- **No semicolons.** Split into two sentences or use a dash.

## 6\. Length and layout

People scan; they do not read. Put the most important information first.

| Element | Rule |
| :---- | :---- |
| Titles | 3–4 words |
| Descriptions | No more than 4 lines |
| Buttons | Up to 3 words; use verbs |
| Controls | Up to 4 words; use active voice |

## 7\. Word choice — UI verbs and nouns

| Replace | With | Note |
| :---- | :---- | :---- |
| click on / tap on | click / tap | Drop the *on* |
| select (a button) | click | Use *click* only for buttons, not multi-option menus |
| check / uncheck (a check box) | select / clear | Standard for check boxes |
| hit / strike (a key) | press |  |
| key-in / type in | enter / type |  |
| execute (a command) | run |  |
| boot up | start / turn on |  |
| bring up | open / display |  |
| switch on / shut off | turn on / turn off | UI text |
| restart / re-start | restart | One word |
| double click / doubleclick | double-click | Hyphenated |
| rightclick / leftclick | right-click / left-click | Hyphenated |
| single-click / singleclick | click |  |
| drag-and-drop | drag and drop | UI action |
| drop-down (noun) | dropdown | Noun form, one word |
| drop down (menu control adjective) | drop-down | Hyphenated as adjective for menu controls. ⚠ CONFLICT: the Grammarly CSV contains both rules — use *dropdown* for the noun and *drop-down* only as an adjective modifying *menu* or *list* |
| combo box | list |  |
| dialog box | dialog | The container is a *dialog* |
| pop-up | window |  |
| radio button | option button |  |
| blade | pane | Describing UI sections |
| hotkey | keyboard shortcut |  |
| abort / terminate | stop / cancel / end |  |
| grayed out / greyed out | unavailable |  |
| info | information |  |
| ok | OK (UI) / okay (prose) |  |
| yes/no | yes or no |  |
| passcode | password |  |
| home page / homepage | homepage | UI |
| scrollbar | scroll bar | UI elements |
| toolbar | tool bar | UI elements |
| on-screen | onscreen | UI |
| back-end | backend |  |
| enduser | end user |  |
| webpage | web page |  |
| Click the Save button | Click **Save** | Don't repeat *button* |
| Open the Settings menu | Open **Settings** | Drop trailing *menu* / *option* |

## 8\. Inclusive language

Snyk writes to a global audience. Be aware of implicit biases; have peers with different backgrounds spot-check.

### Words to avoid (and replacements)

| Avoid | Use instead |
| :---- | :---- |
| crazy / insane | a lot, many, thousands, astounding |
| he / she | they (or *you* directed at the reader) |
| him / her | them |
| one (as pronoun) | they / you |
| master | main, controller |
| master / slave | leader / follower |
| manpower | effort, power |
| mankind | humanity, people |
| postmortem | retrospective, retro, incident retro |
| salesman | salesperson |
| whitelist | allowlist (or *unblocked list*) |
| blacklist | denylist (or *blocked list*) |

**Note.** Do not modify *whitelist* or *blacklist* when they appear inside software or commands the user actually runs.

### Other accessibility considerations

- **Descriptive links.** Avoid *Learn more* or *Click here*. Use text that tells the user where the link goes — e.g., *Read the Snyk Code documentation*.  
- **Above / below.** Replace with *earlier / later* or *preceding / following* for screen-reader compatibility.  
- **All copy must be live text**, not embedded in images.  
- **Place instructions before the input field:** Label → Assistive text → Control.

## 9\. Snyk-specific terms — correct spelling (A–Z)

For definitions, see the Snyk Glossary.

**\#**

- **30-day trial** — always hyphenated. Not *30 day trial*.

**A**

- **Amazon / AWS** — don't drop the brand prefix and don't swap the two: *Amazon EC2*, *Amazon ECS*, *Amazon EKS*, *Amazon ECR*; *AWS Fargate*, *AWS IAM*, *AWS KMS*, *AWS Lambda*, *AWS CodePipeline*, *AWS CodeCommit*, *AWS CodeBuild*.  
- **add-on** (noun), **add on** (verb), **Add-on** (proper noun, as in *Heroku Add-on*).  
- **agile** — lowercase as a general adjective. *Agile* capitalized only as the methodology.  
- **AI-BOM** — the Snyk-approved format. Lowercase `aibom` only inside command names.  
- **allow** — *to give permission* (not to empower). Compare *enable* below.  
- **allowlist** — replaces *whitelist*.  
- **APK**.

**B**

- **Bitbucket** — one word, only the first B is capitalized.  
- **blacklist** — do not use. Use *denylist*.  
- **built-in** (adj), **built in** (noun).

**C**

- **cheat sheet** — two words.  
- **CI/CD** — no spaces around the slash. Spell out *continuous integration/continuous delivery* on first use. *Deployment* may substitute for *delivery* only when writing for a customer or partner who uses that phrasing.  
- **client-side** (adj), **client side** (noun).  
- **Cloud Foundry** — C and F capitalized, space between.  
- **cloud native** — no hyphen (per CNCF guidance).  
- **Cloud Native Application Security (CNAS)** — capitalized when used as a Snyk solution; use the acronym after first use.  
- **codebase** — one word.  
- **Composer** — capitalize the C.  
- **containers** — preferred over *Docker containers*; Docker is one engine among many (CRI-O, etc.).  
- **container registries** — preferred over *Docker registries*.  
- **cross-site scripting (XSS)**.  
- **cybersecurity** — one word.

**D**

- **data center** — two words, no hyphen. Not *datacenter*.  
- **deep link** — two words, lowercase.  
- **denylist** — replaces *blacklist*.  
- **dep** — all lowercase.  
- **Docker** — do not use as a synonym for *container*.  
- **Docker Hub** — two words.  
- **Dockerfile** — one word, capitalized.  
- **DAST** (dynamic application security testing) — acronym after first use.

**E**

- **email** — not *e-mail*.  
- **enable** — describes empowerment. Consider *lets* as an alternative: *Lets users…*  
- **ensure** — preferred over *make sure*.

**F**

- **fintech** — lowercase. ⚠ CONFLICT: the Grammarly CSV (April 2026\) replaces *fintech* with *Fintech*; the Snyk terms PDF (May 2026\) says lowercase. The PDF wins — use **fintech**.

**G**

- **genAI** — lowercase *gen*, capitalize *AI*.  
- **Git repository / Git repo** — preferred over *SCM*. Use *hosted Git repo* for on-prem deployments.  
- **GitHub** — capitalize G and H.  
- **GitLab** — capitalize G and L.  
- **Go** — capitalized. *golang* is the lowercase nickname.  
- **Google Cloud** — preferred over *Google Cloud Platform (GCP)* since 2020\.

**H**

- **hard coded** — two words, no hyphen.

**I**

- **infrastructure as code (IaC)** — not capitalized except as part of a product name. ⚠ The Snyk terms PDF abbreviates this as *IAC*; common industry use is *IaC*. The Grammarly CSV agrees with lowercase. Verify Snyk house standard before publishing.  
- **intent** (Android feature) — capitalize only with the word *Android*: *Android Intents can be embedded.*  
- **issue** — describes licensing problems or a mixed group including licensing. Do not use *issue* for security problems; use *vulnerability*. Do not use *vulnerability* for license problems.  
- **IAST** (interactive application security testing) — acronym after first use.

**J**

- **JavaScript** — capitalize J and S. Do not abbreviate to JS.

**K**

- **knowledge base** — two words, no hyphen.

**L**

- **lifecycle** — one word.  
- **login** (noun): *your login credentials*. **log in** (verb): *log in to the landing page*. Same pattern: *checkout* (noun) / *check out* (verb), *setup* (noun) / *set up* (verb).

**M**

- **man-in-the-middle (MITM)** — hyphenated, lowercase.  
- **merge request (MR)** — GitLab's term for pull request. Lowercase except at sentence start.

**N**

- **.NET** — letters capitalized; period at the start.  
- **Node.js** — capitalize the N; include the `.js`.  
- **npm** — always lowercase.

**O**

- **Object-Graph Navigation Language** — capitalized, hyphenated.  
- **open source** — lowercase, no hyphen.  
- **OpenShift** — O and S capitalized; no space.  
- **OWASP Top 10**.

**P**

- **PaaS** — *Platform as a Service*.  
- **pip** — always lowercase.  
- **plan** — *Free plan*, *Team plan*, *Business plan*, *Enterprise plan*. Do not use *tier*.  
- **pull request (PR)** — lowercase except at sentence start.  
- **PyPI** — written as `PyPI`; pronounced *pie pee eye*.

**R**

- **real time** (noun): *Scan your code in real time.* **real-time** (adj): *Real-time scanning keeps you secure.*  
- **ReDoS** — *regular expression denial of service*.  
- **regex** — *regular expression*.  
- **repository / repositories** (formal), **repo / repos** (informal).  
- **RubyGems** — capitalize R and G.  
- **runtime** — one word.

**S**

- **same-origin policy (SOP)**.  
- **sbt** — always lowercase.  
- **SBOM** — *software bill of materials*. Never *SBoM*.  
- **SDLC** — *software development lifecycle*.  
- **server-side** (adj), **server side** (noun).  
- **Snyk pipe** — lowercase *pipe* (Snyk's is not a product like *Bitbucket Pipes*).  
- **SOC 2** — space between *SOC* and *2*.  
- **software composition analysis (SCA)** — acronym after first use. *SCA ≠ static code analysis.*  
- **standalone** — one word.  
- **SAST** (static application security testing) — acronym after first use.  
- **static code analysis ≠ SCA.** Static code analysis is the parent term of SAST. Do not abbreviate to SCA.  
- **step-by-step** — hyphenated.

**T**

- **taint analysis** — two words.  
- **third-party** (adj): *third-party software*.  
- **tier** — do not use for Snyk offerings; use *plan*.  
- **TypeScript** — camel case.

**U**

- **URI**, **URL**.  
- **username** — one word.

**V**

- **Vulnerability DB / Vulnerability Database** — never *VulnDB*.

**W**

- **Wi-Fi** — always hyphenated; both letters capitalized.  
- **web** — lowercase (except at the start of a sentence).  
- **webhook** — not *web-hook*.  
- **web page** — two words.  
- **web server** — two words.  
- **website** — one word, not *web site*.  
- **whitelist** — do not use. Use *allowlist*.  
- **white paper** — two words.

**Y**

- **Yarn** (noun) / `yarn` (command) — capitalized unless inside a code block.  
- **YAML**.

**Z**

- **Zip Slip** — both words capitalized.

## 10\. UX copy — specific components

### Error messages

- **Structure:** explain what went wrong and provide a way out or a fix.  
- **Tone:** positive and actionable, not technical or blaming.  
- **Avoid jargon:** no *failure*, *illegal*, *fatal error*.

### Notifications

- Short informational message, with a CTA if action is required.  
- Present participle for transitional text: *Importing…*

### Placeholders

- Show a data-format example, not a label.  
- Be consistent — pick *Add* or *Enter* and use it throughout the form.

### Confirmation dialogs

- Ask a clear question: *Delete project?*  
- Confirm-button labels should name the action: *Delete project*, not *Confirm*.  
- For destructive actions, state the consequences explicitly. Cancel buttons must clearly contrast with the destructive action.

## 11\. Using screenshots

**Policy:** prioritize clear text over screenshots. Use screenshots only for complicated processes or to clarify ambiguities.

### When to use

- Multi-step processes where the screenshot supplements, removes ambiguity, or guides.  
- UI changes that need visual exemplification (e.g., a button moved to a non-obvious location).  
- Interaction patterns that are not intuitive.  
- Changelog entries showcasing updates.

If a feature requires a screenshot to be usable, consider whether the UI itself should be improved — flag to Product Design.

### When NOT to use

- The screenshot adds no informational value (decorative).  
- The audience prefers a different format (technical users prefer code samples over UI images).  
- The user can perform the workflow from text alone.  
- What's depicted is obvious (search bar, common icon).

### Audience-based guidance

| Audience | Example doc | Guidance |
| :---- | :---- | :---- |
| Customer workflows (manage risk) | `docs.snyk.io/manage-risk` | Use sensibly for UI-based work |
| Customer workflows (enterprise setup) | `docs.snyk.io/enterprise-setup` | Use to illustrate concepts or key functions |
| Customer workflows (CLI) | `docs.snyk.io/snyk-cli` | Prefer code samples, commands, config examples |
| IDE | `docs.snyk.io/integrate-with-snyk/use-snyk-in-your-ide` | Use rarely or never unless essential |

### How to capture

- **Light mode/theme only.**  
- **Zoom in.** Capture the relevant area, not the whole screen. \~150% zoom.  
- **No annotations or overlays.** No arrows, borders, frames, callouts. Direct attention through cropping and zoom.  
- **Hide sensitive data.** No account IDs, tokens, passwords, customer or user names, real emails. Prefer demo environments; otherwise crop or use the browser Inspect tool. If using Snagit blur, use intensity 12.5 — but note some tools can unblur, so redact robustly.  
- **Crop to content** while keeping enough surrounding context.  
- **No effects** (shadows, borders).  
- **Transparent background.**

### Filename convention

`location-in-ui-feature-or-element-description.png`

- Lowercase only.  
- Words separated by dashes.  
- Include the UI location (if applicable) and a brief description.

Examples:

- `org-settings-iac-detect-config-files-enabled.png`  
- `org-level-member-group-member-details.png`

### Storage and lifecycle

- Source of truth: the docs platform's (GitBook) image library. Do not maintain copies in Google Drive.  
- **Add:** Capture → edit → save with naming convention → in GitBook open a CR → create an image block → upload.  
- **Replace:** in GitBook open a CR → find the image → three-dots → Replace image → upload.  
- **Remove:** in GitBook open a CR → find the image → delete the image block.

### Captions and alt text

- Every non-decorative image must have meaningful alt text. Decorative images: empty alt.  
- If the image's text is already in the body text → empty alt.  
- If the image contains functional text (e.g., buttons) → describe the function in alt.  
- If the image contains text NOT in the body → put that text in alt.  
- **Caption and alt text must not be the same.**

### Good practice

- Introduce each image with a full sentence describing it.  
- Show all options when capturing dropdowns.  
- Keep a consistent enhancement style.

## 12\. Using diagrams

### When to use

For: users and roles, Projects, integrations, processes (sequences of steps), UI maps, features.

### Types

- **Flow charts** — concepts, processes, hierarchies (users and roles, Group \> Org, Projects).  
- **Concept maps**, **sequence diagrams**, **decision trees**, **journey maps**.

### Best practices

- **Integrate diagrams with text.** Explain the diagram in the surrounding text. Generally, present the diagram first, then walk the user through it.  
- **Ensure legibility.**  
- **Well designed** — high-quality, appropriate colors, lines, arrows, shapes.

### Edward Tufte's four principles

1. **Graphical excellence** — the most ideas, in the shortest time, with the least ink, in the smallest space.  
2. **Visual integrity** — never distort the underlying data or create false interpretations.  
3. **Maximize the data-ink ratio** — remove unnecessary elements.  
4. **Aesthetic elegance** — simple, clean, clear depiction of data.

### Tools

Miro, draw.io (Flowchart Maker & Online Diagram Software), Microsoft Visio, Lucidchart, Gliffy Diagram.

## 13\. UX copy checklist

Apply this for every PR or design review.

**Core content**

- [ ] Scannable — most important info first.  
- [ ] Concise — within the 4-line description limit; nothing without value.  
- [ ] Jargon-free — plain language where possible.  
- [ ] Active voice — *Connect your repo*, not *The repo has been connected*.

**Formatting and style**

- [ ] Sentence case for titles and buttons (exceptions: product names and statuses).  
- [ ] No periods on titles, fragments, or buttons. Periods only for multi-sentence descriptions.  
- [ ] Buttons ≤ 3 words.  
- [ ] Placeholders show format examples, not labels.

**Context and action**

- [ ] Errors tell the user how to fix the problem.  
- [ ] Users know what happens after the primary CTA.  
- [ ] Feature names match what's used elsewhere in the Snyk UI.

**Accessibility and inclusivity**

- [ ] Descriptive link text (no *Learn more* or *Click here*).  
- [ ] Neutral pronouns (*they / their*) or 2nd person (*you / your*).

## 14\. Resolved conflicts and open questions

This section documents discrepancies between the source documents and how they were resolved.

| Topic | Conflict | Resolution |
| :---- | :---- | :---- |
| **fintech capitalization** | Grammarly CSV (April 2026): *Fintech*; Snyk terms PDF (May 2026): *fintech* | Use **fintech** (newer source wins). |
| **drop-down vs. dropdown** | Grammarly CSV row 47: *drop-down → dropdown*. Row 161: *drop down → drop-down* (for menu controls). | Use **dropdown** as the noun; reserve **drop-down** as an adjective only with *menu* or *list*. Verify with Veronica. |
| **IaC vs. IAC** | Snyk terms PDF: *IAC*. Common industry use and Grammarly CSV: *IaC*. | Verify Snyk house style. This guide uses **IaC** in running prose. |
| **1 MB vs. 1MB** | Grammarly CSV row 83: *1 MB → 1MB*. Most style guides use a space. | Follow Snyk Grammarly rule: **1MB** with no space. Verify before publishing externally. |
| **Internet capitalization** | Grammarly CSV row 151: *internet → Internet*; row 152: *Web → web*. Modern style guides lowercase both. | Per Grammarly CSV, **Internet** capitalized, **web** lowercase. Flag for review — AP changed *internet* to lowercase in 2016\. |
| **Snyk's → Snyk** | Grammarly CSV row 73: *Snyk's → Snyk* | Treat as a style preference: avoid possessive of the company name unless grammatically required. |
| **Capitalization rules doc and UX Copy doc overlap** | Both cover sentence-case usage. | Merged into Section 4\. Examples taken from the standalone Capitalization rules doc; UI-specific exceptions (ALL CAPS statuses, navigation headings) from the UX Copy doc. |

---

*This guide is the consolidated reference. Source documents (May 20, 2026 exports \+ April 27, 2026 Grammarly CSV) remain authoritative if anything here is ambiguous.*  
