# AI Resume Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-3.7-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)

**An intelligent resume analysis system that extracts candidate information, classifies job categories, and estimates experience levels using machine learning and NLP.**

</div>

---

## Overview

AI Resume Analyzer is a full-stack application that processes resumes (PDF/DOCX/Text) and provides:

- **Information Extraction** — Name, email, phone, skills, education
- **Job Classification** — ML-powered categorization into 11 job roles
- **Experience Analysis** — Total years, relevant vs. other experience, seniority level

---

## Architecture

```
┌─────────────────┐     HTTP/REST      ┌─────────────────┐
│                 │ ◄─────────────────► │                 │
│  Next.js 14     │                     │  FastAPI        │
│  Frontend       │                     │  Backend        │
│                 │                     │                 │
│  • React 19     │                     │  • spaCy NER    │
│  • TypeScript   │                     │  • scikit-learn │
│  • Tailwind CSS │                     │  • pdfplumber   │
└─────────────────┘                     └─────────────────┘
```

---

## Features

### Resume Parsing
| Component | Technology | Description |
|-----------|------------|-------------|
| **Name Extraction** | spaCy NER | PERSON entity recognition with fallback heuristics |
| **Contact Info** | Regex | Email and phone number patterns (international formats) |
| **Skills** | Keyword Matching | 100+ curated tech skills (languages, frameworks, tools) |
| **Education** | Pattern Matching | Degrees, certifications, institutions |
| **Experience** | Date Parsing | Date range extraction with `dateutil` |

### ML Classification
- **Algorithm**: TF-IDF Vectorization + Logistic Regression
- **Training Data**: Custom resume dataset
- **Output**: Job category + confidence score (0-1)

### Job Categories
```
Software Engineer    │  AI/ML Engineer      │  Data Scientist
Web Developer        │  Full Stack Developer│  DevOps Engineer
Cloud Architect      │  Mobile App Developer│  QA Engineer
Cybersecurity Analyst│  Database Administrator
```

### Experience Levels
| Level | Years |
|-------|-------|
| Junior | 0 - 2 |
| Mid | 2 - 5 |
| Senior | 5+ |

---

## Project Structure

```
AI-Resume-Analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry
│   │   ├── routers/
│   │   │   └── analyze.py          # POST /analyze endpoint
│   │   ├── services/
│   │   │   ├── pdf_extractor.py    # PDF/DOCX text extraction
│   │   │   └── resume_parser.py    # NLP-based information extraction
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic request/response models
│   │   └── ml/
│   │       ├── classifier.py       # Model loading & prediction
│   │       ├── train_classifier.py # Training pipeline
│   │       ├── dataset/            # Training data
│   │       └── resume_classifier.joblib  # Trained model
│   ├── requirements.txt
│   └── render.yaml                 # Render deployment config
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx                # Main application page
│   │   ├── layout.tsx              # Root layout
│   │   └── globals.css             # Global styles & animations
│   ├── components/
│   │   ├── FileUpload.tsx          # Drag & drop file upload
│   │   └── ResultsDisplay.tsx      # Analysis results UI
│   ├── tailwind.config.js
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- pip / npm

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Start server
uvicorn app.main:app --reload --port 8000
```

**API available at:** `http://localhost:8000`  
**Interactive docs:** `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**UI available at:** `http://localhost:3000`

---

## API Reference

### `POST /analyze`

Analyze a resume file or text input.

**Request:**
```bash
# File upload
curl -X POST http://localhost:8000/analyze \
  -F "file=@resume.pdf"

# Text input
curl -X POST http://localhost:8000/analyze \
  -F "text=John Doe is a software engineer..."
```

**Response:**
```json
{
  "name": "John Doe",
  "email": "john.doe@email.com",
  "phone": "+1-555-123-4567",
  "skills": ["Python", "React", "AWS", "Docker"],
  "education": ["B.Sc. Computer Science, MIT"],
  "experience_years": 4.5,
  "relevant_experience_years": 3.2,
  "other_experience_years": 1.3,
  "experience_breakdown": [
    {"title": "Software Engineer", "years": 2.5},
    {"title": "Junior Developer", "years": 1.0}
  ],
  "experience_level": "Mid",
  "classification": "Software Engineer",
  "confidence": 0.87
}
```

### `GET /health`

Health check endpoint.

```bash
curl http://localhost:8000/health
# {"status": "ok", "message": "AI Resume Analyzer API is running"}
```

---

## Tech Stack

### Backend
| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.109.0 | Web framework |
| spaCy | 3.7.2 | NLP & NER |
| scikit-learn | 1.4.0 | ML classification |
| pdfplumber | 0.10.3 | PDF extraction |
| python-docx | 1.1.0 | DOCX extraction |
| python-dateutil | 2.8.2 | Date parsing |

### Frontend
| Package | Version | Purpose |
|---------|---------|---------|
| Next.js | 14 | React framework |
| React | 19 | UI library |
| TypeScript | 5 | Type safety |
| Tailwind CSS | 3 | Styling |

---

## How It Works

1. **Upload** — User uploads PDF/DOCX or pastes text
2. **Extract** — `pdfplumber` or `python-docx` converts to plain text
3. **Parse** — spaCy NER + regex extracts structured data
4. **Classify** — TF-IDF + Logistic Regression predicts job category
5. **Analyze** — Date ranges parsed to calculate experience
6. **Display** — Results rendered in React UI
