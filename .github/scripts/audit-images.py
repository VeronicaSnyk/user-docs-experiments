#!/usr/bin/env python3
"""
audit-images.py — Image quality audit for Snyk user-docs.

Checks:
  1. Missing alt text on images (accessibility).
  2. Orphaned assets — images in .gitbook/assets/ not referenced by any doc.
  3. External image sources (Google Drive, CDN embeds) — fragile, should be hosted locally.
  4. Generic filenames (e.g., "image (12).png") — hard to manage and track.

Outputs a Markdown report to stdout.

Usage:
    python3 .github/scripts/audit-images.py [--path docs/] [--fail-on error]

    --fail-on: exit non-zero on 'error' (default), 'warning', or 'none'
"""

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
DOCS_ROOT = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_ROOT / ".gitbook" / "assets"

IMAGE_ANGLE_RE = re.compile(r'!\[([^\]]*)\]\(<([^>]+)>\)')
IMAGE_INLINE_RE = re.compile(r'!\[([^\]]*)\]\(([^)<][^)]*)\)')
HTML_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')
HTML_HREF_IMG_RE = re.compile(
    r'<a[^>]+href=["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg|webp|pdf))["\']', re.I
)
COVER_FRONTMATTER_RE = re.compile(r'^cover:\s*(.+)$', re.M)
GITBOOK_FILE_RE = re.compile(r'\{%\s*file\s+src=["\']([^"\']+)["\']')
EXTERNAL_IMAGE_DOMAINS = [
    "lh7-rt.googleusercontent.com",
    "lh3.googleusercontent.com",
    "lh6.googleusercontent.com",
    "docs.google.com",
    "drive.google.com",
    "cloudinary.com",
    "res.cloudinary.com",
]
GENERIC_NAME_RE = re.compile(r'^image\s*\(\d+\)', re.IGNORECASE)


def is_external(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def asset_name_from_url(url):
    """Extract bare filename from a markdown URL, handling angle brackets,
    spaces, anchors, and URL encoding. Returns None for external URLs."""
    url = url.strip().strip('"').strip("'")
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1]
    if is_external(url) or url.startswith(("mailto:", "data:")):
        return None
    url = url.split("#")[0]
    url = urllib.parse.unquote(url)
    return Path(url).name


def scan_docs(docs_root: Path) -> dict:
    """Scan all markdown files and return audit findings."""
    findings = {
        "missing_alt": [],       # (file, line, src)
        "external_images": [],   # (file, line, src, domain)
        "referenced_assets": set(),
    }

    for md_file in sorted(docs_root.rglob("*.md")):
        rel = md_file.relative_to(docs_root.parent)
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Per-line scan: missing alt text + external image flagging
        for line_num, line in enumerate(content.splitlines(), 1):
            for regex in (IMAGE_ANGLE_RE, IMAGE_INLINE_RE):
                for match in regex.finditer(line):
                    alt_text = match.group(1).strip()
                    raw_src = match.group(2).strip()
                    name = asset_name_from_url(raw_src)
                    if name:
                        findings["referenced_assets"].add(name)
                    elif is_external(raw_src):
                        for domain in EXTERNAL_IMAGE_DOMAINS:
                            if domain in raw_src:
                                findings["external_images"].append({
                                    "file": str(rel),
                                    "line": line_num,
                                    "src": raw_src[:80] + ("..." if len(raw_src) > 80 else ""),
                                    "domain": domain,
                                })
                                break
                    if not alt_text:
                        findings["missing_alt"].append({
                            "file": str(rel),
                            "line": line_num,
                            "src": name or raw_src[:60],
                        })

        # Whole-file scan: HTML, GitBook, frontmatter patterns
        for regex in (HTML_IMG_RE, HTML_HREF_IMG_RE, COVER_FRONTMATTER_RE, GITBOOK_FILE_RE):
            for match in regex.finditer(content):
                name = asset_name_from_url(match.group(1))
                if name:
                    findings["referenced_assets"].add(name)

    return findings


