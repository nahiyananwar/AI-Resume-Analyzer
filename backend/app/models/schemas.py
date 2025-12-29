from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeAnalysisRequest(BaseModel):
    """Request model for text-based resume analysis"""
    text: Optional[str] = Field(None, description="Raw resume text")


class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    name: Optional[str] = Field(None, description="Candidate name")
    email: Optional[str] = Field(None, description="Candidate email")
    phone: Optional[str] = Field(None, description="Candidate phone number")
    skills: List[str] = Field(default_factory=list, description="Extracted skills")
    education: List[str] = Field(default_factory=list, description="Education details")
    experience_years: float = Field(0.0, description="Total years of experience")
    relevant_experience_years: float = Field(0.0, description="Years of relevant experience")
    other_experience_years: float = Field(0.0, description="Years of other experience")
    experience_breakdown: List[dict] = Field(default_factory=list, description="Breakdown of experience by role")
    experience_level: str = Field("Junior", description="Experience level: Junior/Mid/Senior")
    classification: str = Field("", description="Job category classification")
    confidence: float = Field(0.0, description="Classification confidence score")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "ok"
    message: str = "AI Resume Analyzer API is running"
