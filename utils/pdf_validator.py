"""
PDF validation utilities using PyPDF2
"""
import PyPDF2
import io
from typing import Tuple, Optional

def validate_pdf_file(file_bytes: bytes) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Validate if the uploaded file is a valid PDF
    
    Args:
        file_bytes: The uploaded file bytes
        
    Returns:
        Tuple of (is_valid, error_message, page_count)
    """
    try:
        # Create a BytesIO object from the file bytes
        pdf_stream = io.BytesIO(file_bytes)
        
        # Try to read the PDF
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        
        # Check if the PDF has pages
        page_count = len(pdf_reader.pages)
        
        if page_count == 0:
            return False, "ملف PDF فارغ - لا يحتوي على صفحات", 0
            
        # Try to read the first page to ensure it's not corrupted
        try:
            first_page = pdf_reader.pages[0]
            # Try to extract text to verify page integrity
            first_page.extract_text()
        except Exception as e:
            return False, f"ملف PDF تالف - لا يمكن قراءة الصفحات: {str(e)}", 0
            
        return True, None, page_count
        
    except PyPDF2.errors.PdfReadError as e:
        return False, f"خطأ في قراءة ملف PDF: {str(e)}", 0
    except Exception as e:
        return False, f"خطأ غير متوقع في التحقق من الملف: {str(e)}", 0

def get_pdf_info(file_bytes: bytes) -> dict:
    """
    Extract basic information from PDF file
    
    Args:
        file_bytes: The PDF file bytes
        
    Returns:
        Dictionary containing PDF information
    """
    try:
        pdf_stream = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        
        info = {
            'page_count': len(pdf_reader.pages),
            'title': '',
            'author': '',
            'subject': '',
            'creator': ''
        }
        
        # Try to extract metadata
        if pdf_reader.metadata:
            info['title'] = pdf_reader.metadata.get('/Title', '') or ''
            info['author'] = pdf_reader.metadata.get('/Author', '') or ''
            info['subject'] = pdf_reader.metadata.get('/Subject', '') or ''
            info['creator'] = pdf_reader.metadata.get('/Creator', '') or ''
            
        return info
        
    except Exception as e:
        return {
            'page_count': 0,
            'title': '',
            'author': '',
            'subject': '',
            'creator': '',
            'error': str(e)
        }
