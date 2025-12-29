# AI Resume Analyzer - Frontend

Next.js frontend for the AI Resume Analyzer application.

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx        # Main page
│   ├── layout.tsx      # Root layout
│   └── globals.css     # Global styles
├── components/
│   ├── FileUpload.tsx  # Drag & drop upload
│   └── ResultsDisplay.tsx
└── tailwind.config.js
```

## Features

- Drag & drop file upload (PDF, DOCX)
- Paste text input option
- Real-time analysis results
- Responsive dark theme design
