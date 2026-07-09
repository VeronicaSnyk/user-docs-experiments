---
name: check-broken-links
description: Systematically check documentation for missing and broken links across any path in the repo. Use when you need to identify text references without actual links, broken internal links, or links needing updating (for example after a migration or a large edit).
license: Proprietary
metadata:
  author: edmond.sabou
  version: "1.1.0"
  category: quality-assurance
---

# Check Broken and Missing Links

## Purpose

Identify:
- Text references to documentation without actual links
- Broken internal links pointing to non-existent files
- Links that may need updating (for example after a migration or bulk edit)

## When to Use

Run this skill over any part of the docs you want to validate — a whole section, a
subsection, or the specific pages you just changed — to ensure all cross-references are
properly linked before opening a PR.

## Target path

Every command below takes a **`<TARGET_PATH>`** — the directory (or single file) to check.
Set it to whatever you want to validate. Examples in user-docs:

- A whole section: `scan-fix-and-prevent/`
- A subsection: `scan-fix-and-prevent/scan-with-snyk/snyk-container/`
- The page(s) you just added (pass the file directly)

```bash
TARGET_PATH="scan-fix-and-prevent/scan-with-snyk/snyk-container/"   # ← set this
```

## Workflow

### 1. Find Missing Links

Search for text patterns that suggest a link should exist but is missing:

```bash
grep -rn "see the .* documentation" "$TARGET_PATH" -i --include="*.md"
grep -rn "visit the.*documentation" "$TARGET_PATH" -i --include="*.md"
grep -rn "refer to the" "$TARGET_PATH" -i --include="*.md"
grep -rn "for more information.*see" "$TARGET_PATH" -i --include="*.md"
```

### 2. Check Broken Internal Links

Extract all markdown links and verify they point to existing files:

```bash
# List every .md link target under the path
grep -roh '\[.*\]([^)]*\.md[^)]*)' "$TARGET_PATH" --include="*.md" | \
  sed 's/\[.*\](\(.*\))/\1/' | sort -u
```

For each link found:
1. Resolve relative paths from the source file's location
2. Check whether the target file exists
3. Report broken links with source file and line number

### 3. Check External References

Look for external URLs that should be internal Snyk docs links (adjust the domain(s) to
what you're auditing — e.g. a legacy vendor domain being migrated in, or `docs.snyk.io`
links that should be relative):

```bash
EXTERNAL_DOMAIN="example.com"   # ← the domain you're auditing
grep -rn "$EXTERNAL_DOMAIN" "$TARGET_PATH" --include="*.md"
```

### 4. Generate Report

Create a structured report with:

**Missing Links:**
- File path and line number
- Text suggesting a link should exist
- Suggested link target (if determinable)

**Broken Links:**
- Source file path and line number
- Link text
- Target path that doesn't exist
- Suggested fix (if available)

**External References:**
- File path and line number
- External URL
- Whether it should be converted to an internal link

## Example Output Format

```markdown
# Link Check Report

## Missing Links (N found)

### scan-fix-and-prevent/scan-with-snyk/snyk-container/example-page.md:62
Text: "For more information about permissions, see the permissions documentation."
Suggestion: Add link to the permissions page when available

## Broken Links (N found)

### scan-fix-and-prevent/scan-with-snyk/snyk-container/getting-started.md:28
Link: [Configure authentication](../configure/configure-authentication.md)
Error: File does not exist
Suggestion: Update to the correct relative path

## External References (N found)

### scan-fix-and-prevent/scan-with-snyk/snyk-container/example-page.md:15
URL: https://example.com/en/articles/12345-some-article
Action: Review whether this should remain external or be converted to an internal link
```

## Usage Notes

- Run this check before creating final PRs
- Some "missing links" may be intentional prose — review each case
- Broken links may indicate pages not yet created or incorrect relative paths
- Generate the report and review it with the user before fixing all issues
