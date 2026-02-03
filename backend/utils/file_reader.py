"""
File Reader Module - Extracts text from PDF, DOCX, and TXT files
"""
import io
from docx import Document
import pdfplumber
from typing import Tuple


def extract_text(uploaded_file) -> Tuple[str, str]:
    """
    Extract text from uploaded file (PDF, DOCX, TXT)
    Returns: (text, file_type)
    """
    try:
        file_name = uploaded_file.name.lower()
        
        if file_name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8", errors="ignore")
            return text, "txt"
        
        elif file_name.endswith(".docx"):
            doc = Document(io.BytesIO(uploaded_file.read()))
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            return text, "docx"
        
        elif file_name.endswith(".pdf"):
            text = ""
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return text, "pdf"
        
        else:
            raise ValueError(f"Unsupported file format: {file_name}")
    
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")


def clean_text(text: str) -> str:
    """
    Clean and normalize contract text
    """
    # Remove extra whitespace
    text = " ".join(text.split())
    # Replace multiple punctuation
    import re
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return text


def extract_metadata(text: str) -> dict:
    """
    Extract basic metadata from contract text
    """
    metadata = {
        "word_count": len(text.split()),
        "char_count": len(text),
        "page_estimate": max(1, len(text) // 3000)
    }
    return metadata
