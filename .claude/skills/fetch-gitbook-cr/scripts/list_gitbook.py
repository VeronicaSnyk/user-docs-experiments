#!/usr/bin/env python3
"""Discover GitBook space IDs and change-request IDs.

Usage:
  # 1. List all orgs + spaces you can access (find the space ID):
  python list_gitbook.py

  # 2. List change requests in a space (find the CR ID):
  python list_gitbook.py <SPACE_ID>

Requires GITBOOK_API_TOKEN in .docs-agent/.env (or env).
"""
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env: shared .docs-agent/.env, then skill-local, then cwd
script_dir = Path(__file__).resolve().parent
docs_agent_dir = script_dir.parents[2]  # .../.docs-agent
for env_path in (docs_agent_dir / ".env", script_dir / ".env",
                 Path.cwd() / ".docs-agent" / ".env", Path.cwd() / ".env"):
    if env_path.exists():
        load_dotenv(env_path)
        break
else:
    load_dotenv()

TOKEN = os.environ.get("GITBOOK_API_TOKEN")
if not TOKEN:
    print("Error: GITBOOK_API_TOKEN missing in .docs-agent/.env", file=sys.stderr)
    sys.exit(1)

API = "https://api.gitbook.com/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}


def get_all(url):
    """GET a paginated GitBook endpoint, following `next.page` cursors."""
    items, params = [], {}
    while True:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("items", []))
        nxt = data.get("next", {}).get("page")
        if not nxt:
            return items
        params = {"page": nxt}


def list_spaces():
    me = requests.get(f"{API}/user", headers=HEADERS, timeout=30)
    me.raise_for_status()
    print(f"Authenticated as: {me.json().get('displayName') or me.json().get('email')}\n")

    orgs = get_all(f"{API}/orgs")
    if not orgs:
        print("No organizations visible to this token.")
        return
    for org in orgs:
        print(f"# Org: {org['title']}  (id: {org['id']})")
        spaces = get_all(f"{API}/orgs/{org['id']}/spaces")
        for s in spaces:
            print(f"   space: {s['title']:<40}  id: {s['id']}")
        print()


def list_change_requests(space_id):
    crs = get_all(f"{API}/spaces/{space_id}/change-requests")
    if not crs:
        print(f"No change requests in space {space_id}.")
        return
    print(f"Change requests in space {space_id}:\n")
    for cr in crs:
        print(
            f"  #{cr.get('number','?'):<5} id: {cr['id']}  "
            f"[{cr.get('status','?')}]  {cr.get('subject') or cr.get('title','(no title)')}"
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        list_change_requests(sys.argv[1])
    else:
        list_spaces()
