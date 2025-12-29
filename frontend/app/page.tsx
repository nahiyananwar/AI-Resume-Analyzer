'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import ResultsDisplay from '@/components/ResultsDisplay';

// Main App Component
export default function ResumeAnalyzer() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [resetKey, setResetKey] = useState(0);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setResumeText('');
    setError(null);
    setResult(null);
  };

  const handleTextInput = (text: string) => {
    setResumeText(text);
    setSelectedFile(null);
    setError(null);
    setResult(null);
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResumeText('');
    setError(null);
    setResult(null);
    setResetKey(prev => prev + 1); // Force FileUpload to remount
  };

  const handleAnalyze = async () => {
    if (!selectedFile && !resumeText.trim()) {
      setError('Please upload a resume file or paste resume text');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      if (selectedFile) {
        formData.append('file', selectedFile);
      } else if (resumeText.trim()) {
        formData.append('text', resumeText);
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze resume. Please ensure the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen gradient-bg flex flex-col">
      <header className="sticky top-0 z-50 w-full border-b border-cyan-500/20 bg-black/60 backdrop-blur-xl">
        <div className="w-full px-8 lg:px-16 xl:px-24">
          <div className="max-w-[1600px] mx-auto h-24 flex items-center justify-between">
            <a href="/" className="flex items-center gap-4 cursor-pointer hover:opacity-90 transition-opacity">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-purple-500 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-cyan-500/30">
                AI
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  AI Resume Analyzer
                </h1>
                <p className="text-xs text-gray-500 mt-0.5">Intelligent Career Profile Analysis</p>
              </div>
            </a>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow py-12 lg:py-16">
        <div className="w-full px-8 lg:px-16 xl:px-24">
          <div className="max-w-[1600px] mx-auto">
            {/* Two Column Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">

              {/* LEFT COLUMN - Upload Area */}
              <div className="space-y-8 overflow-hidden">
                {/* Upload Card */}
                <div className="glass-card p-8">
                  <div className="flex items-center justify-between mb-8">
                    <h3 className="text-xl font-bold text-white">Upload Resume</h3>
                    <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>

                  <FileUpload
                    key={resetKey}
                    onFileSelect={handleFileSelect}
                    onTextInput={handleTextInput}
                    isLoading={isLoading}
                  />

                  {/* Action Buttons */}
                  <div className="mt-8 flex gap-4">
                    <button
                      onClick={handleAnalyze}
                      disabled={(!selectedFile && !resumeText.trim()) || isLoading}
                      className="flex-1 btn-primary h-14 justify-center text-lg"
                    >
                      {isLoading ? (
                        <>
                          <div className="spinner mr-3" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                          </svg>
                          Analyze Resume
                        </>
                      )}
                    </button>
                    <button
                      onClick={handleReset}
                      disabled={isLoading}
                      className="px-6 h-14 rounded-xl border border-gray-600 text-gray-300 hover:bg-gray-800 hover:border-gray-500 transition-all flex items-center justify-center gap-2"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Reset
                    </button>
                  </div>

                  {/* Error Display */}
                  {error && (
                    <div className="mt-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400">
                      <div className="flex items-start gap-3">
                        <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-sm leading-relaxed">{error}</p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Engine Capabilities */}
                <div className="glass-card p-8 bg-purple-900/5">
                  <h4 className="text-sm font-bold uppercase tracking-widest mb-8 bg-gradient-to-r from-gray-400 via-cyan-400 to-gray-400 bg-[length:200%_100%] bg-clip-text text-transparent animate-shimmer-text">
                    AI Resume Analyzer Capabilities
                  </h4>
                  <div className="grid grid-cols-2 gap-6">
                    {[
                      { label: 'Identity Mapping', icon: '👤' },
                      { label: 'Skill Deep-Scan', icon: '🛠️' },
                      { label: 'Academic Audit', icon: '🎓' },
                      { label: 'Temporal Analysis', icon: '📅' },
                      { label: 'Seniority Check', icon: '📊' },
                      { label: 'Role Classifier', icon: '🏷️' },
                    ].map((item, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-black/20 border border-cyan-500/10 hover:border-cyan-500/30 transition-all">
                        <span className="text-2xl">{item.icon}</span>
                        <span className="text-sm font-medium text-gray-300">{item.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* RIGHT COLUMN - Results Area */}
              <div className="w-full min-w-0">
                {result ? (
                  <ResultsDisplay result={result} />
                ) : (
                  <div className="glass-card p-8 lg:p-12 min-h-[600px] flex flex-col items-center justify-center bg-transparent border-dashed border-gray-700/50">
                    <div className="text-center w-full max-w-sm mx-auto">
                      <div className="w-24 h-24 lg:w-32 lg:h-32 rounded-full bg-gradient-to-br from-purple-500/10 to-cyan-500/10 flex items-center justify-center mb-6 lg:mb-8 mx-auto">
                        <svg className="w-12 h-12 lg:w-16 lg:h-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <h3 className="text-xl lg:text-2xl font-bold text-gray-400 mb-3 lg:mb-4">
                        Analysis Results
                      </h3>
                      <p className="text-sm lg:text-base text-gray-500 leading-relaxed">
                        Upload a resume to see detailed analysis including job classification, skills extraction, experience breakdown, and confidence metrics.
                      </p>
                    </div>
                  </div>
                )}
              </div>

            </div>
          </div>
        </div>
      </main>

      {/* Dedicated Footer with Spacing */}
      <footer className="w-full border-t border-cyan-500/10 bg-black/70 backdrop-blur-xl mt-24">
        <div className="w-full px-8 lg:px-16 xl:px-24">
          <div className="max-w-[1600px] mx-auto py-16">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
              {/* Brand Section */}
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500 to-purple-500 flex items-center justify-center text-white text-sm font-bold">
                    AI
                  </div>
                  <span className="text-lg font-bold text-white">AI Resume Analyzer</span>
                </div>
                <p className="text-sm text-gray-400 leading-relaxed">
                  Advanced natural language processing engine for automated resume parsing, skill extraction, and intelligent job classification.
                </p>
              </div>

              {/* Features Section */}
              <div className="space-y-4">
                <h5 className="text-sm font-bold text-white uppercase tracking-wider">Features</h5>
                <ul className="space-y-2 text-sm text-gray-400">
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-cyan-400"></div>
                    Contact Information Extraction
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-cyan-400"></div>
                    Skills & Technologies Mapping
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-cyan-400"></div>
                    Experience Level Assessment
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-cyan-400"></div>
                    Job Role Classification
                  </li>
                </ul>
              </div>

              {/* Tech Stack Section */}
              <div className="space-y-4">
                <h5 className="text-sm font-bold text-white uppercase tracking-wider">Built With</h5>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-xs text-cyan-400 font-mono">
                    FastAPI
                  </span>
                  <span className="px-3 py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-xs text-cyan-400 font-mono">
                    Next.js
                  </span>
                  <span className="px-3 py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-xs text-cyan-400 font-mono">
                    spaCy
                  </span>
                  <span className="px-3 py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-xs text-cyan-400 font-mono">
                    React
                  </span>
                </div>
                <p className="text-xs text-gray-500 pt-4">
                  Supporting PDF, DOCX, and Raw Text formats
                </p>
              </div>
            </div>

            {/* Bottom Bar */}
            <div className="pt-8 border-t border-cyan-500/10 flex flex-col md:flex-row items-center justify-between gap-4">
              <p className="text-xs text-gray-500">
                &copy; 2025 AI Resume Analyzer. All rights reserved.
              </p>
              <div className="flex items-center gap-6 text-xs text-gray-500">
                <a href="#" className="hover:text-cyan-400 transition-colors">Privacy Policy</a>
                <a href="#" className="hover:text-cyan-400 transition-colors">Terms of Service</a>
                <a href="https://nahiyan-anwar.onrender.com/" className="hover:text-cyan-400 transition-colors" target='_blank'>Contact</a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}