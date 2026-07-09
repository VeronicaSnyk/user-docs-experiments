#!/usr/bin/env python3
"""
rename_assets.py — Rename generic image files in docs/.gitbook/assets/ to
meaningful descriptive slugs derived from their markdown context.

Usage:
    python3 _planning/rename_assets.py [--dry-run]

Options:
    --dry-run   Print planned renames without making changes.
"""

import os
import re
import sys
import glob
import unicodedata
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "docs" / ".gitbook" / "assets"
DOCS_DIR = REPO_ROOT / "docs"

MAX_SLUG_LEN = 60

# Patterns that identify a generic (meaningless) filename stem.
GENERIC_PATTERNS = [
    # image (N), image (N) (M), image (N) (M) (P) ..., image2, image3, image.png
    re.compile(r'^image(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*(\s*\(\d+\))*\d*$', re.IGNORECASE),
    # Screenshot YYYY-MM-DD ..., Screenshot YYYY-MM-DD at ...
    re.compile(r'^screenshot[\s_]\d{4}', re.IGNORECASE),
    # screen_shot_...
    re.compile(r'^screen.?shot', re.IGNORECASE),
    # Bare numbers: 1.png, 2.png, 10.png, 1 (1).png, 2 (3) (1).png
    re.compile(r'^\d+(\s*\(\d+\))*$'),
    # unknown (N)
    re.compile(r'^unknown(\s*\(\d+\))*$', re.IGNORECASE),
    # untitled, untitled-N-, untitled (N)
    re.compile(r'^untitled[\s\-\(]*\d*[\)\-]*$', re.IGNORECASE),
    # mceclip0, mceclip1, mceclip0-10-, mceclip1-9-
    re.compile(r'^mceclip\d+', re.IGNORECASE),
    # Date-only filenames: 2023-08-15_16-36-28, 2024-02-13_10-17-49
    re.compile(r'^\d{4}-\d{2}-\d{2}[_\-]\d{2}[-_]\d{2}[-_]\d{2}', re.IGNORECASE),
    # Date filenames like 2024-12-06-Ts-VS-Code-ext-obt-more-fin-
    re.compile(r'^\d{4}-\d{2}-\d{2}-', re.IGNORECASE),
]

# Words that are too generic to be the sole content of a slug
BANNED_SOLE_CONTENT = {'image', 'screenshot', 'figure', 'img', 'photo', 'pic', 'picture', 'unknown', 'untitled'}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_generic(stem: str) -> bool:
    """Return True if the filename stem matches a generic naming pattern."""
    stem_stripped = stem.strip()
    for pat in GENERIC_PATTERNS:
        if pat.match(stem_stripped):
            return True
    return False


