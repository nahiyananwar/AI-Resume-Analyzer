'use client';

interface AnalysisResult {
    name: string | null;
    email: string | null;
    phone: string | null;
    skills: string[];
    education: string[];
    experience_years: number;
    relevant_experience_years?: number;
    other_experience_years?: number;
    experience_breakdown?: any[];
    experience_level: string;
    classification: string;
    confidence: number;
}

interface ResultsDisplayProps {
    result: AnalysisResult;
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
    const getExperienceBadgeClass = (level: string) => {
        const levelLower = level.toLowerCase();
        if (levelLower.includes('junior') || levelLower.includes('entry') || levelLower.includes('intern')) return 'exp-junior';
        if (levelLower.includes('mid') || levelLower.includes('intermediate')) return 'exp-mid';
        if (levelLower.includes('senior') || levelLower.includes('lead') || levelLower.includes('principal')) return 'exp-senior';
        return 'exp-mid';
    };

    return (
        <div className="fade-in space-y-6">
            {/* Classification & Confidence Section */}
            <div className="glass-card p-6">
                <h3 className="section-title">Classification</h3>
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div className="classification-badge">
                        {result.classification}
                    </div>
                    <div className="flex-1 max-w-xs">
                        <div className="flex justify-between mb-2">
                            <span className="text-gray-400 text-sm">Confidence</span>
                            <span className="text-white font-semibold">
                                {(result.confidence * 100).toFixed(0)}%
                            </span>
                        </div>
                        <div className="confidence-bar">
                            <div
                                className="confidence-fill"
                                style={{ width: `${result.confidence * 100}%` }}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Experience Section */}
            <div className="glass-card p-6">
                <h3 className="section-title">Experience</h3>
                <div className="flex items-center gap-6">
                    <div>
                        <p className="text-gray-400 text-sm mb-1">Total Experience</p>
                        <p className="text-3xl font-bold text-white">
                            {result.experience_years}
                            <span className="text-lg font-normal text-gray-400 ml-1">years</span>
                        </p>

                        {/* Split Experience Display */}
                        {(result.relevant_experience_years !== undefined && ((result.other_experience_years || 0) > 0 || result.relevant_experience_years !== result.experience_years)) && (
                            <div className="mt-3 text-sm space-y-1 border-t border-gray-700 pt-3">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-purple-500"></div>
                                    <p>
                                        <span className="text-purple-300 font-medium">{result.relevant_experience_years} years</span>
                                        <span className="text-gray-400"> as {result.classification}</span>
                                    </p>
                                </div>
                                {(result.other_experience_years || 0) > 0 && (
                                    <div className="flex items-center gap-2">
                                        <div className="w-2 h-2 rounded-full bg-gray-600"></div>
                                        <p>
                                            <span className="text-gray-400 font-medium">{result.other_experience_years} years</span>
                                            <span className="text-gray-500"> as Other</span>
                                        </p>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                    <div className={`exp-badge ${getExperienceBadgeClass(result.experience_level)}`}>
                        {result.experience_level}
                    </div>
                </div>
            </div>

            {/* Personal Information */}
            <div className="glass-card p-6">
                <h3 className="section-title">Personal Information</h3>
                <div className="space-y-1">
                    <div className="info-row">
                        <span className="info-label">Name</span>
                        <span className="info-value">{result.name || 'Not detected'}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">Email</span>
                        <span className="info-value">
                            {result.email ? (
                                <a href={`mailto:${result.email}`} className="text-purple-400 hover:underline">
                                    {result.email}
                                </a>
                            ) : (
                                'Not detected'
                            )}
                        </span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">Phone</span>
                        <span className="info-value">{result.phone || 'Not detected'}</span>
                    </div>
                </div>
            </div>

            {/* Skills Section */}
            <div className="glass-card p-6">
                <h3 className="section-title">Skills</h3>
                {result.skills.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                        {result.skills.map((skill, index) => (
                            <span key={index} className="skill-tag">
                                {skill}
                            </span>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-400">No skills detected</p>
                )}
            </div>

            {/* Education Section */}
            <div className="glass-card p-6">
                <h3 className="section-title">Education</h3>
                {result.education.length > 0 ? (
                    <ul className="space-y-2">
                        {result.education.map((edu, index) => (
                            <li key={index} className="text-gray-300 flex items-start gap-2">
                                <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                                </svg>
                                <span>{edu}</span>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="text-gray-400">No education details detected</p>
                )}
            </div>
        </div>
    );
}
