import { GoogleGenAI, Part, Type } from '@google/genai';
import { GeneratedDocumentation, FileData } from '../types';
import { SYSTEM_INSTRUCTION_TEMPLATE, SNYK_DOC_EXAMPLES_BY_SECTION } from '../constants';

// Browser variant: the API key is injected via process.env.API_KEY at build time (vite.config.ts).
// The full style guide is loaded from disk only in the headless core (core/generate.ts); the
// browser UI relies on the inline examples below plus the system instruction.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY! });

const responseSchema = {
  type: Type.OBJECT,
  properties: {
    pages: {
      type: Type.ARRAY,
      description: 'A list of documentation pages to be created or updated.',
      items: {
        type: Type.OBJECT,
        properties: {
          path: { type: Type.STRING, description: "Suggested file path/slug (e.g., 'developer-tools/snyk-cli/commands/code-test.md')." },
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

const buildSystemInstruction = (): string => {
  let examplesString = '';
  for (const [section, content] of Object.entries(SNYK_DOC_EXAMPLES_BY_SECTION)) {
    examplesString += `\n<example section="${section}">\n${content}\n</example>\n`;
  }
  return SYSTEM_INSTRUCTION_TEMPLATE
    .replace('{{STYLE_GUIDE}}', '(See the team style guide. Apply Snyk voice, sentence case, present tense, neutral pronouns, no contractions.)')
    .replace('{{EXAMPLES}}', examplesString);
};

export const generateDocumentation = async (
  prdText: string,
  slidesUrl: string,
  fileData: FileData | null
): Promise<GeneratedDocumentation> => {
  let promptText = `Technical Specifications:\n\n${prdText}`;
  if (slidesUrl) promptText += `\n\nReference Slides URL: ${slidesUrl}`;

  const parts: Part[] = [{ text: promptText }];
  if (fileData) {
    parts.unshift({ inlineData: { mimeType: fileData.mimeType, data: fileData.base64 } });
  }

  const systemInstruction = buildSystemInstruction();

  try {
    const result = await ai.models.generateContent({
      model: 'gemini-3-pro-preview',
      contents: { parts },
      config: {
        systemInstruction,
        responseMimeType: 'application/json',
        responseSchema,
        temperature: 0.2,
        thinkingConfig: { thinkingBudget: 4096 },
      },
    });

    const responseText = result.text.trim();
    const jsonString = responseText.replace(/^```json\s*/, '').replace(/```\s*$/, '');
    const parsedJson = JSON.parse(jsonString);

    if (!parsedJson.pages || !Array.isArray(parsedJson.pages)) {
      throw new Error("AI response format invalid: missing 'pages' array.");
    }
    return parsedJson as GeneratedDocumentation;
  } catch (error) {
    console.error('Error generating documentation:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    if (errorMessage.includes('xhr error') || errorMessage.includes('500')) {
      throw new Error(`Connection issue with the Gemini API. This can happen with very large technical specs or images. Try reducing the input size. Details: ${errorMessage}`);
    }
    throw new Error(`Failed to generate documentation. ${errorMessage}`);
  }
};