def slugify(text: str, max_len: int = MAX_SLUG_LEN) -> str:
    """Convert arbitrary text to a URL-safe, lowercase hyphenated slug."""
    # Normalize unicode to ASCII
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Lowercase
    text = text.lower()
    # Replace common separators and punctuation with spaces
    text = re.sub(r'[_\-/\\|:;,\.!?\(\)\[\]\{\}\'\"<>+=%@#$^&*~`]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Split into words, filter stopwords and generic words
    stopwords = {
        'a', 'an', 'the', 'and', 'or', 'of', 'in', 'to', 'for', 'with',
        'on', 'at', 'by', 'from', 'as', 'is', 'are', 'was', 'be', 'been',
        'being', 'this', 'that', 'it', 'its', 'you', 'your', 'we', 'our',
        'can', 'will', 'how', 'what', 'when', 'where', 'which', 'who',
        'no', 'not', 'but', 'so', 'if', 'then', 'than', 'up', 'into',
        'image', 'screenshot', 'figure', 'img', 'photo',
    }
    words = [w for w in text.split() if w and w not in stopwords and len(w) > 1]
    if not words:
        return ''
    slug = '-'.join(words)
    # Truncate at word boundary
    if len(slug) > max_len:
        slug = slug[:max_len]
        slug = slug.rsplit('-', 1)[0] if '-' in slug else slug[:max_len]
    # Clean leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def is_slug_too_generic(slug: str) -> bool:
    """Return True if the slug is too vague to be useful."""
    if not slug:
        return True
    parts = set(slug.split('-'))
    if parts <= BANNED_SOLE_CONTENT:
        return True
    if len(slug) < 5:
        return True
    return False


def find_all_md_files() -> list[Path]:
    """Return all .md files under docs/."""
    return list(DOCS_DIR.rglob('*.md'))


def build_reference_index(md_files: list[Path]) -> dict[str, list[Path]]:
    """
    Build a mapping: asset_filename -> [md_file, ...] for all generic assets.
    Only files in ASSETS_DIR are indexed.
    """
    index = defaultdict(list)
    asset_ref_pattern = re.compile(r'\.gitbook/assets/(.+?\.(?:png|jpg|jpeg|gif|svg|webp))', re.IGNORECASE)

    for md_path in md_files:
        try:
            text = md_path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        for match in asset_ref_pattern.finditer(text):
            fname = match.group(1)
            # Decode URL-encoding if any (e.g. %20 for space)
            try:
                from urllib.parse import unquote
                fname = unquote(fname)
            except Exception:
                pass
            index[fname].append(md_path)

    return index


def extract_context_for_asset(asset_name: str, md_files: list[Path]) -> str:
    """
    Extract the best descriptive text for an asset from its referencing markdown files.
    Priority: figcaption text > alt text > nearest heading > nearest paragraph sentence.
    Returns the best context string, or '' if none found.
    """
    # Patterns for different reference styles
    # Style 1: <figure><img src="...asset..." alt="ALT">...<figcaption><p>CAPTION</p></figcaption>
    # Style 2: ![ALT](path/to/asset)
    # Style 3: <img src="...asset..." alt="ALT">

    escaped = re.escape(asset_name)

    # We'll collect candidate strings
    candidates = []

    for md_path in md_files:
        try:
            text = md_path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        lines = text.splitlines()

        for i, line in enumerate(lines):
            if asset_name not in line:
                continue

            # --- Extract figcaption ---
            # Look for figcaption in nearby lines (this line and next ~5)
            window = '\n'.join(lines[max(0, i-1):min(len(lines), i+8)])
            figcap_match = re.search(r'<figcaption>\s*<p[^>]*>(.*?)</p>', window, re.DOTALL | re.IGNORECASE)
            if figcap_match:
                cap = re.sub(r'<[^>]+>', '', figcap_match.group(1)).strip()
                if cap and len(cap) > 4:
                    candidates.append(('figcaption', cap, md_path))

            # --- Extract alt text ---
            # From <img ... alt="ALT" ...>
            alt_match = re.search(r'alt=["\']([^"\']{4,})["\']', line, re.IGNORECASE)
            if alt_match:
                alt = alt_match.group(1).strip()
                if alt and len(alt) > 4:
                    candidates.append(('alt', alt, md_path))

            # --- Extract markdown alt: ![ALT](...) ---
            md_img_match = re.search(r'!\[([^\]]+)\]\(', line)
            if md_img_match:
                alt = md_img_match.group(1).strip()
                if alt and len(alt) > 4:
                    candidates.append(('md_alt', alt, md_path))

            # --- Extract nearest heading ---
            for j in range(i - 1, max(-1, i - 15), -1):
                heading_match = re.match(r'^#{1,4}\s+(.+)', lines[j])
                if heading_match:
                    heading_text = heading_match.group(1).strip()
                    if heading_text and len(heading_text) > 4:
                        candidates.append(('heading', heading_text, md_path))
                    break

            # --- Extract surrounding paragraph text ---
            # Look 3 lines above for a paragraph
            for j in range(i - 1, max(-1, i - 5), -1):
                para = lines[j].strip()
                # Skip blank lines, headings, HTML tags, code fences
                if not para or para.startswith('#') or para.startswith('<') or para.startswith('```') or para.startswith('|'):
                    continue
                # Take first sentence or up to 100 chars
                sentence = re.split(r'[.!?]', para)[0].strip()
                if sentence and len(sentence) > 8:
                    candidates.append(('paragraph', sentence, md_path))
                break

    if not candidates:
        return ''

    # Priority order: figcaption > alt > md_alt > heading > paragraph
    priority = {'figcaption': 0, 'alt': 1, 'md_alt': 2, 'heading': 3, 'paragraph': 4}
    candidates.sort(key=lambda x: priority.get(x[0], 99))

    # Return the best candidate
    return candidates[0][1] if candidates else ''


def make_unique_slug(slug: str, used_slugs: set, ext: str) -> str:
    """Ensure slug is unique among already-used slugs (with extension)."""
    candidate = slug + ext
    if candidate not in used_slugs:
        return slug
    # Append numeric suffix
    n = 2
    while True:
        truncated = slug[:MAX_SLUG_LEN - len(str(n)) - 1]
        new_slug = f"{truncated}-{n}"
        candidate = new_slug + ext
        if candidate not in used_slugs:
            return new_slug
        n += 1


def update_references(old_name: str, new_name: str, md_files: list[Path], dry_run: bool) -> int:
    """Replace all references to old_name with new_name in all md files. Returns count of files changed."""
    changed = 0
    # We need to handle both URL-encoded and plain references
    for md_path in md_files:
        try:
            text = md_path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        if old_name not in text:
            continue

        new_text = text.replace(old_name, new_name)
        if new_text != text:
            if not dry_run:
                md_path.write_text(new_text, encoding='utf-8')
            changed += 1

    return changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("=== DRY RUN — no files will be changed ===\n")

    # Gather all assets
    all_asset_files = [f for f in ASSETS_DIR.iterdir() if f.is_file()]
    generic_files = [f for f in all_asset_files if is_generic(f.stem)]

    print(f"Total assets: {len(all_asset_files)}")
    print(f"Generic-named assets found: {len(generic_files)}\n")

    # Build reference index
    print("Building markdown reference index...")
    all_md_files = find_all_md_files()
    print(f"Scanning {len(all_md_files)} markdown files...\n")
    ref_index = build_reference_index(all_md_files)

    # Track used slugs to avoid collisions
    # Seed with existing non-generic asset names
    used_slugs: set[str] = set()
    for f in all_asset_files:
        if not is_generic(f.stem):
            used_slugs.add(f.name)

    stats = {'renamed': 0, 'skipped_no_context': 0, 'skipped_no_ref': 0, 'errors': 0}
    rename_plan: list[tuple[Path, Path, str]] = []  # (old_path, new_path, reason)

    for asset_file in sorted(generic_files):
        fname = asset_file.name
        ext = asset_file.suffix.lower()

        # Find which md files reference this asset
        referencing_files = ref_index.get(fname, [])

        if not referencing_files:
            stats['skipped_no_ref'] += 1
            continue

        # Extract context
        context = extract_context_for_asset(fname, referencing_files)

        if not context:
            stats['skipped_no_context'] += 1
            continue

        # Generate slug
        slug = slugify(context)

        if is_slug_too_generic(slug):
            stats['skipped_no_context'] += 1
            continue

        # Ensure uniqueness
        final_slug = make_unique_slug(slug, used_slugs, ext)
        new_name = final_slug + ext
        new_path = ASSETS_DIR / new_name

        used_slugs.add(new_name)
        rename_plan.append((asset_file, new_path, context))

    # Report plan
    print(f"Planned renames: {len(rename_plan)}")
    print(f"Skipped (no markdown reference): {stats['skipped_no_ref']}")
    print(f"Skipped (no usable context): {stats['skipped_no_context']}")
    print()

    # Show plan
    for old_path, new_path, context in rename_plan:
        print(f"  {old_path.name}")
        print(f"  -> {new_path.name}")
        print(f"     context: \"{context[:80]}\"")
        print()

    if dry_run:
        print("=== DRY RUN complete — no changes made ===")
        return

    # Execute renames
    print("\nExecuting renames...")
    for old_path, new_path, context in rename_plan:
        try:
            # 1. Update all markdown references first
            refs_updated = update_references(old_path.name, new_path.name, all_md_files, dry_run=False)
            # 2. Rename the file
            old_path.rename(new_path)
            stats['renamed'] += 1
            print(f"  OK  {old_path.name} -> {new_path.name}  ({refs_updated} md file(s) updated)")
        except Exception as e:
            stats['errors'] += 1
            print(f"  ERR {old_path.name}: {e}")

    print()
    print("=== Summary ===")
    print(f"  Renamed:                  {stats['renamed']}")
    print(f"  Skipped (no reference):   {stats['skipped_no_ref']}")
    print(f"  Skipped (no context):     {stats['skipped_no_context']}")
    print(f"  Errors:                   {stats['errors']}")


if __name__ == '__main__':
    main()
