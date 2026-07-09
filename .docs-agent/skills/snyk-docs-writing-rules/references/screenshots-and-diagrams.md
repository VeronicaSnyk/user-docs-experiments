# Screenshots and diagrams

Read this when adding screenshots or diagrams to Snyk documentation.

(In-product UX copy — error messages, notifications, placeholders, confirmation dialogs — is covered by the separate `ux-copy` skill, not here.)

## Contents

1. Using screenshots
2. Using diagrams

---

## 1. Using screenshots

**Policy:** prioritize clear text over screenshots. Use screenshots only for complicated processes or to clarify ambiguities.

### When to use

- Multi-step processes where the screenshot removes ambiguity or guides the reader.
- UI changes that need visual explanation (a button moved to a non-obvious place).
- Interaction patterns that are not intuitive.
- Changelog entries showcasing updates.

If a feature *needs* a screenshot to be usable, consider whether the UI itself should improve — flag it to Product Design.

### When NOT to use

- The screenshot adds no informational value (decorative).
- The audience prefers another format (technical users prefer code samples over UI images).
- The user can complete the workflow from text alone.
- What's shown is obvious (a search bar, a common icon).

### Audience-based guidance

| Audience | Example doc | Guidance |
|---|---|---|
| Customer workflows (manage risk) | docs.snyk.io/manage-risk | Use sensibly for UI-based work |
| Customer workflows (enterprise setup) | docs.snyk.io/enterprise-setup | Use to illustrate concepts or key functions |
| Customer workflows (CLI) | docs.snyk.io/snyk-cli | Prefer code samples, commands, config examples |
| IDE | docs.snyk.io/integrate-with-snyk/use-snyk-in-your-ide | Use rarely or never unless essential |

### How to capture

- Light mode/theme only.
- Zoom in (~150%). Capture the relevant area, not the whole screen.
- No annotations or overlays (no arrows, borders, frames, callouts). Direct attention through cropping and zoom.
- Hide sensitive data — no account IDs, tokens, passwords, customer/user names, real emails. Prefer demo environments; otherwise crop or use the browser Inspect tool. If using Snagit blur, use intensity 12.5, but note some tools can unblur — redact robustly.
- Crop to content while keeping enough context.
- No effects (shadows, borders). Transparent background.

### Filename convention

`location-in-ui-feature-or-element-description.png`

- Lowercase only; words separated by dashes; include the UI location and a brief description.
- Examples: `org-settings-iac-detect-config-files-enabled.png`, `org-level-member-group-member-details.png`.

### Storage and lifecycle

- Source of truth: the docs platform's (GitBook) image library. Don't keep copies in Google Drive.
- **Add:** capture → edit → save with naming convention → in GitBook open a CR → create an image block → upload.
- **Replace:** in GitBook open a CR → find the image → three-dots → Replace image → upload.
- **Remove:** in GitBook open a CR → find the image → delete the image block.

### Captions and alt text

- Every non-decorative image needs meaningful alt text. Decorative images: empty alt.
- If the image's text is already in the body → empty alt.
- If the image contains functional text (e.g., buttons) → describe the function in alt.
- If the image contains text not in the body → put that text in alt.
- Caption and alt text must not be the same.

### Good practice

- Introduce each image with a full sentence describing it.
- Show all options when capturing dropdowns.
- Keep a consistent enhancement style.

---

## 2. Using diagrams

### When to use

For users and roles, Projects, integrations, processes (sequences of steps), UI maps, and features.

### Types

- **Flow charts** — concepts, processes, hierarchies (users and roles, Group > Org, Projects).
- Concept maps, sequence diagrams, decision trees, journey maps.

### Best practices

- Integrate diagrams with text. Generally present the diagram first, then walk the user through it.
- Ensure legibility.
- Well designed — high-quality, appropriate colors, lines, arrows, shapes.

### Edward Tufte's four principles

1. **Graphical excellence** — the most ideas, in the shortest time, with the least ink, in the smallest space.
2. **Visual integrity** — never distort the data or create false interpretations.
3. **Maximize the data-ink ratio** — remove unnecessary elements.
4. **Aesthetic elegance** — simple, clean, clear.

### Tools

Miro, draw.io, Microsoft Visio, Lucidchart, Gliffy Diagram.
