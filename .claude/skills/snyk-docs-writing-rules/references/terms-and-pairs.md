# Terms, verb/noun pairs, compound words, UI elements

The full term reference for Snyk writing. Read this when you need to:

- Decide between a one-word and two-word form ("back up" vs "backup").
- Know which form is hyphenated.
- Find the canonical capitalization of a Snyk, partner, or security term.
- Pick the right UI-element verb or noun.

When this file is silent, fall back to MS style (see `ms-fallback.md`).

## Contents

1. Snyk-specific names
2. Snyk-specific terminology (critical distinctions)
3. Product and tool names
4. Concepts (lowercase unless brands)
5. Security terms and acronyms
6. Verb/noun pairs
7. UI-element terms (verbs and nouns)
8. Compound words: hyphenation
9. Words to avoid
10. Plural rules
11. "Allow," "enable," and "lets"

---

## 1. Snyk-specific names

| Term | Form |
|---|---|
| Snyk Projects, Snyk Project | Always capitalized (Snyk-defined entity, not generic "projects"). |
| Snyk Code, Snyk Open Source, Snyk Container, Snyk IaC | Capitalize all product names exactly. |
| Priority Score | Capitalized as a feature name. |
| Custom Rules | Capitalized as a product feature. |
| Organization, Group | Capitalize as Snyk-defined nouns. Prefer "company" over a generic "organization." |
| Cloud Native Application Security (CNAS) | Capitalized as the Snyk solution. Use the acronym after first use. |
| Vulnerability DB, Vulnerability Database | Snyk's database of vulnerabilities. Never "VulnDB." |
| Snyk pipe | Lowercase "pipe" — it's not a product. (Distinct from Bitbucket Pipes.) |

## 2. Snyk-specific terminology (critical distinctions)

- **issue vs vulnerability.** Use **vulnerability** for security problems. Use **issue** only for licensing problems, or a group of problems that includes a license problem. Never use "issue" for a security problem; never "vulnerability" for a license problem.
- **plan, not tier.** Free plan, Team plan, Business plan, Enterprise plan. Don't use "tier."
- **container, not Docker.** Docker is one engine among many (CRI-O, containerd). Don't use "Docker" as a synonym for "container."
- **container registries, not Docker registries.**
- **Git repository (or Git repo) for the repository; SCM integration for the integration.** Use "Git repo" / "Git repository" for the repository itself (and "hosted Git repo" for on-prem deployments of Git). Don't use "SCM" as a synonym for a repository. **Do** use "SCM integration" — not "Git integration" — for the integration that connects Snyk to a source code management system (GitHub, GitLab, Bitbucket, and so on).
- **SCA ≠ static code analysis.** SCA = software composition analysis. Static code analysis is the parent term of SAST. Don't abbreviate "static code analysis" to "SCA."
- **30-day trial.** Always hyphenated. Not "30 day trial."

## 3. Product and tool names (capitalize exactly)

### Language ecosystems and tools

| Name | Notes |
|---|---|
| .NET | Uppercase, leading period. |
| Composer | Capital C. |
| dep | All lowercase. |
| Go | Capitalized as "Go"; lowercase as "golang." |
| JavaScript | Capital J and S. **Don't abbreviate to "JS."** |
| Node.js | Capital N, lowercase ".js." |
| npm | Always lowercase. Rewrite to avoid starting a sentence with it. |
| pip | Always lowercase. |
| PyPI | Always `PyPI`. |
| RubyGems | Capital R and G, one word. |
| sbt | Always lowercase. |
| TypeScript | Capital T and S, one word. |
| Yarn (noun) / `yarn` (command) | Capitalized as a noun; lowercase in code. |

### Source hosts and platforms

| Name | Notes |
|---|---|
| Bitbucket | One word. Only the first B capitalized. (Not "BitBucket.") |
| GitHub | Capital G and H. |
| GitLab | Capital G and L. |
| Cloud Foundry | Two words. C and F capitalized. |
| OpenShift | One word. O and S capitalized. |

### Cloud providers

| Name | Notes |
|---|---|
| Amazon EC2, ECS, EKS, ECR | Keep the "Amazon" prefix — don't drop it, don't swap for "AWS." |
| AWS Fargate, IAM, KMS, Lambda, CodePipeline, CodeCommit, CodeBuild | Keep the "AWS" prefix — don't drop it, don't swap for "Amazon." |
| Google Cloud | Current name. Not "Google Cloud Platform" or "GCP" (renamed 2020). |
| Google Play Instant | Three words, all capitalized. |

### Container ecosystem

| Name | Notes |
|---|---|
| Docker | Capitalized. Don't use as a generic synonym for "container." |
| Docker Hub | Two words, both capitalized. |
| Dockerfile | One word. Capitalized. |
| Kubernetes | Full word, capitalized. Use "k8s" only where the audience expects it. |

## 4. Concepts (lowercase unless they're brands)

