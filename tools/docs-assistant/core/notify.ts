// Outbound notifications: post the draft URL and guardrail outcomes back to Slack, and append
// a comment to the ship-it-created Jira ticket. Both are best-effort and no-op when the relevant
// secrets are absent (so local dry runs and partial configs don't fail the pipeline).

import type { ClassificationSummary } from './guardrails.ts';

export interface NotifyContext {
  draftUrl: string;
  spaceLabel: string;
  summary: ClassificationSummary;
  requester?: string;
  slackChannel?: string;
  jiraIssueKey?: string;
}

// Build a human-readable summary of the run, shared by Slack and Jira.
export function buildMessage(ctx: NotifyContext): string {
  const lines: string[] = [];
  lines.push(`Snyk docs draft created in *${ctx.spaceLabel}*: ${ctx.draftUrl}`);

  const drafted = ctx.summary.pushable.map((c) => c.path);
  if (drafted.length) lines.push(`\nDrafted ${drafted.length} page(s):`);
  for (const c of ctx.summary.pushable) {
    const flag = c.verdict === 'NEEDS_TEAM_APPROVAL' ? `  ⚠️ requires ${c.team} approval (typos/formatting only)` : '';
    lines.push(`  • ${c.path}${flag}`);
  }

  if (ctx.summary.rejected.length) {
    lines.push(`\nNot drafted — path-locked (synced page, cannot rename/create):`);
    for (const c of ctx.summary.rejected) lines.push(`  • ${c.path} — ${c.reason}`);
  }
  if (ctx.summary.blocked.length) {
    lines.push(`\nBlocked — automation-owned, not editable:`);
    for (const c of ctx.summary.blocked) lines.push(`  • ${c.path}`);
  }
  return lines.join('\n');
}

export async function postToSlack(ctx: NotifyContext): Promise<void> {
  const token = process.env.SLACK_BOT_TOKEN;
  if (!token || !ctx.slackChannel) {
    console.log('[notify] Slack skipped (no SLACK_BOT_TOKEN or channel).');
    return;
  }
  const res = await fetch('https://slack.com/api/chat.postMessage', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ channel: ctx.slackChannel, text: buildMessage(ctx) }),
  });
  const data = await res.json().catch(() => ({}));
  if (!data.ok) console.warn(`[notify] Slack post failed: ${data.error || res.status}`);
}

export async function commentOnJira(ctx: NotifyContext): Promise<void> {
  const { JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN } = process.env;
  if (!JIRA_BASE_URL || !JIRA_EMAIL || !JIRA_API_TOKEN || !ctx.jiraIssueKey) {
    console.log('[notify] Jira skipped (missing Jira secrets or issue key).');
    return;
  }
  const auth = Buffer.from(`${JIRA_EMAIL}:${JIRA_API_TOKEN}`).toString('base64');
  const res = await fetch(`${JIRA_BASE_URL}/rest/api/3/issue/${ctx.jiraIssueKey}/comment`, {
    method: 'POST',
    headers: { Authorization: `Basic ${auth}`, 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({
      body: {
        type: 'doc',
        version: 1,
        content: [
          { type: 'paragraph', content: [{ type: 'text', text: `GitBook draft: ` }, { type: 'text', text: ctx.draftUrl, marks: [{ type: 'link', attrs: { href: ctx.draftUrl } }] }] },
          { type: 'paragraph', content: [{ type: 'text', text: buildMessage(ctx) }] },
        ],
      },
    }),
  });
  if (!res.ok) console.warn(`[notify] Jira comment failed: ${res.status} ${res.statusText}`);
}