def scan_assets(assets_dir: Path, referenced: set) -> dict:
    """Find orphaned and generically named assets."""
    findings = {
        "orphaned": [],
        "generic_names": [],
    }

    if not assets_dir.exists():
        return findings

    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}
    for asset in sorted(assets_dir.iterdir()):
        if asset.suffix.lower() not in image_extensions:
            continue
        if asset.name not in referenced:
            findings["orphaned"].append(asset.name)
        if GENERIC_NAME_RE.match(asset.stem):
            findings["generic_names"].append(asset.name)

    return findings


def render_report(doc_findings: dict, asset_findings: dict) -> tuple[str, bool, bool]:
    """Return (markdown_report, has_errors, has_warnings)."""
    lines = ["# Image Audit Report\n"]
    has_errors = False
    has_warnings = False

    # Missing alt text — accessibility error
    missing_alt = doc_findings["missing_alt"]
    if missing_alt:
        has_errors = True
        lines.append(f"## ❌ Missing alt text ({len(missing_alt)} images)\n")
        lines.append("Images without alt text are inaccessible to screen readers.\n")
        lines.append("| File | Line | Image |\n|------|------|-------|\n")
        for item in missing_alt[:50]:  # cap at 50 for readability
            lines.append(f"| `{item['file']}` | {item['line']} | `{item['src']}` |")
        if len(missing_alt) > 50:
            lines.append(f"\n_...and {len(missing_alt) - 50} more._")
        lines.append("")

    # External image sources — warning
    external = doc_findings["external_images"]
    if external:
        has_warnings = True
        lines.append(f"## ⚠️ External image sources ({len(external)} found)\n")
        lines.append("These images are hosted externally and may break without notice. "
                     "Download and host them in `.gitbook/assets/`.\n")
        lines.append("| File | Line | Domain | URL |\n|------|------|--------|-----|\n")
        for item in external:
            lines.append(f"| `{item['file']}` | {item['line']} | `{item['domain']}` | `{item['src']}` |")
        lines.append("")

    # Orphaned assets — warning
    orphaned = asset_findings["orphaned"]
    if orphaned:
        has_warnings = True
        lines.append(f"## ⚠️ Orphaned assets ({len(orphaned)} files)\n")
        lines.append("These files exist in `.gitbook/assets/` but are not referenced in any doc. "
                     "Remove them to reduce repo bloat.\n")
        for name in orphaned[:50]:
            lines.append(f"- `{name}`")
        if len(orphaned) > 50:
            lines.append(f"\n_...and {len(orphaned) - 50} more._")
        lines.append("")

    # Generic filenames — suggestion
    generic = asset_findings["generic_names"]
    if generic:
        lines.append(f"## 💡 Generic filenames ({len(generic)} files)\n")
        lines.append("These files have auto-generated names (e.g., `image (12).png`). "
                     "Rename them descriptively so they can be tracked and replaced.\n")
        for name in generic[:30]:
            lines.append(f"- `{name}`")
        if len(generic) > 30:
            lines.append(f"\n_...and {len(generic) - 30} more._")
        lines.append("")

    if not has_errors and not has_warnings and not generic:
        lines.append("## ✅ All image checks passed\n")
        lines.append("No missing alt text, orphaned assets, or external image sources found.")

    return "\n".join(lines), has_errors, has_warnings


def main():
    parser = argparse.ArgumentParser(description="Audit images in user-docs.")
    parser.add_argument("--path", default=str(DOCS_ROOT))
    parser.add_argument("--fail-on", choices=["error", "warning", "none"], default="error")
    args = parser.parse_args()

    docs_root = Path(args.path)
    print(f"Scanning {docs_root}...", file=sys.stderr)

    doc_findings = scan_docs(docs_root)
    asset_findings = scan_assets(ASSETS_DIR, doc_findings["referenced_assets"])

    report, has_errors, has_warnings = render_report(doc_findings, asset_findings)
    print(report)

    if args.fail_on == "error" and has_errors:
        sys.exit(1)
    elif args.fail_on == "warning" and (has_errors or has_warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
