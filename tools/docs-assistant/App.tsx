import React, { useState } from 'react';
import { Header } from './components/Header';
import { InputSection } from './components/InputSection';
import { OutputSection } from './components/OutputSection';
import { generateDocumentation } from './services/geminiService';
import { GeneratedDocumentation, GitBookMetadata, FileData } from './types';
import { GitBookModal } from './components/GitBookModal';
import { pushToGitBook } from './services/gitbookService';

function App() {
  const [prdText, setPrdText] = useState('');
  const [slidesUrl, setSlidesUrl] = useState('');
  const [fileData, setFileData] = useState<FileData | null>(null);
  const [documentation, setDocumentation] = useState<GeneratedDocumentation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isGitBookModalOpen, setIsGitBookModalOpen] = useState(false);

  const handleFileSelect = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      if (result) {
        const [meta, base64Data] = result.split(',');
        const mimeType = meta.match(/:(.*?);/)?.[1];
        if (base64Data && mimeType) setFileData({ base64: base64Data, mimeType, name: file.name });
      }
    };
    reader.readAsDataURL(file);
  };

  const handleGenerate = async () => {
    if (!prdText.trim() && !slidesUrl.trim() && !fileData) return;
    setIsLoading(true);
    setError(null);
    setDocumentation(null);
    try {
      const result = await generateDocumentation(prdText, slidesUrl, fileData);
      setDocumentation(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePushToGitBook = async (metadata: GitBookMetadata): Promise<string> => {
    if (!documentation) throw new Error("No documentation available.");
    return await pushToGitBook(metadata);
  };

  return (
    <>
      <div className="bg-black min-h-screen text-gray-300 font-sans">
        <Header />
        <main className="container mx-auto p-4 md:p-6 lg:p-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <InputSection
              prdText={prdText}
              setPrdText={setPrdText}
              slidesUrl={slidesUrl}
              setSlidesUrl={setSlidesUrl}
              onGenerate={handleGenerate}
              isLoading={isLoading}
              fileData={fileData}
              onFileSelect={handleFileSelect}
              onFileRemove={() => setFileData(null)}
            />
            <OutputSection
              documentation={documentation}
              isLoading={isLoading}
              error={error}
              onOpenGitBookModal={() => setIsGitBookModalOpen(true)}
            />
          </div>
        </main>
      </div>
      {isGitBookModalOpen && documentation && (
        <GitBookModal
          documentation={documentation}
          onClose={() => setIsGitBookModalOpen(false)}
          onSubmit={handlePushToGitBook}
        />
      )}
    </>
  );
}

export default App;
