"""
Resume Analysis Router
Provides the /analyze endpoint for resume processing
"""
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from typing import Optional
from app.models.schemas import ResumeAnalysisResponse
from app.services.pdf_extractor import extract_text_from_pdf, extract_text_from_docx
from app.services.resume_parser import parse_resume
from app.ml.classifier import classify_resume, get_experience_level


router = APIRouter()


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    file: Optional[UploadFile] = File(None, description="PDF or DOCX resume file"),
    text: Optional[str] = Form(None, description="Raw resume text")
):
    """
    Analyze a resume and extract key information
    
    - **file**: Upload a PDF or DOCX resume file
    - **text**: Or provide raw resume text
    
    Returns extracted information, job classification, and experience level.
    """
    resume_text = None
    
    # Process file upload
    if file:
        # Validate file type
        filename = file.filename.lower() if file.filename else ""
        
        if filename.endswith('.pdf'):
            try:
                content = await file.read()
                resume_text = extract_text_from_pdf(content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to process PDF file: {str(e)}"
                )
        elif filename.endswith('.docx'):
            try:
                content = await file.read()
                resume_text = extract_text_from_docx(content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to process DOCX file: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a PDF or DOCX file."
            )
    elif text:
        resume_text = text.strip()
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide either a file upload or text input."
        )
    
    # Validate text content
    if not resume_text or len(resume_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="Resume content is too short or empty. Please provide a valid resume."
        )
    
    # Parse resume
    parsed_data = parse_resume(resume_text)
    
    # Classify resume
    classification, confidence = classify_resume(resume_text)
    

    
    # Calculate Relevant vs Other Experience
    breakdown = parsed_data.get("experience_breakdown", [])
    relevant_years = 0.0
    other_years = 0.0
    
    # Define keywords for each category
    # Categories: "Software Engineer", "Data Scientist", "AI Engineer", "Web Developer", 
    # "Mobile App Developer", "DevOps Engineer", "Full Stack Developer"
    # "Cloud Architect", "Database Administrator", "Cybersecurity Analyst", "QA Engineer", "Network Engineer"
    category_keywords = {
        "Web Developer": ["web", "frontend", "front-end", "front end", "backend", "back-end", "back end", "fullstack", "full-stack", "full stack", "react", "node", "js", "html", "css", "django", "laravel", "developer", "engineer", "software", "freelance"],
        "Full Stack Developer": ["fullstack", "full-stack", "full stack", "web", "frontend", "backend", "react", "node", "django", "software", "developer", "engineer"],
        "Software Engineer": ["software", "engineer", "developer", "programmer", "system", "application", "tech", "stack"],
        "AI Engineer": ["ai", "machine learning", "ml", "deep learning", "dl", "nlp", "computer vision", "data scientist", "model", "algorithm"],
        "Data Scientist": ["data", "scientist", "analyst", "ml", "ai", "python", "statistics", "research"],
        "Machine Learning Engineer": ["machine learning", "ml", "ai", "model", "algorithm", "engineer"],
        "DevOps Engineer": ["devops", "cloud", "aws", "azure", "docker", "kubernetes", "ci/cd", "infrastructure", "systems"],
        "Cloud Architect": ["cloud", "architect", "aws", "azure", "gcp", "infrastructure"],
        "Mobile App Developer": ["mobile", "android", "ios", "flutter", "react native", "swift", "kotlin", "app"],
        "QA Engineer": ["qa", "quality", "test", "automation", "selenium", "assurance"],
        "Cybersecurity Analyst": ["security", "cyber", "analyst", "network", "protection", "info"],
    }
    
    target_keywords = category_keywords.get(classification, [])
    # Fallback to generic if not found specific
    if not target_keywords:
        target_keywords = classification.lower().split()

    for item in breakdown:
        title = item["title"].lower()
        years = item["years"]
        # Check matches
        matched = False
        for kw in target_keywords:
            if kw.lower() in title:
                matched = True
                break
        
        if matched:
            relevant_years += years
        else:
            other_years += years
    
    # If no breakdown found (e.g. no dates), assume all is relevant if total > 0? 
    # Or just keep it as is.
    if not breakdown and parsed_data["experience_years"] > 0:
         # If classification matches skills/text, assume relevant?
         # Simplified: If no breakdown, we can't split.
         relevant_years = parsed_data["experience_years"]

    # Get experience level based on RELEVANT experience
    experience_level = get_experience_level(relevant_years)

    # Build response
    return ResumeAnalysisResponse(
        name=parsed_data["name"],
        email=parsed_data["email"],
        phone=parsed_data["phone"],
        skills=parsed_data["skills"],
        education=parsed_data["education"],
        experience_years=parsed_data["experience_years"],
        relevant_experience_years=round(relevant_years, 1),
        other_experience_years=round(other_years, 1),
        experience_breakdown=breakdown,
        experience_level=experience_level,
        classification=classification,
        confidence=confidence
    )
