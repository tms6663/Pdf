from pdf2docx import Converter
import io
import time
import os

def convert_pdf_to_docx(file_bytes, original_filename):
    """
    Converts a PDF file (from bytes) to DOCX format.
    Returns: success (bool), docx_bytes (bytes), error_message (str)
    """
    try:
        # Create temporary input and output paths
        # Use tempfile to create actual files on disk for pdf2docx
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf_path = temp_pdf.name

        # Create a temporary path for the output docx file
        # It's crucial to write to a file first for pdf2docx
        temp_docx_path = temp_pdf_path.replace(".pdf", ".docx") # A simple temp docx path

        cv = Converter(temp_pdf_path)
        cv.convert(temp_docx_path)
        cv.close()

        # Read the converted docx bytes
        with open(temp_docx_path, "rb") as f:
            docx_bytes = f.read()
        
        return True, docx_bytes, ""
    except Exception as e:
        return False, None, f"خطأ في عملية التحويل: {str(e)}"
    finally:
        # Clean up temporary files
        if 'temp_pdf_path' in locals() and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        if 'temp_docx_path' in locals() and os.path.exists(temp_docx_path):
            os.remove(temp_docx_path)

def estimate_conversion_time(page_count):
    """
    Estimates conversion time based on page count.
    """
    if page_count < 10:
        return "ثوانٍ قليلة"
    elif page_count < 50:
        return "1-2 دقيقة"
    elif page_count < 200:
        return "2-5 دقائق"
    else:
        return "أكثر من 5 دقائق"

def get_output_filename(original_filename):
    """
    Generates an output filename for the DOCX file.
    """
    base_name = os.path.splitext(original_filename)[0]
    return f"{base_name}_converted.docx"
