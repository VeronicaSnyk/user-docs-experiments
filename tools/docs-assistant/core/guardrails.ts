// Guardrails: classify every planned page BEFORE any GitBook write.
//
// Source of truth: "Writing CLI and IDE documentation" (cli-style-rules.md). Several pages are
// synced to or from other repos and must not be freely rewritten by automation:
//   - IDE plugin compatibility matrix -> automation-owned, never edit (BLOCKED).
//   - CLI help, Getting started CLI, top-level IDE READMEs -> need owning-team approval, and
//     their source-file path must never change (renaming/new slug breaks the sync).

import type { DocumentationPage, PageClassification } from '../types.ts';
import {
  normalizePath,
  isCliHelpPath,
  isSyncedToCliRepo,
  isTopLevelIdePage,
  isCompatMatrix,
} from './paths.ts';

// A page is "synced" (path-locked + needs approval) if it is owned by another repo.
function isSyncedPage(path: string): boolean {
  return isSyncedToCliRepo(path) || isTopLevelIdePage(path);
}

/**
 * Classify a single planned page.
 *
 * - BLOCKED: compatibility matrix — drop entirely, never push.
 * - PATH_LOCKED: a synced page where the generator proposes a NEW page (new slug) — the source
 *   path must not change, so creating/renaming is rejected.
 * - NEEDS_TEAM_APPROVAL: a synced page being updated in place — generate the draft but flag the
 *   owning team and restrict to typos/formatting.
 * - OK: an ordinary page — push freely.
 *
 * `existingPaths`, when provided, is the set of normalized paths that already exist in the repo;
 * it lets us distinguish "update in place" (OK to draft, needs approval) from "rename/new slug"
 * (PATH_LOCKED) for synced pages.
 */
export function classifyPage(
  page: DocumentationPage,
  existingPaths?: Set<string>,
): PageClassification {
  const cliHelp = isCliHelpPath(page.path);
  const base = { path: page.path, isCliHelp: cliHelp };

  if (isCompatMatrix(page.path)) {
    return {
      ...base,
      verdict: 'BLOCKED',
      reason:
        'The IDE plugin compatibility matrix is owned by automation. Do not edit it in GitBook or in PRs.',
    };
  }

  if (isSyncedPage(page.path)) {
    const team = isTopLevelIdePage(page.path) ? 'Team IDE' : 'Team CLI';

    // A synced page must keep its source-file path. Creating a new synced page, or pointing at a
    // path that does not already exist, implies a path change that would break the sync.
    const known = existingPaths ? existingPaths.has(normalizePath(page.path)) : true;
    if (page.isNew || !known) {
      return {
        ...base,
        verdict: 'PATH_LOCKED',
        team,
        reason:
          `This page is synced to another repo, so its source-file path must not change. ` +
          `Creating or renaming it (proposed: "${page.path}") would break the sync. ` +
          `Coordinate with ${team}.`,
      };
    }

    return {
      ...base,
      verdict: 'NEEDS_TEAM_APPROVAL',
      team,
      reason:
        `This page is synced to another repo. Requires ${team} approval; limit changes to ` +
        `typos and formatting. Do not change the source-file path.`,
    };
  }

  return {
    ...base,
    verdict: 'OK',
    reason: 'Ordinary user-docs page.',
  };
}

export interface ClassificationSummary {
  pushable: PageClassification[]; // OK + NEEDS_TEAM_APPROVAL (drafted; approval flagged)
  blocked: PageClassification[]; // BLOCKED — dropped
  rejected: PageClassification[]; // PATH_LOCKED — dropped
  needsApproval: PageClassification[]; // subset of pushable
  all: PageClassification[];
}

// Classify a whole set of planned pages and bucket the verdicts.
export function classifyPages(
  pages: DocumentationPage[],
  existingPaths?: Set<string>,
): ClassificationSummary {
  const all = pages.map((p) => classifyPage(p, existingPaths));
  const pushable = all.filter(
    (c) => c.verdict === 'OK' || c.verdict === 'NEEDS_TEAM_APPROVAL',
  );
  return {
    all,
    pushable,
    blocked: all.filter((c) => c.verdict === 'BLOCKED'),
    rejected: all.filter((c) => c.verdict === 'PATH_LOCKED'),
    needsApproval: all.filter((c) => c.verdict === 'NEEDS_TEAM_APPROVAL'),
  };
}
