#!/usr/bin/env python3
"""
Fetch content from Google Docs using the Google Docs API.

Usage:
    python scripts/fetch_google_docs.py <document_url_or_id>
    python scripts/fetch_google_docs.py --auth  # Setup authentication

Examples:
    python scripts/fetch_google_docs.py https://docs.google.com/document/d/1ABC123/edit
    python scripts/fetch_google_docs.py 1ABC123
    python scripts/fetch_google_docs.py --auth

Prerequisites:
    1. Enable Google Docs API in Google Cloud Console
    2. Create OAuth 2.0 credentials (Desktop application)
    3. Add credentials to .env file (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    4. Run with --auth flag to authenticate (first time only)
"""

import os
import sys
import json
import argparse
import pickle
import ssl
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import httplib2

# Paths
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DOCS_AGENT_DIR = SKILL_DIR.parent
PROJECT_ROOT = DOCS_AGENT_DIR.parent

# Load environment variables from .env file
# Check multiple locations: .docs-agent/.env (shared), skill-specific, then project root
env_locations = [
    DOCS_AGENT_DIR / '.env',           # Shared .docs-agent/.env
    SKILL_DIR / '.env',                 # Skill-specific .env
    PROJECT_ROOT / '.env',              # Project root .env
]

env_loaded = False
for env_path in env_locations:
    if env_path.exists():
        load_dotenv(env_path)
        env_loaded = True
        break

if not env_loaded:
    load_dotenv()  # Fallback to default behavior

# Define scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents.readonly'
]
TOKEN_FILE = DOCS_AGENT_DIR / 'token.pickle'

# Get Google OAuth credentials from environment
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')


