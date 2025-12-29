import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Resume Analyzer - Classify & Extract Resume Information",
  description: "AI-powered resume analysis tool that extracts key information, classifies job categories, and estimates experience levels from PDF resumes.",
  keywords: ["resume analyzer", "AI", "job classification", "resume parser", "NLP"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
