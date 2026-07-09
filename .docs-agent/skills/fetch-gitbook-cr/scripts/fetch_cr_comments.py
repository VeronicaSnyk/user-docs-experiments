#!/usr/bin/env python3
"""Fetch a GitBook change request and its comments, annotated with the page
title and section (nearest heading) each comment lives under.

Usage:
  python fetch_cr_comments.py <SPACE_ID> <CHANGE_REQUEST_ID_OR_NUMBER>
  python fetch_cr_comments.py <SPACE_ID> <CR> --author "Ezra"   # filter by author

Requires GITBOOK_API_TOKEN in .docs-agent/.env (or env).
"""
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

script_dir = Path(__file__).resolve().parent
docs_agent_dir = script_dir.parents[2]
for env_path in (docs_agent_dir / ".env", script_dir / ".env", Path.cwd() / ".env"):
    if env_path.exists():
        load_dotenv(env_path)
        break
else:
    load_dotenv()

TOKEN = os.environ.get("GITBOOK_API_TOKEN")
if not TOKEN:
    print("Error: GITBOOK_API_TOKEN missing in .docs-agent/.env", file=sys.stderr)
    sys.exit(1)

API = os.environ.get("GITBOOK_API_BASE_URL", "https://api.gitbook.com/v1")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}


# ── document helpers ────────────────────────────────────────────────────────
def doc_to_text(node):
    if isinstance(node, dict):
        if node.get("object") == "leaf":
            return node.get("text", "")
        if node.get("object") == "inline" and node.get("type") == "mention":
            ref = (node.get("data") or {}).get("ref") or {}
            return f"@{ref.get('user', 'user')}"
        parts = []
        for key in ("document", "nodes", "leaves"):
            child = node.get(key)
            if child is not None:
                parts.append(doc_to_text(child))
        text = "".join(parts)
        if node.get("object") == "block" and node.get("type") == "paragraph":
            return text + "\n"
        return text
    if isinstance(node, list):
        return "".join(doc_to_text(n) for n in node)
    return ""


def body_text(c):
    body = c.get("body") or c.get("text") or c.get("document") or ""
    if isinstance(body, dict):
        return doc_to_text(body).strip()
    return str(body).strip()


def block_text(b):
    return doc_to_text(b).strip().replace("\n", " ")


def build_section_map(document):
    """Walk a page document in order; map every block key -> nearest heading text."""
    out, current = {}, None

    def walk(nodes):
        nonlocal current
        for b in nodes or []:
            t = b.get("type", "")
            if t.startswith("heading"):
                current = block_text(b)
            key = b.get("key")
            if key:
                out[key] = current
            walk(b.get("nodes"))

    walk(document.get("nodes"))
    return out


# ── HTTP ────────────────────────────────────────────────────────────────────
def get_json(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code >= 400:
        print(f"HTTP {r.status_code} on {url}\n{r.text}", file=sys.stderr)
        r.raise_for_status()
    return r.json()


def get_all(url):
    items, params = [], {}
    while True:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        if "items" not in data:
            return data
        items.extend(data["items"])
        nxt = data.get("next", {}).get("page")
        if not nxt:
            return items
        params = {"page": nxt}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    author_filter = None
    if "--author" in sys.argv:
        author_filter = sys.argv[sys.argv.index("--author") + 1].lower()
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    space, cr = args[0], args[1]

    info = get_all(f"{API}/spaces/{space}/change-requests/{cr}")
    print(f"# CR #{info.get('number')} — {info.get('subject') or info.get('title')}")
    print(f"  status {info.get('status')} · updated {info.get('updatedAt')}\n")

    # page id -> (title, path) and ordered list of page ids
    content = get_json(f"{API}/spaces/{space}/change-requests/{cr}/content")
    pages = {}
    order = []

    def walk_pages(pl):
        for p in pl:
            pages[p["id"]] = (p.get("title", "?"), p.get("path", ""))
            order.append(p["id"])
            walk_pages(p.get("pages", []))

    walk_pages(content.get("pages", []))

    comments = get_all(f"{API}/spaces/{space}/change-requests/{cr}/comments")
    if not isinstance(comments, list):
        comments = comments.get("items", [])
    if author_filter:
        comments = [
            c for c in comments
            if author_filter in ((c.get("postedBy") or {}).get("displayName", "")
                                  + (c.get("postedBy") or {}).get("email", "")).lower()
        ]

    # group comments by page
    by_page = {}
    for c in comments:
        pid = ((c.get("target") or {}).get("page") or {}).get("id") or "(none)"
        by_page.setdefault(pid, []).append(c)

    section_cache = {}
    n = 0
    for pid in order + [p for p in by_page if p not in order]:
        if pid not in by_page:
            continue
        title, path = pages.get(pid, ("(unknown page)", ""))
        print(f"\n{'='*70}\nPAGE: {title}   [{path}]\n{'='*70}")
        if pid not in section_cache and pid != "(none)":
            try:
                doc = get_json(
                    f"{API}/spaces/{space}/change-requests/{cr}/content/page/{pid}?format=document"
                )
                section_cache[pid] = build_section_map(doc.get("document", {}))
            except Exception:
                section_cache[pid] = {}
        smap = section_cache.get(pid, {})
        for c in by_page[pid]:
            n += 1
            who = (c.get("postedBy") or {}).get("displayName", "?")
            node_id = ((c.get("target") or {}).get("node") or {}).get("id")
            section = smap.get(node_id) or "(intro / no heading)"
            print(f"\n[{n}] {who} · section: «{section}» · {c.get('status')} · id {c.get('id')}")
            print(body_text(c) or "(empty)")
            if c.get("replies"):
                try:
                    rs = get_all(
                        f"{API}/spaces/{space}/change-requests/{cr}/comments/{c.get('id')}/replies"
                    )
                    rs = rs if isinstance(rs, list) else rs.get("items", [])
                    for r in rs:
                        rn = (r.get("postedBy") or {}).get("displayName", "?")
                        print(f"    ↳ {rn}: {body_text(r)}")
                except Exception:
                    print(f"    ({c.get('replies')} replies — could not fetch)")


if __name__ == "__main__":
    main()
