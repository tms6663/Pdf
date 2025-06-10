"""
PDF to DOCX conversion utilities using pdf2docx
"""
import tempfile
import os
from pdf2docx import Converter
from typing import Tuple, Optional
import io

def convert_pdf_to_docx(pdf_bytes: bytes, filename: str) -> Tuple[bool, Optional[bytes], Optional[str]]:
    """
    Convert PDF bytes to DOCX format
    
    Args:
        pdf_bytes: The PDF file bytes
        filename: Original filename (for reference)
        
    Returns:
        Tuple of (success, docx_bytes, error_message)
    """
    temp_pdf_path = None
    temp_docx_path = None
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(pdf_bytes)
            temp_pdf_path = temp_pdf.name
            
        # Create temporary DOCX file path
        temp_docx_path = temp_pdf_path.replace('.pdf', '.docx')
        
        # Convert PDF to DOCX
        cv = Converter(temp_pdf_path)
        cv.convert(temp_docx_path, start=0, end=None)
        cv.close()
        
        # Read the converted DOCX file
        with open(temp_docx_path, 'rb') as docx_file:
            docx_bytes = docx_file.read()
            
        return True, docx_bytes, None
        
    except Exception as e:
        error_msg = f"خطأ في تحويل الملف: {str(e)}"
        return False, None, error_msg
        
    finally:
        # Clean up temporary files
        try:
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
            if temp_docx_path and os.path.exists(temp_docx_path):
                os.unlink(temp_docx_path)
        except Exception as cleanup_error:
            # Log cleanup error but don't fail the conversion
            print(f"تحذير: لم يتم حذف الملفات المؤقتة: {cleanup_error}")

def estimate_conversion_time(page_count: int) -> str:
    """
    Estimate conversion time based on page count
    
    Args:
        page_count: Number of pages in the PDF
        
    Returns:
        Estimated time as string
    """
    if page_count <= 5:
        return "أقل من دقيقة"
    elif page_count <= 20:
        return "1-2 دقيقة"
    elif page_count <= 50:
        return "2-5 دقائق"
    else:
        return "5-10 دقائق"

def get_output_filename(original_filename: str) -> str:
    """
    Generate output filename for the converted DOCX file
    
    Args:
        original_filename: Original PDF filename
        
    Returns:
        Output DOCX filename
    """
    if original_filename.lower().endswith('.pdf'):
        base_name = original_filename[:-4]
    else:
        base_name = original_filename
        
    return f"{base_name}_converted.docx"
