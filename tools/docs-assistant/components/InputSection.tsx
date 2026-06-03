import React, { useRef } from 'react';
import { FileData } from '../types';

interface InputSectionProps {
  prdText: string;
  setPrdText: (text: string) => void;
  slidesUrl: string;
  setSlidesUrl: (url: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
  fileData: FileData | null;
  onFileSelect: (file: File) => void;
  onFileRemove: () => void;
}

export const InputSection: React.FC<InputSectionProps> = ({
  prdText,
  setPrdText,
  slidesUrl,
  setSlidesUrl,
  onGenerate,
  isLoading,
  fileData,
  onFileSelect,
  onFileRemove,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Enable generate if there is text, OR a URL, OR an image.
  const isGenerateDisabled = isLoading || (!prdText.trim() && !slidesUrl.trim() && !fileData);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-lg p-6 flex flex-col h-full">
      <h2 className="text-xl font-semibold mb-4 text-sky-400">
        1. Provide technical specs
      </h2>

      <p className="text-gray-400 mb-2">
        Paste the product requirements document (PRD), one-pager, or any technical specifications below.
      </p>
      <textarea
        value={prdText}
        onChange={(e) => setPrdText(e.target.value)}
        placeholder="For example: Feature: New Snyk Code CLI command `snyk code test --json`..."
        className="w-full flex-grow bg-black border border-gray-800 rounded-md p-3 text-gray-300 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition duration-200 resize-none min-h-[150px]"
        aria-label="Technical specifications input"
      />

      <div className="mt-4">
        <label htmlFor="slidesUrl" className="block text-sm font-medium text-gray-400 mb-1">
          Link to slides (optional)
        </label>
        <input
          type="url"
          id="slidesUrl"
          value={slidesUrl}
          onChange={(e) => setSlidesUrl(e.target.value)}
          placeholder="https://docs.google.com/presentation/d/..."
          className="w-full bg-black border border-gray-800 rounded-md p-3 text-gray-300 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition duration-200"
        />
      </div>

      <div className="mt-4">
        {fileData ? (
          <div className="relative border border-gray-800 rounded-lg p-3 bg-black">
            <p className="text-sm font-medium text-gray-300 mb-2">Attached file: {fileData.name}</p>
            {fileData.mimeType.startsWith('image/') ? (
              <img
                src={`data:${fileData.mimeType};base64,${fileData.base64}`}
                alt="Technical spec preview"
                className="max-h-32 w-auto rounded-md"
              />
            ) : (
              <div className="flex items-center justify-center bg-gray-900 rounded-md h-32 w-24 border border-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <span className="ml-2 text-sm text-gray-400 font-medium">PDF</span>
              </div>
            )}
            <button
              onClick={onFileRemove}
              className="absolute top-2 right-2 bg-gray-700/50 hover:bg-gray-600/70 rounded-full p-1 text-gray-300"
              title="Remove file"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        ) : (
           <div>
            <input
              type="file"
              accept="image/*,application/pdf"
              ref={fileInputRef}
              onChange={handleFileSelect}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="w-full bg-gray-800 hover:bg-gray-700 disabled:bg-gray-800 disabled:cursor-not-allowed text-gray-300 font-bold py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center text-sm"
            >
               <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Add image or PDF (optional)
            </button>
          </div>
        )}
      </div>

      <button
        onClick={onGenerate}
        disabled={isGenerateDisabled}
        className="mt-4 w-full bg-sky-600 hover:bg-sky-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg transition duration-200 flex items-center justify-center"
      >
        {isLoading ? (
          <>
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Generating...
          </>
        ) : (
          'Generate documentation'
        )}
      </button>
    </div>
  );
};
