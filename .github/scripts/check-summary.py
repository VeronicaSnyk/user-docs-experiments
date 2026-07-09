#!/usr/bin/env python3
"""
check-summary.py — Validate SUMMARY.md consistency with docs/ file structure.

Checks:
  1. Every file referenced in SUMMARY.md exists on disk.
  2. Every .md file in docs/ (excluding .gitbook/includes/) is listed in SUMMARY.md.

Exits non-zero if any inconsistency is found.

Usage:
    python3 .github/scripts/check-summary.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
DOCS_ROOT = REPO_ROOT / "docs"
SUMMARY_FILE = DOCS_ROOT / "SUMMARY.md"

# Patterns to exclude from the "all files must be in SUMMARY" check
# (substring match against the path relative to docs/)
EXCLUDE_PATTERNS = [
    ".gitbook/includes/",   # reusable snippets — intentionally excluded from TOC
    ".gitbook/assets/",     # images
    "SUMMARY.md",           # itself
]

# Paths (relative to docs/) excluded by exact match only — nested variants stay in scope
EXCLUDE_EXACT = {
    "README.md",            # root readme listed separately; section READMEs are checked
}

LINK_RE = re.compile(r'\[.*?\]\(([^)]+)\)')


def extract_summary_paths(summary_file: Path) -> list[tuple[int, str]]:
    """Return list of (line_num, relative_path) tuples from SUMMARY.md links."""
    paths = []
    content = summary_file.read_text(encoding="utf-8")
    for line_num, line in enumerate(content.splitlines(), 1):
        for match in LINK_RE.finditer(line):
            raw = match.group(1).split("#")[0].strip()
            if raw and not raw.startswith("http"):
                paths.append((line_num, raw))
    return paths


def get_all_doc_files(docs_root: Path) -> set[Path]:
    """Return all .md files under docs/, excluding excluded patterns."""
    all_files = set()
    for f in docs_root.rglob("*.md"):
        rel = f.relative_to(docs_root)
        rel_str = str(rel)
        if rel_str in EXCLUDE_EXACT:
            continue
        if not any(excl in rel_str for excl in EXCLUDE_PATTERNS):
            all_files.add(rel)
    return all_files


def main():
    if not SUMMARY_FILE.exists():
        print(f"ERROR: SUMMARY.md not found at {SUMMARY_FILE}", file=sys.stderr)
        sys.exit(1)

    summary_refs = extract_summary_paths(SUMMARY_FILE)
    all_doc_files = get_all_doc_files(DOCS_ROOT)

    missing_from_disk: list[tuple[int, str]] = []
    referenced_paths: set[Path] = set()

    for line_num, raw_path in summary_refs:
        resolved = (DOCS_ROOT / raw_path).resolve()
        rel = Path(raw_path)
        referenced_paths.add(rel)
        if not resolved.exists():
            missing_from_disk.append((line_num, raw_path))

    # Files on disk but not in SUMMARY.md
    unreferenced = all_doc_files - referenced_paths

    errors = False

    if missing_from_disk:
        errors = True
        print(f"\n❌ SUMMARY.md references {len(missing_from_disk)} file(s) that do not exist:\n")
        for line_num, path in sorted(missing_from_disk, key=lambda x: x[0]):
            print(f"  SUMMARY.md:{line_num}  →  {path}")

    if unreferenced:
        errors = True
        print(f"\n⚠️  {len(unreferenced)} file(s) exist in docs/ but are NOT in SUMMARY.md:\n")
        for path in sorted(unreferenced):
            print(f"  docs/{path}")
        print("\n  Add these files to SUMMARY.md or move them to .gitbook/includes/ if they are reusable snippets.")

    if not errors:
        print(f"✅ SUMMARY.md is consistent with docs/ ({len(referenced_paths)} files referenced, "
              f"{len(all_doc_files)} files on disk).")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
