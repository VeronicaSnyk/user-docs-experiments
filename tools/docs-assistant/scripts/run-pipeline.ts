// Headless pipeline entrypoint, run by .github/workflows/docs-ship-it.yml on repository_dispatch
// (triggered by the Slack /ship-it Workflow Builder webhook step) or via workflow_dispatch.
//
//   generate (style guide + CLI rules)  ->  guardrails.classify  ->  GitBook draft  ->  notify
//
// Inputs come from CLI flags or, in CI, the GitHub event payload at $GITHUB_EVENT_PATH
// (client_payload: { spec, slidesUrl, space, requester, slackChannel, jiraIssueKey }).
//
// Usage:
//   node --experimental-strip-types scripts/run-pipeline.ts \
//     --spec "Feature: add --json to snyk code test" --space closed-beta [--dry-run]

import { readFile } from 'node:fs/promises';
import { generateDocumentation } from '../core/generate.ts';
import { classifyPages } from '../core/guardrails.ts';
import { createDraft } from '../core/gitbook.ts';
import { postToSlack, commentOnJira, buildMessage } from '../core/notify.ts';
import type { PageUpdate } from '../types.ts';

const SPACES: Record<string, { id: string; label: string }> = {
  'public': { id: '-MdwVZ6HOZriajCf5nXH', label: 'Public User Docs' },
  'closed-beta': { id: 'Y2VjeSnjL1hm69oRmP5s', label: 'Closed Beta Docs' },
};

interface Input {
  spec: string;
  slidesUrl?: string;
  space: string; // key or raw space id
  requester?: string;
  slackChannel?: string;
  jiraIssueKey?: string;
  dryRun: boolean;
}

function parseArgs(argv: string[]): Partial<Input> {
  const out: Record<string, string | boolean> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dry-run') out.dryRun = true;
    else if (a.startsWith('--')) {
      const key = a.slice(2);
      const val = argv[i + 1]?.startsWith('--') ? '' : argv[++i];
      out[key] = val ?? '';
    }
  }
  return out as Partial<Input>;
}

async function readGithubEvent(): Promise<Partial<Input>> {
  const p = process.env.GITHUB_EVENT_PATH;
  if (!p) return {};
  try {
    const event = JSON.parse(await readFile(p, 'utf8'));
    const cp = event.client_payload ?? {};
    return {
      spec: cp.spec,
      slidesUrl: cp.slidesUrl,
      space: cp.space,
      requester: cp.requester,
      slackChannel: cp.slackChannel,
      jiraIssueKey: cp.jiraIssueKey,
    };
  } catch {
    return {};
  }
}

function resolveSpace(space: string): { id: string; label: string } {
  if (SPACES[space]) return SPACES[space];
  // Treat as a raw space id.
  return { id: space, label: space };
}

async function main() {
  const fromEvent = await readGithubEvent();
  const fromArgs = parseArgs(process.argv.slice(2));
  const input: Input = {
    spec: fromArgs.spec ?? fromEvent.spec ?? '',
    slidesUrl: fromArgs.slidesUrl ?? fromEvent.slidesUrl,
    space: fromArgs.space ?? fromEvent.space ?? 'closed-beta',
    requester: fromArgs.requester ?? fromEvent.requester,
    slackChannel: fromArgs.slackChannel ?? fromEvent.slackChannel,
    jiraIssueKey: fromArgs.jiraIssueKey ?? fromEvent.jiraIssueKey,
    dryRun: Boolean(fromArgs.dryRun),
  };

  if (!input.spec.trim()) {
    throw new Error('No spec provided. Pass --spec "..." or a client_payload.spec.');
  }
  const space = resolveSpace(input.space);

  console.log(`[pipeline] Generating documentation for space "${space.label}"...`);
  const doc = await generateDocumentation({ prdText: input.spec, slidesUrl: input.slidesUrl });
  console.log(`[pipeline] Generated ${doc.pages.length} page(s).`);

  // Classify before any write. (existingPaths is left undefined here: without a repo snapshot we
  // treat synced updates as in-place; a synced page marked isNew is still rejected as PATH_LOCKED.)
  const summary = classifyPages(doc.pages);

  const pushablePaths = new Set(summary.pushable.map((c) => c.path));
  const updates: PageUpdate[] = doc.pages
    .filter((p) => pushablePaths.has(p.path))
    .map((p) => ({ path: p.path, content: p.content }));

  for (const c of summary.blocked) console.warn(`[pipeline] BLOCKED (dropped): ${c.path}`);
  for (const c of summary.rejected) console.warn(`[pipeline] PATH_LOCKED (dropped): ${c.path}`);
  for (const c of summary.needsApproval) console.log(`[pipeline] NEEDS ${c.team} APPROVAL: ${c.path}`);

  if (updates.length === 0) {
    console.log('[pipeline] Nothing pushable after guardrails. Exiting without creating a draft.');
    return;
  }

  if (input.dryRun) {
    console.log('[pipeline] --dry-run: skipping GitBook write and notifications.\n');
    console.log(buildMessage({ draftUrl: '(dry-run, no draft created)', spaceLabel: space.label, summary }));
    return;
  }

  const apiToken = process.env.GITBOOK_API_TOKEN;
  if (!apiToken) throw new Error('GITBOOK_API_TOKEN is not set.');

  const subject = `Docs draft: ${input.spec.slice(0, 80).replace(/\s+/g, ' ').trim()}`;
  const { url } = await createDraft({ apiToken, spaceId: space.id, subject, updates });
  console.log(`[pipeline] Draft created: ${url}`);

  const ctx = {
    draftUrl: url,
    spaceLabel: space.label,
    summary,
    requester: input.requester,
    slackChannel: input.slackChannel,
    jiraIssueKey: input.jiraIssueKey,
  };
  await postToSlack(ctx);
  await commentOnJira(ctx);

  // Expose the URL to later workflow steps.
  if (process.env.GITHUB_OUTPUT) {
    const { appendFile } = await import('node:fs/promises');
    await appendFile(process.env.GITHUB_OUTPUT, `draft_url=${url}\n`);
  }
}

main().catch((err) => {
  console.error('[pipeline] Failed:', err instanceof Error ? err.message : err);
  process.exit(1);
});
