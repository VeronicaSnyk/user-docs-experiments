#!/usr/bin/env python3
"""Spot-check orphans using exact filename grep against all docs."""
import re
import subprocess
from pathlib import Path

DOCS_ROOT = Path("docs")
ASSETS_DIR = DOCS_ROOT / ".gitbook" / "assets"

IMAGE_MD_RE = re.compile(r'!\[[^\]]*\]\(<([^>]+)>|!\[[^\]]*\]\(([^)<>][^)]*)\)')
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')

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

image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}
all_assets = [a for a in ASSETS_DIR.iterdir() if a.suffix.lower() in image_extensions]
orphaned = sorted(a for a in all_assets if a.name not in referenced)

# Sample every 20th file and do a fixed-string exact grep
samples = orphaned[::20]
print(f"Spot-checking {len(samples)} samples (every 20th of {len(orphaned)}) with exact grep...\n")
failures = []
for asset in samples:
    result = subprocess.run(
        ["grep", "-rF", asset.name, "docs/"],
        capture_output=True, text=True
    )
    hits = [h for h in result.stdout.strip().splitlines()
            if asset.name in h]  # exact name in line
    if hits:
        failures.append((asset.name, hits))
        print(f"  FOUND: {asset.name}")
        for h in hits[:2]:
            print(f"    {h[:120]}")
    else:
        print(f"  clean: {asset.name[:70]}")

print(f"\n{'⚠ ' + str(len(failures)) + ' false positives found — review before deleting' if failures else '✅ All spot-checked samples confirmed orphaned'}")
