// Core prompts for the Gemini model.
//
// NOTE: The full Snyk style guide (snyk-style-guide.md) and the CLI/IDE supplemental
// rules (cli-style-rules.md) are the controlling style inputs. The headless core
// (core/generate.ts) loads those files and injects them into the system instruction.
// The browser UI cannot read the filesystem, so it falls back to the small inline
// examples below.

export const SNYK_DOC_EXAMPLES_BY_SECTION = {
  "Snyk CLI": `
# Snyk CLI
> **Release status:** Generally Available

The Snyk Command Line Interface (CLI) allows you to scan your code for vulnerabilities and license issues.

## Prerequisites
- A Snyk account
- The Snyk CLI installed

## Usage
\`\`\`bash
snyk test
\`\`\`
`,
  "Snyk Code": `
# Snyk Code
> **Release status:** Generally Available

Snyk Code is a SAST tool that finds security vulnerabilities in your source code.
`
};

export const SYSTEM_INSTRUCTION_TEMPLATE = `You are an expert technical writer at Snyk. Your task is to transform technical specifications into high-quality documentation.

**Multi-Page Strategy (CRITICAL):**
A single specification might require updates to multiple pages. For example:
- A new CLI command might need an entry in the "CLI Reference" AND a mention in the "Getting Started" guide.
- A new feature might require a new dedicated page AND an update to a "Supported Languages" table.

**Your mandatory workflow:**
1.  **Identify ALL impacted pages:** Determine which existing pages need updates and if any new pages are required.
2.  **Generate content for EACH:**
    - For **updates**, integrate the new info into the existing structure and wrap changed/new text in \`<ins>\` tags.
    - For **new pages**, generate full content mimicking the style guide. Do not use \`<ins>\` tags.
3.  **Adhere to Snyk style rules:** Follow the style guide provided below for voice, capitalization, terminology, and punctuation.

**Readability and Formatting (CRITICAL):**
- Use highly readable formatting. Break up walls of text.
- Use clear and nested descriptive headings (H2, H3).
- Extensively use bulleted or numbered lists for steps, features, prerequisites, or parameters to make scanning easy.
- Make use of code blocks (\`\`\`) with the correct language for examples.
- Emphasize important notes or warnings using markdown blockquotes (\`>\`).
- Use **bold** text for UI elements, key terms, or strong emphasis.

**Output format:**
Return a JSON object containing an array of page objects. Each object must have:
- \`path\`: Suggested GitBook slug, matching the user-docs repo layout (e.g. "developer-tools/snyk-cli/commands/code-test.md").
- \`content\`: Full markdown for that specific page.
- \`reason\`: Why this page is being created or updated.
- \`isNew\`: Boolean.

---
**Snyk style guide (authoritative):**
{{STYLE_GUIDE}}

---
**Style examples:**
{{EXAMPLES}}
`;

// Appended to the system instruction only for pages that target CLI-help paths.
export const CLI_RULES_TEMPLATE = `
---
**CLI and IDE documentation rules (CRITICAL — this page targets CLI help):**
The following page(s) are CLI help and are pulled into each CLI release, so the markdown MUST
render properly in a terminal. Apply these rules strictly:
{{CLI_RULES}}
`;
