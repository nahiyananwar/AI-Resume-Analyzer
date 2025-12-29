'use client';

import { useCallback, useState } from 'react';

type InputMode = 'file' | 'text';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  onTextInput: (text: string) => void;
  isLoading: boolean;
}

export default function FileUpload({ onFileSelect, onTextInput, isLoading }: FileUploadProps) {
  const [inputMode, setInputMode] = useState<InputMode>('file');
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type === 'application/pdf' || file.name.endsWith('.pdf') || file.name.endsWith('.docx')) {
        setSelectedFile(file);
        onFileSelect(file);
      } else {
        alert('Please upload a PDF or DOCX file');
      }
    }
  }, [onFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      setSelectedFile(file);
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const handleClick = () => {
    document.getElementById('file-input')?.click();
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    setResumeText(text);
    onTextInput(text);
  };

  const switchMode = (mode: InputMode) => {
    setInputMode(mode);
    // Clear the other mode's data when switching
    if (mode === 'file') {
      setResumeText('');
      onTextInput('');
    } else {
      setSelectedFile(null);
    }
  };

  return (
    <div className="space-y-4">
      {/* Mode Toggle Tabs */}
      <div className="flex rounded-xl overflow-hidden border border-purple-500/30 bg-black/20">
        <button
          type="button"
          onClick={() => switchMode('file')}
          className={`flex-1 px-4 py-3 text-sm font-medium transition-all flex items-center justify-center gap-2 ${inputMode === 'file'
            ? 'bg-purple-600 text-white'
            : 'text-gray-400 hover:text-white hover:bg-purple-500/10'
            }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          File Upload
        </button>
        <button
          type="button"
          onClick={() => switchMode('text')}
          className={`flex-1 px-4 py-3 text-sm font-medium transition-all flex items-center justify-center gap-2 ${inputMode === 'text'
            ? 'bg-purple-600 text-white'
            : 'text-gray-400 hover:text-white hover:bg-purple-500/10'
            }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Paste Text
        </button>
      </div>

      {/* File Upload Mode */}
      {inputMode === 'file' && (
        <div
          className={`dropzone ${isDragging ? 'active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <input
            id="file-input"
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileInput}
            className="hidden"
            disabled={isLoading}
          />

          <div className="relative z-10">
            {/* Upload Icon */}
            <div className="mb-6">
              <svg
                className="w-16 h-16 mx-auto text-purple-400 opacity-80"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>

            {selectedFile ? (
              <div>
                <p className="text-lg font-semibold text-white mb-2">
                  Selected: {selectedFile.name}
                </p>
                <p className="text-sm text-gray-400">
                  {(selectedFile.size / 1024).toFixed(1)} KB
                </p>
              </div>
            ) : (
              <div>
                <p className="text-xl font-semibold text-white mb-2">
                  Drag & Drop your resume here
                </p>
                <p className="text-gray-400 mb-4">
                  or click to browse files
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF and DOCX files
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Text Input Mode */}
      {inputMode === 'text' && (
        <div className="text-input-area">
          <textarea
            value={resumeText}
            onChange={handleTextChange}
            placeholder="Paste your resume text here..."
            className="w-full h-64 p-4 rounded-xl bg-black/30 border border-purple-500/30 text-white placeholder-gray-500 resize-none focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
            disabled={isLoading}
          />
          <p className="text-sm text-gray-500 mt-2">
            {resumeText.length > 0 ? `${resumeText.length} characters` : 'Paste your resume content above'}
          </p>
        </div>
      )}
    </div>
  );
}
