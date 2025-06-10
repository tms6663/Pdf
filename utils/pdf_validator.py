import pypdf
import io

def validate_pdf_file(file_bytes):
    """
    Validates a PDF file from bytes and extracts page count.
    Returns: is_valid (bool), error_message (str), page_count (int)
    """
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = pypdf.PdfReader(pdf_file)
        
        if reader.is_encrypted:
            return False, "الملف محمي بكلمة مرور ولا يمكن تحويله.", 0
            
        page_count = len(reader.pages)
        if page_count == 0:
            return False, "ملف PDF لا يحتوي على صفحات.", 0
            
        return True, "", page_count
    except pypdf.errors.PdfReadError:
        return False, "ملف PDF تالف أو غير صالح.", 0
    except Exception as e:
        return False, f"حدث خطأ غير متوقع أثناء التحقق من الملف: {str(e)}", 0

def get_pdf_info(file_bytes):
    """
    Extracts metadata (title, author) from a PDF file from bytes.
    Returns: dict with 'title' and 'author'
    """
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = pypdf.PdfReader(pdf_file)
        
        metadata = reader.metadata
        info = {}
        if metadata:
            info['title'] = metadata.get('/Title', 'غير متوفر')
            info['author'] = metadata.get('/Author', 'غير متوفر')
        return info
    except Exception:
        return None # Return None if unable to extract info
