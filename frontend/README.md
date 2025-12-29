# AI Resume Analyzer — Frontend

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

</div>

---

## Overview

React-based frontend for the AI Resume Analyzer, built with Next.js 14 App Router.

---

## Quick Start

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx        # Main application page
│   ├── layout.tsx      # Root layout with metadata
│   └── globals.css     # Global styles, animations, theme
│
├── components/
│   ├── FileUpload.tsx      # Drag & drop + text input
│   └── ResultsDisplay.tsx  # Analysis results cards
│
├── tailwind.config.js  # Custom theme & animations
├── postcss.config.mjs  # PostCSS configuration
└── package.json
```

---

## Components

### `FileUpload`
- Drag & drop zone for PDF/DOCX files
- Tab toggle between file upload and text paste
- File validation and size display

### `ResultsDisplay`
- Classification badge with confidence bar
- Experience breakdown (relevant vs other)
- Skills tags grid
- Education list
- Contact information

---

## Styling

Built with **Tailwind CSS** and custom CSS:

- Dark theme with cyan/purple gradient accents
- Glassmorphism card effects
- Animated shimmer text
- Responsive grid layout
- Custom scrollbar styling

---

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
