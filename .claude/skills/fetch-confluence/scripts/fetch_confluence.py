#!/usr/bin/env python3
"""
Fetch content from Confluence using the Confluence REST API.

Usage:
    python scripts/fetch_confluence.py <page_url_or_id>
    python scripts/fetch_confluence.py --search "query"

Examples:
    python scripts/fetch_confluence.py https://snyksec.atlassian.net/wiki/spaces/DOC/pages/123456/Page+Title
    python scripts/fetch_confluence.py 123456
    python scripts/fetch_confluence.py --search "style guide"
"""

import os
import sys
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv
from markdownify import markdownify as md

# Load environment variables from .env file
# Check multiple locations: .docs-agent/.env (shared), skill-specific, then project root
script_dir = Path(__file__).parent
skill_dir = script_dir.parent
docs_agent_dir = skill_dir.parent.parent

env_locations = [
    docs_agent_dir / '.env',           # Shared .docs-agent/.env
    skill_dir / '.env',                 # Skill-specific .env
    Path.cwd() / '.env',                # Project root .env
]

env_loaded = False
for env_path in env_locations:
    if env_path.exists():
        load_dotenv(env_path)
        env_loaded = True
        break

if not env_loaded:
    load_dotenv()  # Fallback to default behavior

CONFLUENCE_BASE_URL = os.getenv('CONFLUENCE_BASE_URL')
CONFLUENCE_EMAIL = os.getenv('CONFLUENCE_EMAIL')
CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')

# Validate credentials
if not all([CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN]):
    print("Error: Missing Confluence credentials in .env file", file=sys.stderr)
    print("Required variables: CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN", file=sys.stderr)
    sys.exit(1)


class ConfluenceClient:
    """Client for interacting with Confluence REST API."""

    def __init__(self, base_url, email, api_token):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def extract_page_id_from_url(self, url):
        """Extract page ID from Confluence URL."""
        # Example URL: https://snyksec.atlassian.net/wiki/spaces/DOC/pages/123456/Page+Title
        parts = urlparse(url)
        path_parts = parts.path.split('/')

        try:
            pages_index = path_parts.index('pages')
            if pages_index + 1 < len(path_parts):
                page_id = path_parts[pages_index + 1]
                return page_id
        except (ValueError, IndexError):
            pass

        return None

    def get_page_content(self, page_id):
        """Fetch page content by ID."""
        api_url = f"{self.base_url}/rest/api/content/{page_id}"
        params = {
            'expand': 'body.storage,body.view,version,space,history'
        }

        try:
            response = self.session.get(api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_id}: {e}", file=sys.stderr)
            return None

    def search_content(self, query, limit=10):
        """Search for content in Confluence."""
        api_url = f"{self.base_url}/rest/api/content/search"
        params = {
            'cql': f'text ~ "{query}"',
            'limit': limit,
            'expand': 'space,history.lastUpdated'
        }

        try:
            response = self.session.get(api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching for '{query}': {e}", file=sys.stderr)
            return None

    def format_page_content(self, page_data, as_markdown=True):
        """Format page content for display.

        Args:
            page_data: The Confluence page data
            as_markdown: If True, convert HTML to Markdown (default: True)
        """
        if not page_data:
            return None

        output = []
        output.append(f"# {page_data.get('title', 'Untitled')}")
        output.append("")
        output.append(f"**Space:** {page_data.get('space', {}).get('name', 'Unknown')}")
        output.append(f"**Page ID:** {page_data.get('id', 'Unknown')}")

        version_info = page_data.get('version', {})
        output.append(f"**Version:** {version_info.get('number', 'Unknown')}")

        history = page_data.get('history', {})
        last_updated = history.get('lastUpdated', {})
        if last_updated:
            output.append(f"**Last Updated:** {last_updated.get('when', 'Unknown')} by {last_updated.get('by', {}).get('displayName', 'Unknown')}")

        output.append("")
        output.append("---")
        output.append("")

        # Get the body content (prefer view format, fallback to storage)
        body = page_data.get('body', {})
        content = body.get('view', {}).get('value') or body.get('storage', {}).get('value', '')

        if content:
            output.append("## Content")
            output.append("")

            # Convert HTML to Markdown if requested
            if as_markdown:
                # Convert HTML to Markdown
                markdown_content = md(content, heading_style="ATX", bullets="-")
                output.append(markdown_content)
            else:
                output.append(content)
        else:
            output.append("*No content available*")

        return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Fetch content from Confluence',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'identifier',
        nargs='?',
        help='Page URL or Page ID'
    )
    parser.add_argument(
        '--search', '-s',
        help='Search query'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=10,
        help='Number of search results to return (default: 10)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON instead of formatted text'
    )
    parser.add_argument(
        '--html',
        action='store_true',
        help='Output HTML instead of Markdown (default is Markdown)'
    )

    args = parser.parse_args()

    # Create Confluence client
    client = ConfluenceClient(CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)

    # Search mode
    if args.search:
        results = client.search_content(args.search, limit=args.limit)

        if not results:
            print("No results found or error occurred", file=sys.stderr)
            sys.exit(1)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"# Search Results for '{args.search}'")
            print(f"Found {results.get('size', 0)} results:")
            print()

            for result in results.get('results', []):
                title = result.get('title', 'Untitled')
                page_id = result.get('id', 'Unknown')
                space = result.get('space', {}).get('name', 'Unknown')
                url = f"{CONFLUENCE_BASE_URL}/spaces/{result.get('space', {}).get('key', '')}/pages/{page_id}"

                print(f"- **{title}**")
                print(f"  - Space: {space}")
                print(f"  - ID: {page_id}")
                print(f"  - URL: {url}")
                print()

        sys.exit(0)

    # Page fetch mode
    if not args.identifier:
        parser.print_help()
        sys.exit(1)

    # Determine if identifier is a URL or page ID
    page_id = args.identifier
    if args.identifier.startswith('http'):
        page_id = client.extract_page_id_from_url(args.identifier)
        if not page_id:
            print(f"Error: Could not extract page ID from URL: {args.identifier}", file=sys.stderr)
            sys.exit(1)

    # Fetch page content
    page_data = client.get_page_content(page_id)

    if not page_data:
        print(f"Error: Could not fetch page with ID: {page_id}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(page_data, indent=2))
    else:
        # Convert to Markdown by default, unless --html flag is used
        as_markdown = not args.html
        formatted = client.format_page_content(page_data, as_markdown=as_markdown)
        if formatted:
            print(formatted)
        else:
            print("Error formatting page content", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