- agile (lowercase as a general adjective; "Agile" only as the named methodology)
- AI-BOM (Snyk-approved form; lowercase `aibom` only inside command names)
- cybersecurity (one word)
- data center (two words, no hyphen — not "datacenter")
- deep link (two words, lowercase)
- email (no hyphen)
- fintech (lowercase, except at the start of a sentence)
- genAI (lowercase "gen," capital "AI")
- infrastructure as code (lowercase; **IaC** is the acronym — not "IAC")
- knowledge base (two words, no hyphen)
- machine learning, artificial intelligence
- open source (noun; "open-source" as adjective)
- cloud native (noun; "cloud-native" as adjective)
- standalone (one word)
- taint analysis (two words)
- web (lowercase, except at the start of a sentence)
- web page (two words)
- web server (two words)
- website (one word)
- white paper (two words)

---

## 5. Security terms and acronyms

**First-use rule:** spell out an acronym only the first time it appears on a page, with the acronym in parentheses. After that, use only the acronym for the rest of the page — don't spell it out again.

| Spelled out | Acronym | Notes |
|---|---|---|
| static application security testing | SAST | |
| dynamic application security testing | DAST | |
| interactive application security testing | IAST | |
| software composition analysis | SCA | Not the same as static code analysis. |
| software bill of materials | SBOM | Never "SBoM." |
| infrastructure as code | IaC | Mixed-case acronym; lowercase the spelled-out form. |
| continuous integration/continuous delivery | CI/CD | Slash, no spaces (both in the acronym and spelled out). "Deployment" acceptable for customers/partners who use it. |
| cross-site scripting | XSS | |
| regular expression denial of service | ReDoS | |
| regular expression | regex | |
| same-origin policy | SOP | |
| man-in-the-middle | MITM | Hyphenated, lowercase. |
| software development lifecycle | SDLC | |
| Cloud Native Application Security | CNAS | Capitalize as a Snyk solution. |

Other acronyms (standard first-use): APK, OWASP Top 10, SOC 2 (space between "SOC" and "2"), URL, URI, YAML, Zip Slip (both words capitalized), PaaS (Platform as a Service).

### Specific term notes

- **intent** (Android): capitalize alongside "Android" ("Android Intents can be embedded"); lowercase otherwise.
- **Object-Graph Navigation Language**: capitalized and hyphenated.
- **merge request (MR)**: GitLab's term for a pull request. Lowercase except at the start of a sentence.
- **pull request (PR)**: lowercase except at the start of a sentence.
- **repository / repositories** (formal), **repo / repos** (informal): use as fits the tone.
- **Wi-Fi**: always hyphenated; both letters capitalized.

---

## 6. Verb/noun pairs

Two-word form = verb. One-word form = noun or adjective.

| Verb | Noun/Adjective | Example |
|---|---|---|
| back up | backup | "Back up your database. Restore from the backup if needed." |
| log in | login | "Log in to the Snyk Web UI using your login credentials." |
| set up | setup | "Set up your environment. The setup is fast." |
| log out | logout | Mirrors log in. |
| time out | timeout | "If the session times out, you see a timeout error." |
| check out | checkout | "Check out the branch. The checkout completed." |
| add on | add-on | "Add on the integration." Use "Add-on" capitalized only for a named product (Heroku Add-on). |

Note: prefer **log in / login** over "sign in / sign-in" (Snyk convention; see `decisions-log.md`).

---

## 7. UI-element terms (verbs and nouns)

Use the right column.

| Use this | Not this | Note |
|---|---|---|
| click / tap | click on / tap on | Drop the "on." |
| click (a button) | select (a button) | "Click" for buttons and links. |
| select / clear (a check box) | check / uncheck | Standard for check boxes. |
| press (a key) | hit / strike | |
| enter / type | key-in / type in | |
| run (a command) | execute | |
| start / turn on | boot up | |
| open / display | bring up | |
| turn on / turn off | switch on / shut off | |
| restart | re-start | One word. |
| double-click | double click / doubleclick | Hyphenated. |
| right-click / left-click | rightclick / leftclick | Hyphenated. |
| click | single-click / singleclick | |
| drag and drop | drag-and-drop | UI action. |
| dropdown | drop-down / drop down | One word, **noun and adjective**. |
| list | combo box | |
| dialog | dialog box | The container is a "dialog." |
| dialog / window | pop-up | Prefer "dialog" or "window." Use "pop-up" (hyphenated) only for a genuinely transient/unexpected popup. |
| option button | radio button | Use **radio button** — "option button" is dated. *(This row corrects the older guide: keep "radio button.")* |
| pane | blade | A sub-area of a window. |
| keyboard shortcut | hotkey | |
| stop / cancel / end | abort / terminate | |
| unavailable | grayed out / greyed out | |
| information | info | |
| OK (in UI) / okay (in prose) | ok | |
| yes or no | yes/no | |
| password | passcode | |
| homepage | home page | |
| scroll bar | scrollbar | Two words. |
| tool bar | toolbar | Two words. |
| onscreen | on-screen | |
| backend | back-end | |
| end user | enduser | |
| web page | webpage | Two words. |
| Click **Save** | Click the Save button | Don't repeat "button." |
| Open **Settings** | Open the Settings menu | Drop trailing "menu"/"option." |

