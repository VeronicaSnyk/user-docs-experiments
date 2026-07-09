#!/usr/bin/env python3
"""Count truly orphaned assets by scanning all reference patterns."""
import re
from pathlib import Path

DOCS_ROOT = Path("docs")
ASSETS_DIR = DOCS_ROOT / ".gitbook" / "assets"

# Markdown image: ![alt](path) and ![alt](<path>)
IMAGE_MD_RE = re.compile(r'!\[[^\]]*\]\(<([^>]+)>|!\[[^\]]*\]\(([^)<>][^)]*)\)')
# HTML src attribute
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')

referenced = set()
for md_file in sorted(DOCS_ROOT.rglob("*.md")):
    try:
        content = md_file.read_text(encoding="utf-8")
    except Exception:
        continue
    for m in IMAGE_MD_RE.finditer(content):
        src = (m.group(1) or m.group(2) or "").strip().split(" ")[0]
        if src and not src.startswith("http"):
            referenced.add(Path(src).name)
    for m in SRC_RE.finditer(content):
        src = m.group(1).strip()
        if src and not src.startswith("http"):
            referenced.add(Path(src).name)

image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}
all_assets = [a for a in ASSETS_DIR.iterdir() if a.suffix.lower() in image_extensions]
orphaned = sorted(a for a in all_assets if a.name not in referenced)

print(f"Referenced: {len(referenced)}")
print(f"Orphaned:   {len(orphaned)}")
print(f"Total:      {len(all_assets)}")
