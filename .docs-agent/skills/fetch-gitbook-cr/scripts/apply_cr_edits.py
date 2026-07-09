#!/usr/bin/env python3
"""Apply verified markdown edits to GitBook change-request pages.

Usage:
  python apply_cr_edits.py check    # verify every target string matches, no writes
  python apply_cr_edits.py apply    # apply edits page by page, then re-verify
"""
import os, sys, json
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")
T = os.environ["GITBOOK_API_TOKEN"]
H = {"Authorization": f"Bearer {T}", "Accept": "application/json", "Content-Type": "application/json"}
API = "https://api.gitbook.com/v1"; S = "N5N885PkllOWeBmgm3Bp"; CR = "12"

# (page_id, page_name, [ (old, new, expected_count) ])  expected_count None = replace_all (>=1)
EDITS = [
 ("QtEnHQTwb4KXYNoyES9e", "Evo by Snyk", [
   ('{% hint style="info" %}\nTo access additional capabilities, navigate to [Evo by Snyk](https://evo.ai.snyk.io/) and apply to become a design partner.\n{% endhint %}\n\n',
    '', 1),
   ('Evo has two layers:\n\n* **Solutions** discover your AI assets and assess their risk.\n* **Surfaces** let you review that risk, govern it with policy, and report on it. A solution discovers an asset and surfaces its risk context, you apply that context in your policies, and Evo raises an issue when an asset violates a policy. You then triage and resolve that issue in your standard security workflow.',
    'The platform surfaces described in this documentation present the different Evo solutions. A solution discovers an asset and surfaces its risk context. You apply that context in your policies, and Evo raises an issue when an asset violates a policy. You then triage and resolve that issue in your standard security workflow.', 1),
 ]),
 ("ZxhSJiaYd8FiIRaJ67SK", "Activation and deployment", [
   ('Follow the on-screen instructions to install on a local machine or through your MDM tool. Advanced options are available for endpoints that run security tooling such as Zscaler or CrowdStrike.',
    'Follow the on-screen instructions to install on a local machine or through your MDM tool.', 1),
 ]),
 ("JDrQtn8uN8qJnbsX2w2v", "Agent Supply Chain Security", [
   ('Agent Supply Chain Security is a capability of Agentic Development Security. Its assets are surfaced under **Inventory** > **Machines**.',
    'Evo surfaces Agent Supply Chain Security assets under **Inventory** > **Machines**.', 1),
   ('* **Prompt injection**: hidden instructions in a tool description that the agent processes as commands.',
    '* **Prompt injection in tool**: hidden instructions in a tool description that the agent processes as commands.', 1),
   ("* **System service modification**: instructions to change the host's system files, accounts, or privileges.",
    "* **Attempt to modify system services**: instructions to change the host's system files, accounts, or privileges.", 1),
 ]),
 ("PIY0AYvVHHvaqsPzPQRg", "Access and authentication", [
   ('To use Evo, enable it for your tenant, then add the members who need access.\n\nOnce Evo is enabled:',
    'You must enable Evo for your Snyk Tenant before you can use it. To enable it, contact your Snyk account team. Then add the members who need access.\n\nAfter Evo is enabled:', 1),
   ('2. Sign in using your existing Snyk authentication workflow.',
    '2. Log in using your existing Snyk authentication workflow.', 1),
 ]),
 ("PLLtKcbhnFqk7Kjf4fh0", "Trusted Output Assurance", [
   ('* [Distribution at scale](../../agentic-security-with-snyk-studio/distribution-at-scale) to roll out Snyk Studio across your organization',
    '* [Activation and deployment](activation-and-deployment) to roll out Agentic Development Security across your organization', 1),
 ]),
 ("b8xXw9khz4kyv4KQTG07", "Agent Behavior Governance", [
   ('Agent Behavior Governance is a capability of Agentic Development Security.\n\n', '', 1),
   ('You review and govern Behavioral Agent Governance in the **Observe** area. During open preview, Observe is separate from the platform surfaces.',
    'You review and govern agent behavior in the **Observe** area. During open preview, **Observe** is separate from the platform surfaces.', 1),
   ('Behavioral Agent Governance', 'Agent Behavior Governance', None),  # replace_all remaining
 ]),
]

def get_md(pid):
    r = requests.get(f"{API}/spaces/{S}/change-requests/{CR}/content/page/{pid}?format=markdown", headers=H, timeout=30)
    r.raise_for_status()
    return r.json()["markdown"]

def apply_edits(md, edits):
    for old, new, cnt in edits:
        n = md.count(old)
        if cnt is None:
            if n < 1: raise AssertionError(f"replace_all target not found: {old[:60]!r}")
        elif n != cnt:
            raise AssertionError(f"expected {cnt} match(es), found {n}: {old[:60]!r}")
        md = md.replace(old, new)
    return md

def put_md(pid, md):
    body = {"changes": [{"operation": "update_page", "page": pid, "document": {"markdown": md}}]}
    r = requests.post(f"{API}/spaces/{S}/change-requests/{CR}/content", headers=H, data=json.dumps(body), timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"PUT failed {r.status_code}: {r.text}")
    return r.status_code

mode = sys.argv[1] if len(sys.argv) > 1 else "check"
for pid, name, edits in EDITS:
    md = get_md(pid)
    try:
        newmd = apply_edits(md, edits)
    except AssertionError as e:
        print(f"✗ {name} ({pid}): {e}")
        continue
    changed = newmd != md
    print(f"{'✓' if changed else '–'} {name} ({pid}): {len(edits)} edit(s) matched, {'CHANGED' if changed else 'no change'}")
    if mode == "apply" and changed:
        code = put_md(pid, newmd)
        verify = get_md(pid)
        ok = all((new in verify) for old, new, _ in edits if new) and all((old not in verify) for old, new, _ in edits if old and old not in verify or True)
        # simpler verify: every old removed (for non-empty new) and new present
        problems = []
        for old, new, _ in edits:
            if new and new not in verify: problems.append(f"new missing: {new[:40]!r}")
        print(f"    submitted (HTTP {code}); verify: {'OK' if not problems else problems}")
