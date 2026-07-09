#!/usr/bin/env python3
"""
Fetch ticket details from Jira using the Jira REST API.

Usage:
    python scripts/fetch_jira_ticket.py <ticket_key_or_url>

Examples:
    python scripts/fetch_jira_ticket.py DOC-123
    python scripts/fetch_jira_ticket.py https://your-org.atlassian.net/browse/DOC-123
"""

import os
import sys
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv

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

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

# Validate credentials
if not all([JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
    print("Error: Missing Jira credentials in .env file", file=sys.stderr)
    print("Required variables: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN", file=sys.stderr)
    sys.exit(1)


class JiraClient:
    """Client for interacting with Jira REST API."""

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

    def extract_ticket_key_from_url(self, url):
        """Extract ticket key from Jira URL."""
        # Example URL: https://your-org.atlassian.net/browse/DOC-123
        parts = urlparse(url)
        path_parts = parts.path.split('/')

        try:
            browse_index = path_parts.index('browse')
            if browse_index + 1 < len(path_parts):
                ticket_key = path_parts[browse_index + 1]
                return ticket_key.upper()
        except (ValueError, IndexError):
            pass

        return None

    def get_ticket(self, ticket_key):
        """Fetch ticket details by key."""
        api_url = f"{self.base_url}/rest/api/3/issue/{ticket_key}"
        params = {
            'expand': 'renderedFields,names,schema,transitions,changelog'
        }

        try:
            response = self.session.get(api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ticket {ticket_key}: {e}", file=sys.stderr)
            return None

    def get_ticket_comments(self, ticket_key):
        """Fetch all comments for a ticket."""
        api_url = f"{self.base_url}/rest/api/3/issue/{ticket_key}/comment"

        try:
            response = self.session.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching comments for {ticket_key}: {e}", file=sys.stderr)
            return None

    def format_ticket(self, ticket_data):
        """Format ticket data for display.

        Args:
            ticket_data: The Jira ticket data
        """
        if not ticket_data:
            return None

        fields = ticket_data.get('fields', {})
        key = ticket_data.get('key', 'Unknown')

        output = []
        output.append(f"# {key}: {fields.get('summary', 'Untitled')}")
        output.append("")
        output.append(f"**URL:** {self.base_url}/browse/{key}")
        output.append(f"**Status:** {fields.get('status', {}).get('name', 'Unknown')}")
        output.append(f"**Priority:** {fields.get('priority', {}).get('name', 'Unknown')}")

        reporter = fields.get('reporter', {})
        if reporter:
            output.append(f"**Reporter:** {reporter.get('displayName', 'Unknown')}")

        assignee = fields.get('assignee', {})
        if assignee:
            output.append(f"**Assignee:** {assignee.get('displayName', 'Unassigned')}")

        # Labels
        labels = fields.get('labels', [])
        if labels:
            output.append(f"**Labels:** {', '.join(labels)}")

        # Components
        components = fields.get('components', [])
        if components:
            comp_names = [c.get('name', '') for c in components]
            output.append(f"**Components:** {', '.join(comp_names)}")

        output.append("")
        output.append("---")
        output.append("")

        # Description
        description = fields.get('description')
        if description:
            output.append("## Description")
            output.append("")
            # Handle both old and new Jira description formats
            if isinstance(description, dict):
                # Atlassian Document Format (ADF)
                output.append(self._parse_adf(description))
            else:
                # Plain text or Wiki markup
                output.append(str(description))
            output.append("")

        # Attachments
        attachments = fields.get('attachment', [])
        if attachments:
            output.append("## Attachments")
            output.append("")
            for att in attachments:
                filename = att.get('filename', 'Unknown')
                size = att.get('size', 0)
                author = att.get('author', {}).get('displayName', 'Unknown')
                created = att.get('created', 'Unknown')
                url = att.get('content', '')
                output.append(f"- **{filename}** ({self._format_size(size)}) - uploaded by {author} on {created}")
                output.append(f"  - URL: {url}")
            output.append("")

        # Comments
        comments_data = self.get_ticket_comments(key)
        if comments_data and comments_data.get('comments'):
            output.append("## Comments")
            output.append("")
            for comment in comments_data.get('comments', []):
                author = comment.get('author', {}).get('displayName', 'Unknown')
                created = comment.get('created', 'Unknown')
                body = comment.get('body', {})

                output.append(f"### {author} - {created}")
                output.append("")

                # Handle ADF format for comments
                if isinstance(body, dict):
                    output.append(self._parse_adf(body))
                else:
                    output.append(str(body))
                output.append("")

        # Issue links
        issue_links = fields.get('issuelinks', [])
        if issue_links:
            output.append("## Related Tickets")
            output.append("")
            for link in issue_links:
                link_type = link.get('type', {}).get('name', 'Unknown')

                # Inward or outward issue
                related_issue = link.get('inwardIssue') or link.get('outwardIssue')
                if related_issue:
                    related_key = related_issue.get('key', '')
                    related_summary = related_issue.get('fields', {}).get('summary', '')
                    output.append(f"- **{link_type}**: [{related_key}]({self.base_url}/browse/{related_key}) - {related_summary}")
            output.append("")

        return '\n'.join(output)

    def _parse_adf(self, adf_content):
        """Parse Atlassian Document Format to plain text/markdown."""
        if not isinstance(adf_content, dict):
            return str(adf_content)

        # Simple ADF parser - extracts text from content blocks
        result = []

        def extract_text(node):
            if isinstance(node, dict):
                node_type = node.get('type', '')

                if node_type == 'text':
                    text = node.get('text', '')
                    # Apply marks (bold, italic, etc.)
                    marks = node.get('marks', [])
                    for mark in marks:
                        if mark.get('type') == 'strong':
                            text = f"**{text}**"
                        elif mark.get('type') == 'em':
                            text = f"*{text}*"
                        elif mark.get('type') == 'code':
                            text = f"`{text}`"
                    return text

                elif node_type == 'paragraph':
                    content = node.get('content', [])
                    return ''.join(extract_text(c) for c in content)

                elif node_type == 'heading':
                    level = node.get('attrs', {}).get('level', 1)
                    content = node.get('content', [])
                    text = ''.join(extract_text(c) for c in content)
                    return f"{'#' * level} {text}"

                elif node_type == 'bulletList' or node_type == 'orderedList':
                    items = node.get('content', [])
                    return '\n'.join(extract_text(item) for item in items)

                elif node_type == 'listItem':
                    content = node.get('content', [])
                    text = ''.join(extract_text(c) for c in content)
                    return f"- {text}"

                elif node_type == 'codeBlock':
                    content = node.get('content', [])
                    text = ''.join(extract_text(c) for c in content)
                    return f"```\n{text}\n```"

                # Recursively process content
                content = node.get('content', [])
                if content:
                    return '\n\n'.join(extract_text(c) for c in content)

            return ''

        return extract_text(adf_content)

    def _format_size(self, size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description='Fetch ticket details from Jira',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'identifier',
        help='Ticket key (DOC-123) or URL'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON instead of formatted text'
    )

    args = parser.parse_args()

    # Create Jira client
    client = JiraClient(JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN)

    # Determine if identifier is a URL or ticket key
    ticket_key = args.identifier.upper()
    if args.identifier.startswith('http'):
        ticket_key = client.extract_ticket_key_from_url(args.identifier)
        if not ticket_key:
            print(f"Error: Could not extract ticket key from URL: {args.identifier}", file=sys.stderr)
            sys.exit(1)

    # Fetch ticket data
    ticket_data = client.get_ticket(ticket_key)

    if not ticket_data:
        print(f"Error: Could not fetch ticket: {ticket_key}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(ticket_data, indent=2))
    else:
        formatted = client.format_ticket(ticket_data)
        if formatted:
            print(formatted)
        else:
            print("Error formatting ticket data", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
