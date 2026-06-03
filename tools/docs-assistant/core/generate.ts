// Headless documentation generation. Loads the authoritative Snyk style guide and the CLI/IDE
// supplemental rules from disk, then drives Gemini in two passes:
//   1. Plan the impacted pages (paths + reasons + content).
//   2. For pages that target CLI-help paths, re-condition the content with the CLI rules and the
//      command-page template enforced.
//
// Used by the GitHub Actions pipeline. The browser UI uses services/geminiService.ts instead
// (it cannot read the filesystem), but both share the same prompt templates in constants.ts.

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { GoogleGenAI, Type } from '@google/genai';
import type { Part } from '@google/genai';
import type { GeneratedDocumentation, DocumentationPage, FileData } from '../types.ts';
import {
  SYSTEM_INSTRUCTION_TEMPLATE,
  SNYK_DOC_EXAMPLES_BY_SECTION,
  CLI_RULES_TEMPLATE,
} from '../constants.ts';
import { isCliHelpPath } from './paths.ts';

const MODEL = process.env.GEMINI_MODEL || 'gemini-3-pro-preview';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STYLE_GUIDE_PATH = path.resolve(__dirname, '..', 'snyk-style-guide.md');
const CLI_RULES_PATH = path.resolve(__dirname, '..', 'cli-style-rules.md');

const responseSchema = {
  type: Type.OBJECT,
  properties: {
    pages: {
      type: Type.ARRAY,
      description: 'A list of documentation pages to be created or updated.',
      items: {
        type: Type.OBJECT,
        properties: {
          path: { type: Type.STRING, description: "Suggested file path/slug matching the user-docs repo layout." },
          content: { type: Type.STRING, description: 'The full Markdown content. Use <ins> tags for updates.' },
          reason: { type: Type.STRING, description: 'Why this page is impacted.' },
          isNew: { type: Type.BOOLEAN, description: 'True if creating a new page.' },
        },
        required: ['path', 'content', 'reason', 'isNew'],
      },
    },
  },
  required: ['pages'],
};

function buildExamples(): string {
  let examples = '';
  for (const [section, content] of Object.entries(SNYK_DOC_EXAMPLES_BY_SECTION)) {
    examples += `\n<example section="${section}">\n${content}\n</example>\n`;
  }
  return examples;
}

async function buildSystemInstruction(styleGuide: string): Promise<string> {
  return SYSTEM_INSTRUCTION_TEMPLATE
    .replace('{{STYLE_GUIDE}}', styleGuide)
    .replace('{{EXAMPLES}}', buildExamples());
}

function parsePages(responseText: string): DocumentationPage[] {
  const jsonString = responseText.trim().replace(/^```json\s*/, '').replace(/```\s*$/, '');
  const parsed = JSON.parse(jsonString);
  if (!parsed.pages || !Array.isArray(parsed.pages)) {
    throw new Error("AI response format invalid: missing 'pages' array.");
  }
  return parsed.pages as DocumentationPage[];
}

export interface GenerateInput {
  prdText: string;
  slidesUrl?: string;
  fileData?: FileData | null;
}

export async function generateDocumentation(input: GenerateInput): Promise<GeneratedDocumentation> {
  const apiKey = process.env.GEMINI_API_KEY || process.env.API_KEY;
  if (!apiKey) throw new Error('GEMINI_API_KEY is not set.');

  const ai = new GoogleGenAI({ apiKey });
  const [styleGuide, cliRules] = await Promise.all([
    readFile(STYLE_GUIDE_PATH, 'utf8'),
    readFile(CLI_RULES_PATH, 'utf8'),
  ]);

  let promptText = `Technical Specifications:\n\n${input.prdText}`;
  if (input.slidesUrl) promptText += `\n\nReference Slides URL: ${input.slidesUrl}`;

  const parts: Part[] = [{ text: promptText }];
  if (input.fileData) {
    parts.unshift({ inlineData: { mimeType: input.fileData.mimeType, data: input.fileData.base64 } });
  }

  // Pass 1 — plan impacted pages with the base style guide.
  const planResult = await ai.models.generateContent({
    model: MODEL,
    contents: { parts },
    config: {
      systemInstruction: await buildSystemInstruction(styleGuide),
      responseMimeType: 'application/json',
      responseSchema,
      temperature: 0.2,
      thinkingConfig: { thinkingBudget: 4096 },
    },
  });

  const pages = parsePages(planResult.text);

  // Pass 2 — re-condition any CLI-help pages with the CLI rules appended.
  const cliPages = pages.filter((p) => isCliHelpPath(p.path));
  if (cliPages.length === 0) {
    return { pages };
  }

  const cliSystemInstruction =
    (await buildSystemInstruction(styleGuide)) + CLI_RULES_TEMPLATE.replace('{{CLI_RULES}}', cliRules);

  const conditioned = await Promise.all(
    cliPages.map(async (page) => {
      const reprompt =
        `Rewrite the following CLI help page so it strictly follows the CLI and IDE documentation ` +
        `rules and the CLI Help command template (H1 = command name; H2 Usage, Description, ` +
        `Exit codes, Options; "option" terminology; imperative-verb option descriptions; ` +
        `"Default: ..." for defaults; absolute links outside help files with no trailing period; ` +
        `relative "command --help" links between help files). Keep the same page path and intent.\n\n` +
        `Page path: ${page.path}\nReason: ${page.reason}\n\nCurrent content:\n${page.content}`;

      const res = await ai.models.generateContent({
        model: MODEL,
        contents: { parts: [{ text: reprompt }] },
        config: {
          systemInstruction: cliSystemInstruction,
          responseMimeType: 'application/json',
          responseSchema,
          temperature: 0.2,
          thinkingConfig: { thinkingBudget: 4096 },
        },
      });

      // The reprompt returns a single-page document; take the first page's content.
      const out = parsePages(res.text);
      const rewritten = out.find((p) => p.path === page.path) ?? out[0];
      return { ...page, content: rewritten?.content ?? page.content };
    }),
  );

  const byPath = new Map(conditioned.map((p) => [p.path, p]));
  return {
    pages: pages.map((p) => byPath.get(p.path) ?? p),
  };
}
