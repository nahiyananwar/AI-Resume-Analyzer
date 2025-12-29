# AI Resume Analyzer + Classifier

An AI-powered resume analysis system that extracts key information from resumes, classifies job categories, and estimates experience levels.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange?logo=scikit-learn)

## ✨ Features

- **Resume Parsing & Extraction**
  - Name extraction using spaCy NER
  - Email and phone detection via regex
  - Skills matching against curated tech keywords
  - Education details extraction
  - Experience calculation from date ranges

- **ML Classification**
  - TF-IDF + Logistic Regression model
  - 6 job categories: Software Engineer, AI/ML Engineer, Data Scientist, Web Developer, DevOps/Cloud Engineer, FullStack Developer
  - Confidence score for predictions

- **Experience Level Estimation**
  - Junior (0-2 years)
  - Mid (2-5 years)
  - Senior (5+ years)

- **Modern Web UI**
  - Drag & drop file upload
  - Real-time analysis results
  - Confidence score visualization
  - Premium dark theme design

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **pdfplumber** - PDF text extraction
- **spaCy** - NLP for name entity recognition
- **scikit-learn** - ML classification (TF-IDF + Logistic Regression)
- **joblib** - Model persistence

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling

## 📦 Project Structure

```
AI Resume Analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── routers/
│   │   │   └── analyze.py       # /analyze endpoint
│   │   ├── services/
│   │   │   ├── pdf_extractor.py # PDF to text
│   │   │   └── resume_parser.py # Extract info
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   └── ml/
│   │       ├── train_classifier.py
│   │       ├── classifier.py
│   │       └── resume_classifier.joblib
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main page
│   │   ├── layout.tsx           # Root layout
│   │   └── globals.css          # Styles
│   ├── components/
│   │   ├── FileUpload.tsx       # Drag & drop upload
│   │   └── ResultsDisplay.tsx   # Results UI
│   └── package.json
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Train the classifier (first time only)**
   ```bash
   python -m app.ml.train_classifier
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   The UI will be available at `http://localhost:3000`

## 📡 API Reference

### POST /analyze

Analyze a resume file or text.

**Request (File Upload)**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@resume.pdf"
```

**Request (Text Input)**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "text=John Doe is a software engineer with 5 years of experience..."
```

**Response**
```json
{
  "name": "John Doe",
  "email": "john@gmail.com",
  "phone": "017xxxxxxx",
  "skills": ["Python", "Django", "TensorFlow"],
  "education": ["Bachelor's in Computer Science"],
  "experience_years": 3.5,
  "experience_level": "Mid",
  "classification": "AI/ML Engineer",
  "confidence": 0.89
}
```

### GET /health

Health check endpoint.

```bash
curl http://localhost:8000/health
```

## 📊 Job Categories

The classifier recognizes the following job categories:

| Category | Key Indicators |
|----------|----------------|
| Software Engineer | Java, C++, algorithms, backend, API |
| AI/ML Engineer | TensorFlow, PyTorch, neural networks, ML |
| Data Scientist | statistics, pandas, data analysis, visualization |
| Web Developer | HTML, CSS, JavaScript, React, UI/UX |
| DevOps/Cloud Engineer | AWS, Docker, Kubernetes, CI/CD |
| FullStack Developer | Node.js, React, MongoDB, full-stack |

## 🧪 Testing

### Test with sample text
```bash
curl -X POST http://localhost:8000/analyze \
  -F "text=Jane Smith is an experienced machine learning engineer specializing in deep learning and computer vision. Email: jane.smith@email.com. Phone: 555-123-4567. She has worked at Google from 2018 to 2023 developing TensorFlow models. Skills include Python, PyTorch, TensorFlow, and neural networks. She holds a Master's degree in Computer Science from Stanford University."
```

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
