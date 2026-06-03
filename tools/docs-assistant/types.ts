export interface DocumentationPage {
  path: string; // The suggested file path/slug
  content: string; // The markdown content (with <ins> tags if it's an update)
  reason: string; // Why this page is impacted
  isNew: boolean; // Whether it's a new page or an update
}

export interface GeneratedDocumentation {
  pages: DocumentationPage[];
}

export interface PageUpdate {
  path: string;
  content: string;
}

export interface GitBookMetadata {
  commitMessage: string;
  apiKey: string;
  spaceId: string;
  updates: PageUpdate[];
}

export interface FileData {
  base64: string;
  mimeType: string;
  name: string;
}

// ---- Pipeline (headless) types ----

export type GuardrailVerdict = 'OK' | 'NEEDS_TEAM_APPROVAL' | 'PATH_LOCKED' | 'BLOCKED';

export type OwningTeam = 'Team CLI' | 'Team IDE';

export interface PageClassification {
  path: string;
  verdict: GuardrailVerdict;
  team?: OwningTeam; // set for NEEDS_TEAM_APPROVAL
  isCliHelp: boolean; // CLI-help formatting rules apply
  reason: string; // human-readable explanation of the verdict
}

// A page after classification, carrying its verdict alongside the generated content.
export interface ClassifiedPage extends DocumentationPage {
  classification: PageClassification;
}
