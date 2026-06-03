// Canonical path predicates for user-docs pages that the pipeline must treat specially.
// Paths are normalized: leading slash stripped, lowercased, trailing ".md" removed.

export function normalizePath(p: string): string {
  return p
    .trim()
    .replace(/^\/+/, '')
    .replace(/\.md$/i, '')
    .toLowerCase();
}

const CLI_COMMANDS_PREFIX = 'developer-tools/snyk-cli/commands/';
const CLI_COMMANDS_SUMMARY = 'developer-tools/snyk-cli/cli-commands-and-options-summary';
const CLI_GETTING_STARTED = 'developer-tools/snyk-cli/getting-started-with-the-snyk-cli';

// Top-level IDE plugin/extension pages synced to each plugin repo README.
// These are the README (folder root) page of each IDE plugin folder under developer-tools.
const IDE_PLUGIN_DIRS = [
  'developer-tools/snyk-ide-plugins-and-extensions/eclipse-plugin',
  'developer-tools/snyk-ide-plugins-and-extensions/jetbrains-plugin',
  'developer-tools/snyk-ide-plugins-and-extensions/visual-studio-extension',
  'developer-tools/snyk-ide-plugins-and-extensions/visual-studio-code-extension',
];

const IDE_COMPAT_MATRIX =
  'developer-tools/snyk-ide-plugins-and-extensions/compatibility-matrix';

// CLI-help pages: per-command pages + the commands/options summary. These follow the
// CLI Help command template and are pulled into each CLI release.
export function isCliHelpPath(path: string): boolean {
  const p = normalizePath(path);
  return p.startsWith(CLI_COMMANDS_PREFIX) || p === CLI_COMMANDS_SUMMARY;
}

// Pages synced to the cli repo (CLI help + the Getting started README).
export function isSyncedToCliRepo(path: string): boolean {
  const p = normalizePath(path);
  return isCliHelpPath(path) || p === CLI_GETTING_STARTED;
}

// Top-level IDE plugin/extension README pages synced to plugin repos.
// GitBook represents a folder's top page as either the bare folder path or "<folder>/readme".
export function isTopLevelIdePage(path: string): boolean {
  const p = normalizePath(path);
  return IDE_PLUGIN_DIRS.some((base) => p === base || p === `${base}/readme`);
}

// The IDE plugin compatibility matrix — owned by automation; never edit.
export function isCompatMatrix(path: string): boolean {
  return normalizePath(path) === IDE_COMPAT_MATRIX;
}

// Returns the parent directory of a normalized path, or '' for a top-level page.
export function parentDir(path: string): string {
  const p = normalizePath(path);
  const idx = p.lastIndexOf('/');
  return idx === -1 ? '' : p.slice(0, idx);
}
