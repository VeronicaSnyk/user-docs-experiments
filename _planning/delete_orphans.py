#!/usr/bin/env python3
"""Delete orphaned assets from .gitbook/assets/ and print a manifest."""
import re
import sys
from pathlib import Path

DOCS_ROOT = Path("docs")
ASSETS_DIR = DOCS_ROOT / ".gitbook" / "assets"

IMAGE_MD_RE = re.compile(r'!\[[^\]]*\]\(<([^>]+)>|!\[[^\]]*\]\(([^)<>][^)]*)\)')
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')
# GitBook card covers use <a href="...asset..."> not <img>
HREF_ASSET_RE = re.compile(r'href=["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg|webp|pdf))["\']')
# GitBook page cover frontmatter: "cover: .gitbook/assets/name.png"
COVER_RE = re.compile(r'^cover:\s+(\S+)', re.MULTILINE)

referenced = set()
for md_file in sorted(DOCS_ROOT.rglob("*.md")):
    try:
        content = md_file.read_text(encoding="utf-8")
    except Exception:
        continue
    for m in IMAGE_MD_RE.finditer(content):
        src = re.sub(r'\s+["\'].*$', '', (m.group(1) or m.group(2) or "").strip())
        if src and not src.startswith("http"):
            referenced.add(Path(src).name)
    for m in SRC_RE.finditer(content):
        src = m.group(1).strip()
        if src and not src.startswith("http"):
            referenced.add(Path(src).name)
    for m in HREF_ASSET_RE.finditer(content):
        src = m.group(1).strip()
        if src and not src.startswith("http"):
            referenced.add(Path(src).name)
    for m in COVER_RE.finditer(content):
        src = m.group(1).strip()
        if src and not src.startswith("http"):
            referenced.add(Path(src).name)

image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}
all_assets = [a for a in ASSETS_DIR.iterdir() if a.suffix.lower() in image_extensions]
orphaned = sorted(a for a in all_assets if a.name not in referenced)

dry_run = "--dry-run" in sys.argv

print(f"{'DRY RUN — ' if dry_run else ''}Deleting {len(orphaned)} orphaned assets...\n")
for asset in orphaned:
    print(f"  {asset.name}")
    if not dry_run:
        asset.unlink()

print(f"\n{'Would delete' if dry_run else 'Deleted'} {len(orphaned)} files.")
