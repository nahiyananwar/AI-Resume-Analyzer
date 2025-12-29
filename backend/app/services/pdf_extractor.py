"""
PDF Text Extraction Service
Uses pdfplumber to extract clean text from PDF files
"""
import pdfplumber
import io
import re
from typing import Optional


def clean_text(text: str) -> str:
    """Clean extracted text by removing extra whitespace and normalizing"""
    if not text:
        return ""
    
    # Replace multiple spaces/tabs with single space (preserve newlines)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Replace multiple newlines with double newline (paragraph separation)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Strip leading/trailing whitespace
    return text.strip()


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file content
    
    Args:
        file_content: PDF file content as bytes
        
    Returns:
        Extracted and cleaned text from the PDF
    """
    text_parts = []
    
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    full_text = '\n\n'.join(text_parts)
    return clean_text(full_text)


def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from DOCX file content
    
    Args:
        file_content: DOCX file content as bytes
        
    Returns:
        Extracted and cleaned text from the DOCX
    """
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_content))
        text_parts = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        
        full_text = '\n'.join(text_parts)
        return clean_text(full_text)
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
