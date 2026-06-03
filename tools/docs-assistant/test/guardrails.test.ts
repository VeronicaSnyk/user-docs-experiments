import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  isCliHelpPath,
  isSyncedToCliRepo,
  isTopLevelIdePage,
  isCompatMatrix,
  normalizePath,
} from '../core/paths.ts';
import { classifyPage } from '../core/guardrails.ts';
import type { DocumentationPage } from '../types.ts';

function page(path: string, isNew = false): DocumentationPage {
  return { path, isNew, content: '# x', reason: 'test' };
}

test('normalizePath strips slash, .md, lowercases', () => {
  assert.equal(normalizePath('/Developer-Tools/Snyk-CLI/commands/Test.md'), 'developer-tools/snyk-cli/commands/test');
});

test('isCliHelpPath matches command pages and the summary', () => {
  assert.ok(isCliHelpPath('developer-tools/snyk-cli/commands/test.md'));
  assert.ok(isCliHelpPath('developer-tools/snyk-cli/commands/code-test.md'));
  assert.ok(isCliHelpPath('developer-tools/snyk-cli/cli-commands-and-options-summary.md'));
  assert.ok(!isCliHelpPath('developer-tools/snyk-cli/getting-started-with-the-snyk-cli.md'));
  assert.ok(!isCliHelpPath('discover-snyk/getting-started/README.md'));
});

test('isSyncedToCliRepo includes CLI help and the getting-started README', () => {
  assert.ok(isSyncedToCliRepo('developer-tools/snyk-cli/commands/monitor.md'));
  assert.ok(isSyncedToCliRepo('developer-tools/snyk-cli/getting-started-with-the-snyk-cli.md'));
  assert.ok(!isSyncedToCliRepo('developer-tools/snyk-cli/debugging-the-snyk-cli.md'));
});

test('isTopLevelIdePage matches plugin folder roots and READMEs', () => {
  assert.ok(isTopLevelIdePage('developer-tools/snyk-ide-plugins-and-extensions/eclipse-plugin'));
  assert.ok(isTopLevelIdePage('developer-tools/snyk-ide-plugins-and-extensions/eclipse-plugin/README.md'));
  assert.ok(isTopLevelIdePage('developer-tools/snyk-ide-plugins-and-extensions/visual-studio-code-extension/readme'));
  // A sub-page of a plugin is NOT a top-level synced page.
  assert.ok(!isTopLevelIdePage('developer-tools/snyk-ide-plugins-and-extensions/eclipse-plugin/configuration-of-the-eclipse-plugin.md'));
});

test('isCompatMatrix matches only the matrix page', () => {
  assert.ok(isCompatMatrix('developer-tools/snyk-ide-plugins-and-extensions/compatibility-matrix.md'));
  assert.ok(!isCompatMatrix('developer-tools/snyk-ide-plugins-and-extensions/eclipse-plugin/README.md'));
});

test('classifyPage: compatibility matrix -> BLOCKED', () => {
  const c = classifyPage(page('developer-tools/snyk-ide-plugins-and-extensions/compatibility-matrix.md'));
  assert.equal(c.verdict, 'BLOCKED');
});

test('classifyPage: in-place CLI help update -> NEEDS_TEAM_APPROVAL (Team CLI), isCliHelp true', () => {
  const c = classifyPage(page('developer-tools/snyk-cli/commands/test.md', false));
  assert.equal(c.verdict, 'NEEDS_TEAM_APPROVAL');
  assert.equal(c.team, 'Team CLI');
  assert.equal(c.isCliHelp, true);
});

test('classifyPage: top-level IDE README update -> NEEDS_TEAM_APPROVAL (Team IDE)', () => {
  const c = classifyPage(page('developer-tools/snyk-ide-plugins-and-extensions/jetbrains-plugin/README.md', false));
  assert.equal(c.verdict, 'NEEDS_TEAM_APPROVAL');
  assert.equal(c.team, 'Team IDE');
});

test('classifyPage: NEW synced page (slug rename/create) -> PATH_LOCKED', () => {
  const c = classifyPage(page('developer-tools/snyk-cli/commands/brand-new-command.md', true));
  assert.equal(c.verdict, 'PATH_LOCKED');
  assert.equal(c.team, 'Team CLI');
});

test('classifyPage: synced update not in existingPaths -> PATH_LOCKED', () => {
  const existing = new Set<string>(); // page not known to exist => treated as a path change
  const c = classifyPage(page('developer-tools/snyk-cli/commands/test.md', false), existing);
  assert.equal(c.verdict, 'PATH_LOCKED');
});

test('classifyPage: synced update present in existingPaths -> NEEDS_TEAM_APPROVAL', () => {
  const existing = new Set<string>(['developer-tools/snyk-cli/commands/test']);
  const c = classifyPage(page('developer-tools/snyk-cli/commands/test.md', false), existing);
  assert.equal(c.verdict, 'NEEDS_TEAM_APPROVAL');
});

test('classifyPage: ordinary page -> OK, isCliHelp false', () => {
  const c = classifyPage(page('developer-tools/snyk-cli/debugging-the-snyk-cli.md', false));
  assert.equal(c.verdict, 'OK');
  assert.equal(c.isCliHelp, false);
});

test('classifyPage: brand-new ordinary page -> OK (only synced pages are path-locked)', () => {
  const c = classifyPage(page('scan-fix-and-prevent/some-new-feature.md', true));
  assert.equal(c.verdict, 'OK');
});
