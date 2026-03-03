from pypdf import PdfReader
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def clean_text(text):
    """Clean extracted text"""
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.replace('\n', ' ')
    return text.strip()

def validate_resume_text(text):
    """Check if resume text is valid"""
    if not text or len(text) < 50:
        return False, "Resume text is too short. Please upload a complete resume."
    return True, "Valid resume text"