import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="bg-gray-950/70 backdrop-blur-sm shadow-md sticky top-0 z-10 border-b border-gray-800">
      <div className="container mx-auto px-4 md:px-6 lg:px-8 py-4">
        <h1 className="text-2xl md:text-3xl font-bold text-sky-400">
          AI documentation assistant
        </h1>
        <p className="text-gray-400 mt-1">
          Transforms technical specs into polished documentation using Snyk's style guide.
        </p>
      </div>
    </header>
  );
};
