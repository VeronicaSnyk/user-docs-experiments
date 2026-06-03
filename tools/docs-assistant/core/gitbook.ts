// Headless GitBook client. Creates a Change Request (draft) and writes pages into it.
//
// Differences from the browser service (services/gitbookService.ts):
//   - No public CORS proxy: server-side fetch talks to api.gitbook.com directly.
//   - No hardcoded API token: the token is passed in (from a secret).

import type { PageUpdate } from '../types.ts';

const GITBOOK_API_BASE = 'https://api.gitbook.com/v1';

export interface CreateDraftInput {
  apiToken: string;
  spaceId: string;
  subject: string; // Change Request title
  updates: PageUpdate[];
}

export interface CreateDraftResult {
  changeRequestId: string;
  url: string; // CR diff URL
}

function authHeaders(apiToken: string): Record<string, string> {
  return {
    Authorization: `Bearer ${apiToken}`,
    'Content-Type': 'application/json',
    Accept: 'application/json',
  };
}

function findPageId(pages: any[], targetPath: string): string | undefined {
  if (!Array.isArray(pages)) return undefined;
  const target = targetPath.replace(/^\/+/, '').replace(/\.md$/i, '').toLowerCase();
  for (const page of pages) {
    if (page.path?.toLowerCase() === target) return page.id;
    if (page.pages) {
      const found = findPageId(page.pages, targetPath);
      if (found) return found;
    }
  }
  return undefined;
}

export async function createDraft(input: CreateDraftInput): Promise<CreateDraftResult> {
  const { apiToken, spaceId, subject, updates } = input;
  if (!apiToken || !spaceId || updates.length === 0) {
    throw new Error('Missing required data for GitBook draft (apiToken, spaceId, updates).');
  }
  const headers = authHeaders(apiToken);

  // 1. Validate space access.
  const spaceRes = await fetch(`${GITBOOK_API_BASE}/spaces/${spaceId}`, { headers });
  if (!spaceRes.ok) {
    throw new Error(`GitBook space access error: ${spaceRes.status} ${spaceRes.statusText}`);
  }

  // 2. Create the Change Request.
  const crRes = await fetch(`${GITBOOK_API_BASE}/spaces/${spaceId}/change-requests`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ subject }),
  });
  if (!crRes.ok) {
    const errData = await crRes.json().catch(() => ({}));
    throw new Error(`CR creation failed: ${errData?.error?.message || crRes.statusText}`);
  }
  const crData = await crRes.json();
  const changeRequestId: string = crData.id;

  // 3. Fetch current content for page mapping (best effort).
  let contentData: { pages: any[] } = { pages: [] };
  const contentRes = await fetch(`${GITBOOK_API_BASE}/spaces/${spaceId}/content`, { headers });
  if (contentRes.ok) {
    contentData = await contentRes.json();
  }

  // 4. Write each page into the CR. Update in place if the page exists; otherwise import.
  const crHeaders = { ...headers, 'X-GitBook-Change-Request': changeRequestId };
  for (const update of updates) {
    const pageId = findPageId(contentData.pages, update.path);

    if (pageId) {
      const pageInfoRes = await fetch(
        `${GITBOOK_API_BASE}/spaces/${spaceId}/content/page/${pageId}`,
        { headers },
      );
      if (pageInfoRes.ok) {
        const pageInfo = await pageInfoRes.json();
        const docId = pageInfo.document?.id;
        if (docId) {
          await fetch(`${GITBOOK_API_BASE}/spaces/${spaceId}/content/document/${docId}`, {
            method: 'PATCH',
            headers: crHeaders,
            body: JSON.stringify({ markdown: update.content }),
          });
          continue;
        }
      }
    }

    const importBody: Record<string, unknown> = { format: 'markdown', content: update.content };
    if (pageId) importBody.pageId = pageId;
    await fetch(`${GITBOOK_API_BASE}/spaces/${spaceId}/import`, {
      method: 'POST',
      headers: crHeaders,
      body: JSON.stringify(importBody),
    });
  }

  // 5. Build the reviewable diff URL.
  let url: string =
    crData.urls?.app || `https://app.gitbook.com/s/${spaceId}/~/changes/${changeRequestId}`;
  url = url.replace(/\/+$/, '');
  if (!url.endsWith('/diff')) url += '/diff';

  return { changeRequestId, url };
}
