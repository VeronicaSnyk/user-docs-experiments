import React, { useState } from 'react';
import { GeneratedDocumentation, DocumentationPage } from '../types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

interface OutputSectionProps {
  documentation: GeneratedDocumentation | null;
  isLoading: boolean;
  error: string | null;
  onOpenGitBookModal: () => void;
}

const PageCard: React.FC<{ page: DocumentationPage }> = ({ page }) => {
  const [contentMode, setContentMode] = useState<'full' | 'changes'>('full');
  const [displayMode, setDisplayMode] = useState<'preview' | 'code'>('code');
  const [copied, setCopied] = useState(false);

  const getDisplayContent = () => {
    if (page.isNew || contentMode === 'full') return page.content;
    const regex = /<ins>([\s\S]*?)<\/ins>/g;
    const matches = Array.from(page.content.matchAll(regex), m => m[1]);
    return matches.length > 0 ? matches.join('\n\n---\n\n') : "> _No specific changes detected._";
  };

  const copy = () => {
    navigator.clipboard.writeText(getDisplayContent()).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="bg-gray-900/40 border border-gray-800 rounded-xl overflow-hidden mb-6 transition-all hover:border-gray-700">
      <div className="bg-gray-900 px-4 py-3 flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border-b border-gray-800">
        <div className="flex-grow min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase flex-shrink-0 ${page.isNew ? 'bg-green-900/50 text-green-400 border border-green-800' : 'bg-blue-900/50 text-blue-400 border border-blue-800'}`}>
              {page.isNew ? 'New Page' : 'Update'}
            </span>
            <h3 className="text-sm font-mono font-bold text-sky-300 break-all">
              {page.path}
            </h3>
          </div>
          <p className="text-xs text-gray-400 mt-1 italic">{page.reason}</p>
        </div>
        <div className="flex items-center gap-2 w-full md:w-auto justify-end flex-wrap">
          <div className="flex bg-black border border-gray-800 rounded-md p-0.5 mr-2">
            <button onClick={() => setDisplayMode('code')} className={`px-2 py-1 rounded text-[10px] font-bold transition-all ${displayMode === 'code' ? 'bg-gray-800 text-white' : 'text-gray-500 hover:text-gray-300'}`}>Markdown</button>
            <button onClick={() => setDisplayMode('preview')} className={`px-2 py-1 rounded text-[10px] font-bold transition-all ${displayMode === 'preview' ? 'bg-gray-800 text-white' : 'text-gray-500 hover:text-gray-300'}`}>Preview</button>
          </div>
          {!page.isNew && (
            <div className="flex bg-black border border-gray-800 rounded-md p-0.5">
              <button onClick={() => setContentMode('full')} className={`px-2 py-1 rounded text-[10px] font-bold transition-all ${contentMode === 'full' ? 'bg-gray-800 text-white' : 'text-gray-500 hover:text-gray-300'}`}>Full</button>
              <button onClick={() => setContentMode('changes')} className={`px-2 py-1 rounded text-[10px] font-bold transition-all ${contentMode === 'changes' ? 'bg-gray-800 text-white' : 'text-gray-500 hover:text-gray-300'}`}>Changes</button>
            </div>
          )}
          <button onClick={copy} className="bg-gray-800 hover:bg-gray-700 text-gray-300 p-1.5 rounded-md transition border border-gray-700 flex-shrink-0" title="Copy markdown content">
            {copied ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
            )}
          </button>
        </div>
      </div>
      {displayMode === 'preview' ? (
        <div className="p-5 prose prose-base prose-invert max-w-none bg-black/20 leading-relaxed text-gray-200">
          <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
            {getDisplayContent()}
          </ReactMarkdown>
        </div>
      ) : (
        <pre className="p-5 bg-gray-950 text-gray-300 text-sm leading-relaxed overflow-x-auto whitespace-pre-wrap font-mono border-t border-gray-800">
          {getDisplayContent()}
        </pre>
      )}
    </div>
  );
};

export const OutputSection: React.FC<OutputSectionProps> = ({ documentation, isLoading, error, onOpenGitBookModal }) => {
  return (
    <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-lg p-6 flex flex-col h-full">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-sky-400">2. Generated documentation</h2>
        {documentation && (
          <button onClick={onOpenGitBookModal} className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg transition shadow-lg shadow-indigo-900/20 flex items-center gap-2 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.88 7.88l-4.244 4.243m11.314-7.072l-4.243 4.243" /></svg>
            Push All to GitBook
          </button>
        )}
      </div>

      <div className="flex-grow overflow-y-auto">
        {isLoading ? (
          <div className="animate-pulse space-y-4">
            <div className="h-40 bg-gray-900 rounded-xl"></div>
            <div className="h-40 bg-gray-900 rounded-xl"></div>
          </div>
        ) : error ? (
          <div className="text-red-400 bg-red-900/10 border border-red-900/50 rounded-lg p-4 text-sm">{error}</div>
        ) : !documentation ? (
          <div className="text-center text-gray-500 py-20">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            <p>Generated pages will appear here.</p>
          </div>
        ) : (
          documentation.pages.map((p, i) => <PageCard key={i} page={p} />)
        )}
      </div>
    </div>
  );
};