### Folder vs Directory

- **Folder** in UI contexts: "Double-click the **My Project** folder."
- **Directory** in CLI/technical contexts: "Change to the `/lib` directory."

---

## 8. Compound words: hyphenation

Hyphenated as an adjective (before a noun); open or solid as a noun.

| Adjective (hyphenated) | Noun |
|---|---|
| client-side | client side |
| server-side | server side |
| cloud-native | cloud native |
| open-source | open source |
| real-time | real time |
| hard-coded | hard coded |
| built-in | built in |
| third-party | (adjective only) |
| step-by-step | (adjective only) |
| man-in-the-middle | (adjective only) |
| same-origin policy | (adjective only; "policy" is the noun) |

### Always one word

codebase, cybersecurity, Dockerfile, email, lifecycle, runtime, standalone, username, webhook, website, dropdown, allowlist, blocklist, homepage, backend, onscreen.

### Always two words

cheat sheet, data center, deep link, Docker Hub, knowledge base, pull request, web server, web page, white paper, scroll bar, tool bar, end user, taint analysis.

### Always hyphenated (any position)

30-day trial, man-in-the-middle (MITM), step-by-step, Object-Graph Navigation Language, Wi-Fi, double-click, right-click, left-click.

### Never hyphenate

Adverbs ending in -ly + adjective: "fully managed service," not "fully-managed service."

---

## 9. Words to avoid (use the Snyk-preferred alternative)

| Don't use | Use instead |
|---|---|
| utilize / utilization / usage | use |
| commence / commencement | start |
| prior to, in advance of | before |
| in the event that / of, as long as | if |
| make sure | ensure |
| first of all | first |
| and/or | and (or rewrite) |
| via | through, using |
| e.g. | for example |
| i.e. | that is |
| etc. | and so on |
| N.B. | note |
| in order to | to |
| within | in |
| due to (the fact that) | because |
| since (for cause) | because |
| with regard to | about |
| with the exception of | except |
| on behalf of | for |
| as well as | and |
| is able to / has the ability to | can |
| is required to | must |
| you need to | you must |
| it is recommended that | Snyk recommends |
| this functionality enables users to | you can |
| a lot | many |
| at this time | now |
| reach out | contact |
| go ahead | continue |
| seek out | find |
| return back / revert back / cancel out | return / revert / cancel |
| a total of | total |
| simply, easy, fast, just, actually, literally, currently | (cut entirely) |
| please | (cut, unless inconveniencing the user) |
| once (to mean "after") | after |
| click here | (rewrite the link into the sentence) |
| see (a page) | visit |
| above / below | earlier / later, preceding / following |
| go to | navigate to |
| chairman / salesman / manpower / mankind | chairperson / salesperson / effort / humanity |
| the disabled | people with disabilities |
| crazy / insane | many, a lot, astounding |
| master / slave | leader / follower |
| master | main, controller |
| postmortem | retrospective, incident retro |
| e-mail | email |
| SCM (as a synonym for a repository) | Git repository (or Git repo) |
| Git integration | SCM integration |
| tier (for plans) | plan |
| Docker (as generic) | container |
| Docker registries (as generic) | container registries |
| issue (for security) | vulnerability |
| vulnerability (for license) | issue |
| JS | JavaScript |
| GCP, Google Cloud Platform | Google Cloud |
| VulnDB | Vulnerability DB / Vulnerability Database |
| whitelist | allowlist |
| blacklist | blocklist |
| denylist | blocklist (Snyk style is "blocklist," not "denylist") |
| enable (for human capability) | "you can…" or imperative — see section 11 |

## 10. Plural rules

- Don't write "repository(s)." Write "one or more repositories."
- Plural of abbreviations: "APIs," "URLs," "PRs" (no apostrophe).
- Plural of decades: "1990s" (no apostrophe).

## 11. "Allow," "enable," and "lets" — verb choice for capability

- **allow** = give permission. ("This setting allows requests from approved domains.")
- **enable** = activate a feature. ("Enable two-factor authentication.") **Do not** use "enable" for what software lets a user do ("enables users to scan…"). Rewrite instead.
- **lets** = an acceptable casual rewrite of "enables users to." ("Snyk lets developers fix vulnerabilities in the IDE.")
- Prefer **"you can…"** or imperatives where they work: "Scan dependencies from the CLI" beats "Snyk lets you scan dependencies from the CLI."

## When in doubt

If this file and MS are both silent, default to: (1) the one-word form for nouns listed in Merriam-Webster; (2) the hyphenated form for adjectives before a noun; (3) the open form for noun phrases.
