# Claude Code Workshop — 1-Hour Hands-On Training

**Audience:** Non-technical or lightly technical users (PMs, writers, analysts) with basic terminal familiarity  
**Duration:** 60 minutes  
**Format:** Guided, hands-on — participants follow along in real time

---

## What you will be able to do after this workshop

- Install Claude Code on your machine
- Start a Claude Code session in the terminal
- Connect Claude to a real codebase (a fork of `snyk/user-docs`)
- Ask Claude questions about code and docs
- Use Claude Code inside VS Code

---

## Before the session — ask participants to do this in advance

Send this checklist before the workshop. It saves 10–15 minutes of setup time during the session.

- [ ] Check your Node.js version: open a terminal and run `node --version`. You need version 18 or newer.  
  - If you don't have Node.js or it's too old, download it from [nodejs.org](https://nodejs.org) — install the **LTS** version.
- [ ] Create a GitHub account if you don't have one: [github.com](https://github.com)
- [ ] Have VS Code installed: [code.visualstudio.com](https://code.visualstudio.com)
- [ ] Have a Claude Pro, Team, or Enterprise subscription (needed for authentication)

---

## Agenda

| Time | Section |
|------|---------|
| 0:00–0:10 | What is Claude Code and why it matters for your work |
| 0:10–0:25 | Install Claude Code and authenticate |
| 0:25–0:40 | Fork the repo and start your first session |
| 0:40–0:50 | Use Claude Code inside VS Code |
| 0:50–0:55 | Customize Claude with CLAUDE.md and the Snyk style guide |
| 0:55–1:00 | Hands-on practice + Q&A |

> **Timing note:** Sections 5 and 6 share the last 10 minutes. If you are running on time, do the CLAUDE.md demo live (5 min) then open for questions. If you are short on time, assign CLAUDE.md as a follow-up exercise and use the full 10 minutes for Q&A.

---

## Section 1 — What is Claude Code? (10 min)

**Facilitator talking points (no hands-on yet):**

Claude Code is a command-line tool that lets you work with Claude directly in your terminal, connected to real files on your computer. Unlike the web chat, it can:

- Read, write, and edit files in your project
- Understand an entire codebase, not just a snippet you paste in
- Run Git operations (create branches, commit changes)
- Work inside VS Code as an integrated panel

**Why this matters for non-engineers:**

- You can ask "what does this service actually do?" and get a real answer from the code
- You can analyze files and docs in bulk — no more copy-paste into a chat window
- You can generate drafts, specs, and changelogs grounded in what actually exists in the repo
- You can onboard to a new project by asking Claude to walk you through it

**Key mental model:** Claude Code is Claude + your local files. The terminal is how you open the door.

---

## Section 2 — Install Claude Code and authenticate (15 min)

### Step 1 — Verify Node.js

Open your terminal (Mac: press `Cmd + Space`, type "Terminal", press Enter).

Run:
```
node --version
```

You should see something like `v20.11.0`. If the number is below 18, or the command is not found, install Node.js LTS from [nodejs.org](https://nodejs.org) first.

---

### Step 2 — Install Claude Code

**Option A — if you have npm (most people):**

Run this in your terminal:
```
npm install -g @anthropic-ai/claude-code
```

Wait for it to finish. You will see a progress bar and some output. This is normal.

**Option B — if npm install fails or you don't have npm:**

Follow the curl-based instructions at [code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview).

---

### Step 3 — Verify the install

Run:
```
claude --version
```

You should see a version number. If you get "command not found," try closing and reopening your terminal, then run it again.

---

### Step 4 — Log in

Run:
```
claude
```

The first time you run this, Claude Code opens a browser window asking you to log in with your Anthropic/Claude account. Log in, grant access, and return to the terminal.

You should see the Claude Code interactive prompt (`>`). You are now authenticated.

Type `/exit` to close it for now.

**If the browser window doesn't open automatically**, run this command manually:
```
claude /login
```

This forces the authentication flow. Follow the prompts in the terminal — it will give you a URL to open in your browser if the automatic redirect fails.

---

## Section 3 — Fork the repo and run your first session (15 min)

We will use the `snyk/user-docs` repository as our practice codebase. Forking it means you get your own safe copy to experiment with — nothing you do affects the real docs.

### Step 1 — Fork the repository

1. Go to [github.com/snyk/user-docs](https://github.com/snyk/user-docs)
2. Click the **Fork** button in the top-right corner
3. Leave all settings as default and click **Create fork**
4. GitHub creates a copy under your own account: `github.com/YOUR-USERNAME/user-docs`

---

### Step 2 — Clone your fork to your computer

In your terminal, navigate to where you want to keep the project. For example, your Desktop:

```
cd ~/Desktop
```

Then clone your fork (replace `YOUR-USERNAME` with your actual GitHub username):

```
git clone https://github.com/YOUR-USERNAME/user-docs.git
```

Wait for it to finish. A new folder called `user-docs` appears on your Desktop.

---

### Step 3 — Navigate into the project

```
cd user-docs
```

---

### Step 4 — Start Claude Code

```
claude
```

You are now inside a Claude Code session connected to the `user-docs` repository. Claude can see every file in this folder.

---

### Step 5 — Try these prompts

Type each of these at the `>` prompt and press Enter. Watch how Claude responds.

**Understand the project:**
```
What is this repository? Give me a one-paragraph summary.
```

**Explore the structure:**
```
What are the main sections of the documentation and where do they live in the folder structure?
```

**Ask a content question:**
```
Does this repo have any documentation about Snyk Broker? Where is it?
```

**Ask about a specific file:**
```
Summarize the file docs/scan-with-snyk/overview.md in three bullet points.
```

**One-shot queries (no interactive session needed):**

You don't always need to open an interactive session. You can pass a question directly on the command line and get an answer immediately:

```
claude "what does this repository do?"
```

```
claude "list all the files in docs/snyk-api/ and describe what each one covers"
```

This is useful for quick lookups. Claude answers and returns you to your normal terminal — no session to manage.

**Give Claude more context with drag-and-drop:**

You can drag any file from your file manager (Finder on Mac, Explorer on Windows) directly into the terminal window. This pastes the file path into your prompt, so Claude knows exactly which file you mean.

Try it:
1. Open a new line at the `>` prompt and start typing: `Summarize this file for me:`
2. Drag a markdown file from your `user-docs` folder into the terminal
3. Press Enter

Claude reads that specific file and responds. This works for any file type — markdown, JSON, CSV, code files, and so on.

**Useful slash commands to know:**
- `/help` — see all available commands
- `/clear` — clear the conversation history and start fresh
- `/compact` — compress long conversations to save tokens (use this when responses slow down)
- `/exit` — close the session

---

## Section 4 — Use Claude Code inside VS Code (10 min)

Claude Code works inside VS Code so you can chat with Claude and see your files side by side.

### Step 1 — Open the project in VS Code

In your terminal (while inside the `user-docs` folder), run:
```
code .
```

VS Code opens with the `user-docs` project loaded.

### Step 2 — Open the integrated terminal

In VS Code: press `` Ctrl + ` `` (backtick) on Windows/Linux, or `` Cmd + ` `` on Mac.

A terminal panel opens at the bottom of VS Code. This is a full terminal — you can run Claude Code here.

### Step 3 — Start Claude Code in the VS Code terminal

In the VS Code terminal, run:
```
claude
```

Claude Code now runs inside VS Code. When Claude edits a file, VS Code shows you a live diff — highlighted in green (additions) and red (deletions) — so you can see exactly what changed.

### Step 4 — Try an edit (safe — you are in your fork)

At the Claude prompt, try:
```
Look at docs/scan-with-snyk/overview.md and suggest one small improvement to the opening paragraph. Show me the change but don't apply it yet.
```

Claude will show you a proposed change. You can then type `yes` or `apply it` to accept, or describe a different approach.

### Step 5 — Paste an image for visual analysis

Claude Code can read images you paste directly into the terminal. This is useful for sharing screenshots of UIs, diagrams, or error messages.

**How to paste an image:**
1. Take a screenshot (Mac: `Cmd + Shift + 4`, then drag to select)
2. The screenshot is copied to your clipboard
3. In the Claude Code prompt, press `Ctrl + V` to paste it
4. Add your question, for example: `What does this UI show? Is there anything confusing about it?`
5. Press Enter

Claude analyzes the image and responds. This works with any image in your clipboard — screenshots, photos, diagrams copied from a browser, and so on.

> **Note:** Image paste works in the terminal and in the VS Code integrated terminal. It does not work if you are on a remote SSH connection.

---

## Section 5 — Customize Claude with CLAUDE.md and the Snyk style guide (bonus, or replace Q&A)

This is the highest-value thing you can do after setup. A `CLAUDE.md` file sits in your project folder and loads automatically every time you start a Claude Code session in that project. Think of it as a briefing document Claude reads before you say a word.

Without it: you re-explain context every session.  
With it: Claude already knows your project, your team's conventions, and how you want it to write.

---

### What to put in a CLAUDE.md

A good `CLAUDE.md` for a docs or PM workflow covers three things:

1. **Project context** — what this repo is, who uses it, what it does
2. **Writing rules** — how Claude should write and edit content
3. **Conventions** — terminology, formatting, things to avoid

---

### Step 1 — Create a CLAUDE.md in your fork

In your terminal, make sure you are inside the `user-docs` folder:

```
cd ~/Desktop/user-docs
```

Open a new file in VS Code:

```
code CLAUDE.md
```

---

### Step 2 — Add the Snyk style guide as Claude's default context

Paste the following into your `CLAUDE.md`. This gives Claude the Snyk writing rules as standing instructions for every session — so it writes and edits in your voice by default, without you having to ask.

```markdown
# Project context

This is the Snyk user documentation repository. Content is written for developers,
security engineers, and DevSecOps practitioners. It is published at docs.snyk.io
via GitBook. All content lives under docs/.

---

# Writing rules — apply to all content you write or edit

## Voice and tense
- Use active voice. The subject does the action.
- Write in present tense. Avoid "will be."
- Use second person ("you") or imperatives. Avoid "I."
- Avoid modal verbs (should, may, might) — they add uncertainty.

## Words to avoid
- Filler: "just," "actually," "literally," "very," "really," "simply," "currently"
- Redundant: "please," "first of all," "in order to," "make sure," "once" (use "after")
- Latin: use "for example" not "e.g."; "that is" not "i.e."; "and so on" not "etc."; "through/using" not "via"
- AI buzzwords: "synergy," "leveraging," "seamless," "cutting-edge," "in the ever-evolving landscape"
- Brand possessives: not "Snyk's" — rewrite to avoid

## Capitalization
- Always capitalize: Projects, Groups, Organizations, Snyk Code, Snyk Open Source, Snyk Web UI
- Correct: Node.js, .NET, npm, GitLab, GitHub, CI/CD, DevOps, DevSecOps, AI-BOM
- Correct compound forms: webhook, codebase, lifecycle, runtime, dropdown, username, standalone

## Numbers
- Spell out one through nine; use numerals for 10 and above
- Use commas as thousands separators: 1,000 not 1000

## Lists
- Bulleted for unordered items; numbered for step-by-step procedures
- Use imperative mood in steps: "Click Save" not "You should click Save"
- Parallel construction: if one item starts with a verb, all items start with a verb

## UI documentation
- Bold UI elements: Click **Save**
- Navigation: "Navigate to **Settings** > **Notifications**"
- Links: embed organically, never use "click here"

## Inclusive language
- Gender-neutral pronouns: they/them
- allowlist / denylist (not whitelist / blacklist) unless the software uses those exact terms
- No directional cues as the only locator ("above," "below," "left")

---

# Content structure

- All docs live under docs/
- Reusable snippets are in .gitbook/includes/
- GitBook config is in docs/.gitbook.yaml and docs/SUMMARY.md

---

# What to do when asked to edit or write content

1. Read the existing file before suggesting any changes.
2. Apply the writing rules above automatically — do not wait to be asked.
3. Preserve existing structure and heading levels unless asked to change them.
4. If you are unsure about Snyk-specific terminology, ask before changing it.
5. Do not add emojis, marketing language, or superlatives.
```

---

### Step 3 — Save the file and start a new session

Save `CLAUDE.md`, then start a new Claude Code session:

```
claude
```

Claude now loads your `CLAUDE.md` automatically at the start of every session. You will see it acknowledged in the startup output.

---

### Step 4 — Test it

Try asking Claude to edit a file without giving any style instructions:

```
Edit the opening paragraph of docs/scan-with-snyk/overview.md to be clearer and more direct.
```

Claude applies the Snyk writing rules — active voice, no filler words, correct capitalization — without you having to ask. Compare the output to what you got before you added the `CLAUDE.md`.

---

### How to keep CLAUDE.md useful over time

- Add new rules as you catch patterns Claude gets wrong
- Add team-specific terminology: product names, internal tool names, things Claude should never rename
- Add links to internal resources Claude should reference ("our PRD template is at docs/templates/prd.md")
- Keep it under ~200 lines — very long `CLAUDE.md` files slow Claude down and dilute the important rules

---

## Section 6 — Hands-on practice + Q&A (10 min)

Give participants 5–7 minutes to try one or two of these on their own, then open for questions.

### Practice prompts (choose one)

**For writers/docs people:**
```
Find all markdown files in docs/snyk-api/ and list their titles (the first H1 heading in each file).
```

```
Read docs/discover-snyk/getting-started/glossary.md and tell me if any definitions seem outdated or missing.
```

**For PMs:**
```
Read the SUMMARY.md file and tell me which top-level sections exist and how many pages each section contains.
```

```
Is there a changelog or release notes file in this repo? If yes, summarize the three most recent entries.
```

**For everyone:**
```
What is a CLAUDE.md file and why would I add one to my project?
```

---

## Quick reference card — share with participants after the session

```
INSTALL
npm install -g @anthropic-ai/claude-code

START A SESSION
cd your-project-folder
claude

KEY COMMANDS
/help        see all commands
/clear       clear conversation
/compact     compress history (saves tokens)
/exit        close session

QUICK TASKS
claude "summarize this project"
claude "what does this file do?" (then drag a file in)

IN VS CODE
Open integrated terminal (Cmd/Ctrl + `)
Run: claude
Live diffs appear when Claude edits files

FORK WORKFLOW (safe practice)
1. Fork snyk/user-docs on GitHub
2. git clone https://github.com/YOUR-USERNAME/user-docs.git
3. cd user-docs
4. claude

CLAUDE.MD — customize Claude for your project
Create a CLAUDE.md file in your project root.
Claude reads it automatically at the start of every session.
Use it to set writing rules, project context, and terminology.
Keep it under ~200 lines.
```

---

## Tips for facilitators

- **If npm install fails:** The most common cause is Node.js being too old. Run `node --version` first.
- **If authentication doesn't open a browser:** Try running `claude /login` manually.
- **If Claude seems slow:** Use `/compact` to compress the conversation history.
- **If someone doesn't have a Claude subscription:** They can observe for now — the install still works, authentication just won't complete until they have an account.
- **Pace check:** If you are running behind, skip Section 4 (VS Code) and do it as a follow-up.
- **CLAUDE.md demo:** The most impactful thing to demo live is the before/after — run a prompt without CLAUDE.md, then add it and run the same prompt again. The difference in output quality makes the value immediately obvious.
