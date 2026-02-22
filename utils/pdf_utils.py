"""
pdf_utils.py
------------
Utility functions for extracting text from PDF resumes.
Supports text-based PDFs only (not scanned/image PDFs).
"""

import pdfplumber


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts text from a text-based PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object or file-like object.

    Returns:
        str: Extracted text content from the PDF.
             Returns an empty string if no text could be extracted.
    """
    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

    except Exception:
        # If anything goes wrong (corrupt PDF, etc.), return empty string
        return ""

    return text.strip()