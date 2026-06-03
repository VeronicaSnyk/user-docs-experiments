import { GitBookMetadata } from '../types';

// Browser variant of the GitBook push. Uses a CORS proxy because the GitBook API does not send
// CORS headers for browser origins. The API token is supplied at runtime via the modal — it is
// NEVER hardcoded here. The headless pipeline (core/gitbook.ts) talks to the API directly.
const GITBOOK_API_BASE = 'https://api.gitbook.com/v1';
const CORS_PROXY = 'https://corsproxy.io/?';

export const pushToGitBook = async (metadata: GitBookMetadata): Promise<string> => {
  const { commitMessage, apiKey, spaceId, updates } = metadata;

  if (!apiKey || !spaceId || updates.length === 0) {
    throw new Error('Missing required data for GitBook push.');
  }

  const headers = {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
    Accept: 'application/json',
  };

  const fetchWithProxy = (url: string, options: RequestInit) =>
    fetch(`${CORS_PROXY}${encodeURIComponent(url)}`, options);

  const spaceRes = await fetchWithProxy(`${GITBOOK_API_BASE}/spaces/${spaceId}`, { headers });
  if (!spaceRes.ok) {
    throw new Error(`GitBook Space Access Error: ${spaceRes.status}`);
  }

  const crRes = await fetchWithProxy(`${GITBOOK_API_BASE}/spaces/${spaceId}/change-requests`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ subject: commitMessage }),
  });
  if (!crRes.ok) {
    const errData = await crRes.json().catch(() => ({}));
    throw new Error(`CR Creation Failed: ${errData?.error?.message || crRes.statusText}`);
  }
  const crData = await crRes.json();
  const changeRequestId = crData.id;

  let contentData: { pages: any[] } = { pages: [] };
  try {
    const contentRes = await fetchWithProxy(`${GITBOOK_API_BASE}/spaces/${spaceId}/content`, { headers });
    if (contentRes.ok) contentData = await contentRes.json();
  } catch {
    console.warn('GitBook: Content mapping failed, using import fallback.');
  }

  const findPageId = (pages: any[], path: string): string | undefined => {
    if (!Array.isArray(pages)) return undefined;
    const target = path.replace(/^\//, '').replace(/\.md$/, '').toLowerCase();
    for (const page of pages) {
      if (page.path?.toLowerCase() === target) return page.id;
      if (page.pages) {
        const found = findPageId(page.pages, path);
        if (found) return found;
      }
    }
    return undefined;
  };

  for (const update of updates) {
    const pageId = findPageId(contentData.pages, update.path);
    const updateHeaders = { ...headers, 'X-GitBook-Change-Request': changeRequestId };

    if (pageId) {
      try {
        const pageInfoRes = await fetchWithProxy(`${GITBOOK_API_BASE}/spaces/${spaceId}/content/page/${pageId}`, { headers });
        if (pageInfoRes.ok) {
          const pageInfo = await pageInfoRes.json();
          const docId = pageInfo.document?.id;
          if (docId) {
            await fetchWithProxy(`${GITBOOK_API_BASE}/spaces/${spaceId}/content/document/${docId}`, {
              method: 'PATCH',
              headers: updateHeaders,
              body: JSON.stringify({ markdown: update.content }),
            });
            continue;
          }
        }
      } catch {
        console.warn(`GitBook: Patch failed for ${pageId}`);
      }
    }

    const importBody: any = { format: 'markdown', content: update.content };
    if (pageId) importBody.pageId = pageId;
    await fetchWithProxy(`${GITBOOK_API_BASE}/spaces/${spaceId}/import`, {
      method: 'POST',
      headers: updateHeaders,
      body: JSON.stringify(importBody),
    });
  }

  let finalUrl = crData.urls?.app || `https://app.gitbook.com/s/${spaceId}/~/changes/${changeRequestId}`;
  finalUrl = finalUrl.replace(/\/+$/, '');
  if (!finalUrl.endsWith('/diff')) finalUrl += '/diff';
  return finalUrl;
};
