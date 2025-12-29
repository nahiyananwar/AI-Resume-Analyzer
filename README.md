# AI Resume Analyzer

An intelligent resume analysis system built with FastAPI and Next.js that extracts information, classifies job categories, and estimates experience levels using machine learning.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
</p>

## Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Parsing** | Extract name, email, phone, skills, and education |
| 🤖 **ML Classification** | Classify into 6 job categories with confidence scores |
| 📊 **Experience Analysis** | Calculate years and determine Junior/Mid/Senior level |
| 🎨 **Modern UI** | Drag & drop upload with real-time results |

## Tech Stack

**Backend:** FastAPI, spaCy, scikit-learn, pdfplumber  
**Frontend:** Next.js, TypeScript, Tailwind CSS

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## API

**POST /analyze** - Analyze a resume (file or text)

```bash
curl -X POST http://localhost:8000/analyze -F "file=@resume.pdf"
```

**Response:**
```json
{
  "name": "John Doe",
  "email": "john@email.com",
  "skills": ["Python", "React", "AWS"],
  "classification": "Software Engineer",
  "experience_level": "Mid",
  "confidence": 0.92
}
```

## Job Categories

- Software Engineer
- AI/ML Engineer
- Data Scientist
- Web Developer
- DevOps/Cloud Engineer
- FullStack Developer