class GoogleDocsClient:
    """Client for interacting with Google Docs API."""

    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google API using OAuth 2.0."""
        # Validate environment variables
        if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET]):
            print("Error: Missing Google OAuth credentials in .env file", file=sys.stderr)
            print("Required variables: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET", file=sys.stderr)
            print("\nSetup Instructions:", file=sys.stderr)
            print("1. Go to Google Cloud Console: https://console.cloud.google.com/", file=sys.stderr)
            print("2. Create a new project or select existing one", file=sys.stderr)
            print("3. Enable Google Docs API and Google Drive API", file=sys.stderr)
            print("4. Create OAuth 2.0 credentials (Desktop application)", file=sys.stderr)
            print("5. Add credentials to .env file:", file=sys.stderr)
            print("   GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com", file=sys.stderr)
            print("   GOOGLE_CLIENT_SECRET=your_client_secret", file=sys.stderr)
            print("6. Run: python scripts/fetch_google_docs.py --auth", file=sys.stderr)
            sys.exit(1)

        # Check if token.pickle exists
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)

        # If credentials don't exist or are invalid, authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}", file=sys.stderr)
                    print("Please re-authenticate using --auth flag", file=sys.stderr)
                    sys.exit(1)
            else:
                # Create OAuth client config from environment variables
                client_config = {
                    "installed": {
                        "client_id": GOOGLE_CLIENT_ID,
                        "client_secret": GOOGLE_CLIENT_SECRET,
                        "project_id": GOOGLE_PROJECT_ID or "default-project",
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": ["http://localhost"]
                    }
                }

                try:
                    flow = InstalledAppFlow.from_client_config(
                        client_config, SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}", file=sys.stderr)
                    sys.exit(1)

            # Save credentials for future use
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)

        # Build the service with custom HTTP client that respects SSL_CERT_FILE
        try:
            # Create HTTP client with SSL certificate verification
            # Get the SSL certificate file from environment or use system default
            cert_file = os.getenv('SSL_CERT_FILE') or ssl.get_default_verify_paths().cafile
            if cert_file and os.path.exists(cert_file):
                http = httplib2.Http(ca_certs=cert_file)
            else:
                http = httplib2.Http()

            # Authorize the HTTP client
            from google_auth_httplib2 import AuthorizedHttp
            authorized_http = AuthorizedHttp(self.creds, http=http)

            self.service = build('docs', 'v1', http=authorized_http)
        except Exception as e:
            print(f"Error building Google Docs service: {e}", file=sys.stderr)
            sys.exit(1)

    def extract_document_id_from_url(self, url):
        """Extract document ID from Google Docs URL."""
        # Example URL: https://docs.google.com/document/d/1ABC123/edit
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.split('/')

            # Find 'd' in path and get the next segment
            if 'd' in path_parts:
                d_index = path_parts.index('d')
                if d_index + 1 < len(path_parts):
                    return path_parts[d_index + 1]
        except Exception:
            pass

        return None

    def get_document(self, document_id):
        """Fetch document content by ID."""
        try:
            document = self.service.documents().get(documentId=document_id).execute()
            return document
        except HttpError as e:
            print(f"Error fetching document {document_id}: {e}", file=sys.stderr)
            return None

    def convert_to_markdown(self, document):
        """Convert Google Docs document to Markdown.

        This is a basic converter. For complex documents, you may need more sophisticated conversion.
        """
        if not document:
            return None

        output = []
        title = document.get('title', 'Untitled')
        output.append(f"# {title}")
        output.append("")

        # Get document body
        body = document.get('body', {})
        content = body.get('content', [])

        for element in content:
            output.extend(self._process_element(element))

        return '\n'.join(output)

    def _process_element(self, element, level=0):
        """Process a single document element."""
        output = []

        # Process paragraph
        if 'paragraph' in element:
            paragraph = element['paragraph']
            elements = paragraph.get('elements', [])

            # Check for heading
            paragraph_style = paragraph.get('paragraphStyle', {})
            named_style_type = paragraph_style.get('namedStyleType', '')

            # Convert heading levels
            if named_style_type.startswith('HEADING_'):
                try:
                    heading_level = int(named_style_type.split('_')[1])
                    heading_text = self._extract_text(elements)
                    output.append(f"{'#' * heading_level} {heading_text}")
                    output.append("")
                except (IndexError, ValueError):
                    text = self._extract_text(elements)
                    if text:
                        output.append(text)
                        output.append("")
            else:
                text = self._extract_text(elements)
                if text:
                    output.append(text)
                    output.append("")

        # Process table
        elif 'table' in element:
            table = element['table']
            output.extend(self._process_table(table))

        # Process table of contents
        elif 'tableOfContents' in element:
            output.append("<!-- Table of Contents -->")
            output.append("")

        return output

    def _extract_text(self, elements):
        """Extract text from paragraph elements."""
        text_parts = []

        for elem in elements:
            if 'textRun' in elem:
                content = elem['textRun'].get('content', '')
                text_style = elem['textRun'].get('textStyle', {})

                # Apply formatting
                if text_style.get('bold'):
                    content = f"**{content}**"
                if text_style.get('italic'):
                    content = f"*{content}*"
                if text_style.get('underline'):
                    content = f"__{content}__"

                # Handle links
                if 'link' in text_style:
                    url = text_style['link'].get('url', '')
                    content = f"[{content}]({url})"

                text_parts.append(content)

        return ''.join(text_parts).strip()

    def _process_table(self, table):
        """Process a table element."""
        output = []
        rows = table.get('tableRows', [])

        if not rows:
            return output

        # Process header row
        header_row = rows[0]
        header_cells = header_row.get('tableCells', [])
        header = []
        for cell in header_cells:
            cell_content = self._extract_cell_content(cell)
            header.append(cell_content)

        if header:
            output.append('| ' + ' | '.join(header) + ' |')
            output.append('| ' + ' | '.join(['---'] * len(header)) + ' |')

        # Process data rows
        for row in rows[1:]:
            cells = row.get('tableCells', [])
            row_data = []
            for cell in cells:
                cell_content = self._extract_cell_content(cell)
                row_data.append(cell_content)

            if row_data:
                output.append('| ' + ' | '.join(row_data) + ' |')

        output.append("")
        return output

    def _extract_cell_content(self, cell):
        """Extract content from a table cell."""
        content = cell.get('content', [])
        text_parts = []

        for element in content:
            if 'paragraph' in element:
                elements = element['paragraph'].get('elements', [])
                text = self._extract_text(elements)
                if text:
                    text_parts.append(text)

        return ' '.join(text_parts).strip()


def main():
    parser = argparse.ArgumentParser(
        description='Fetch content from Google Docs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'identifier',
        nargs='?',
        help='Document URL or Document ID'
    )
    parser.add_argument(
        '--auth',
        action='store_true',
        help='Authenticate with Google (first-time setup)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON instead of Markdown'
    )

    args = parser.parse_args()

    # Create Google Docs client (this will handle authentication)
    client = GoogleDocsClient()

    # If --auth flag, just authenticate and exit
    if args.auth:
        print("Authentication successful!", file=sys.stderr)
        print(f"Token saved to: {TOKEN_FILE}", file=sys.stderr)
        sys.exit(0)

    # Require document identifier
    if not args.identifier:
        parser.print_help()
        sys.exit(1)

    # Determine if identifier is a URL or document ID
    document_id = args.identifier
    if args.identifier.startswith('http'):
        document_id = client.extract_document_id_from_url(args.identifier)
        if not document_id:
            print(f"Error: Could not extract document ID from URL: {args.identifier}", file=sys.stderr)
            sys.exit(1)

    # Fetch document
    document = client.get_document(document_id)

    if not document:
        print(f"Error: Could not fetch document with ID: {document_id}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(document, indent=2))
    else:
        markdown = client.convert_to_markdown(document)
        if markdown:
            print(markdown)
        else:
            print("Error converting document to Markdown", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
