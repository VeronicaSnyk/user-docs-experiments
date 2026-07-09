#!/usr/bin/env python3
"""
Extract and categorize URLs from Jira ticket content.

Usage:
    python scripts/extract_urls.py <ticket_key>

Output:
    JSON with categorized URLs (Confluence, Google Docs, other)
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

# Add parent skill directory to path to import from fetch-jira-ticket
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'fetch-jira-ticket' / 'scripts'))

# Load environment variables
script_dir = Path(__file__).parent
skill_dir = script_dir.parent
docs_agent_dir = skill_dir.parent.parent

env_locations = [
    docs_agent_dir / '.env',
    skill_dir / '.env',
    Path.cwd() / '.docs-agent' / '.env',
    Path.cwd() / '.env',
]

for env_path in env_locations:
    if env_path.exists():
        load_dotenv(env_path)
        break
else:
    load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')


def extract_urls_from_text(text):
    """Extract all URLs from text."""
    if not text:
        return []

    # Simple URL regex pattern
    url_pattern = r'https?://[^\s<>"{}|\\^\[\]`]+'
    matches = re.findall(url_pattern, str(text))

    cleaned = []
    for url in matches:
        # Strip trailing punctuation left over from prose/markdown, for
        # example ".", ",", ";", "]", ">". A trailing ")" is handled
        # separately below so balanced parentheses inside a URL survive.
        prev = None
        while url != prev:
            prev = url
            url = url.rstrip('.,;]>')
            # Drop a trailing ")" only when unbalanced (markdown [text](url)).
            if url.endswith(')') and url.count(')') > url.count('('):
                url = url[:-1]
        cleaned.append(url)

    return cleaned


def categorize_url(url):
    """Categorize URL by type."""
    parsed = urlparse(url)
    hostname = parsed.hostname or ''

    if 'atlassian.net/wiki' in url or 'confluence' in hostname:
        return 'confluence'
    elif 'docs.google.com/document' in url:
        return 'google_docs'
    elif 'docs.google.com/spreadsheets' in url:
        return 'google_sheets'
    elif 'github.com' in hostname:
        return 'github'
    else:
        return 'other'


def parse_adf_for_urls(adf_content):
    """Extract URLs from Atlassian Document Format content."""
    urls = []

    def traverse(node):
        if isinstance(node, dict):
            # Check for link marks
            marks = node.get('marks', [])
            for mark in marks:
                if mark.get('type') == 'link':
                    href = mark.get('attrs', {}).get('href')
                    if href:
                        urls.append(href)

            # Check for text content (may contain URLs)
            if node.get('type') == 'text':
                text = node.get('text', '')
                urls.extend(extract_urls_from_text(text))

            # Traverse content
            content = node.get('content', [])
            for item in content:
                traverse(item)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(adf_content)
    return urls


def extract_ticket_urls(ticket_data):
    """Extract all URLs from a Jira ticket."""
    fields = ticket_data.get('fields', {})
    all_urls = []

    # Extract from description
    description = fields.get('description')
    if description:
        if isinstance(description, dict):  # ADF format
            all_urls.extend(parse_adf_for_urls(description))
        else:  # Plain text
            all_urls.extend(extract_urls_from_text(description))

    # Extract from comments
    comments = ticket_data.get('fields', {}).get('comment', {}).get('comments', [])
    for comment in comments:
        body = comment.get('body')
        if body:
            if isinstance(body, dict):  # ADF format
                all_urls.extend(parse_adf_for_urls(body))
            else:  # Plain text
                all_urls.extend(extract_urls_from_text(body))

    return all_urls


def main():
    parser = argparse.ArgumentParser(
        description='Extract and categorize URLs from Jira ticket',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('ticket_key', help='Jira ticket key (e.g., DOC-123)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Validate credentials (after arg parsing so --help works without creds)
    if not all([JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
        print("Error: Missing Jira credentials in .env file", file=sys.stderr)
        sys.exit(1)

    # Lazy import so --help works without triggering the JiraClient
    # module's import-time credential check.
    from fetch_jira_ticket import JiraClient

    # Fetch ticket
    client = JiraClient(JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN)

    # Get full ticket data with comments
    api_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{args.ticket_key.upper()}"
    params = {
        'expand': 'renderedFields,names,schema,transitions,changelog',
        'fields': 'description,comment,summary,labels'
    }

    try:
        response = client.session.get(api_url, params=params)
        response.raise_for_status()
        ticket_data = response.json()
    except Exception as e:
        print(f"Error fetching ticket: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract URLs
    urls = extract_ticket_urls(ticket_data)

    # Categorize URLs
    categorized = {
        'confluence': [],
        'google_docs': [],
        'google_sheets': [],
        'github': [],
        'other': []
    }

    for url in set(urls):  # Remove duplicates
        category = categorize_url(url)
        categorized[category].append(url)

    # Output
    result = {
        'ticket_key': args.ticket_key.upper(),
        'ticket_summary': ticket_data.get('fields', {}).get('summary', ''),
        'labels': ticket_data.get('fields', {}).get('labels', []),
        'total_urls': len(urls),
        'unique_urls': len(set(urls)),
        'urls': categorized
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Ticket: {result['ticket_key']} - {result['ticket_summary']}")
        print(f"Labels: {', '.join(result['labels'])}")
        print(f"\nFound {result['unique_urls']} unique URLs:")

        if categorized['confluence']:
            print(f"\n📄 Confluence pages ({len(categorized['confluence'])}):")
            for url in categorized['confluence']:
                print(f"  - {url}")

        if categorized['google_docs']:
            print(f"\n📝 Google Docs ({len(categorized['google_docs'])}):")
            for url in categorized['google_docs']:
                print(f"  - {url}")

        if categorized['google_sheets']:
            print(f"\n📊 Google Sheets ({len(categorized['google_sheets'])}):")
            for url in categorized['google_sheets']:
                print(f"  - {url}")

        if categorized['github']:
            print(f"\n🔗 GitHub ({len(categorized['github'])}):")
            for url in categorized['github']:
                print(f"  - {url}")

        if categorized['other']:
            print(f"\n🌐 Other URLs ({len(categorized['other'])}):")
            for url in categorized['other']:
                print(f"  - {url}")

        # Provide fetch commands
        print("\n" + "="*60)
        print("Commands to fetch referenced content:")
        print("="*60)

        for url in categorized['confluence']:
            print(f"\npython .docs-agent/skills/fetch-confluence/scripts/fetch_confluence.py '{url}'")

        for url in categorized['google_docs']:
            print(f"\npython .docs-agent/skills/fetch-google-docs/scripts/fetch_google_docs.py '{url}'")


if __name__ == '__main__':
    main()
