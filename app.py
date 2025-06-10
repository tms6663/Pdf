"""
PDF to Word Converter Application using Streamlit
"""
import streamlit as st
import io
import os
from utils.pdf_validator import validate_pdf_file, get_pdf_info
from utils.pdf_converter import convert_pdf_to_docx, estimate_conversion_time, get_output_filename

# Page configuration
st.set_page_config(
    page_title="محول PDF إلى Word",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main application function"""
    
    # Application header
    st.title("📄 محول PDF إلى Word")
    st.markdown("---")
    
    # Application description
    st.markdown("""
    ### مرحباً بك في أداة تحويل PDF إلى Word
    
    هذه الأداة تسمح لك بتحويل ملفات PDF إلى مستندات Word (DOCX) بسهولة وأمان.
    
    **الميزات:**
    - ✅ تحويل سريع وآمن
    - ✅ التحقق من صحة الملفات
    - ✅ دعم الملفات الكبيرة
    - ✅ معاينة معلومات الملف
    """)
    
    st.markdown("---")
    
    # File upload section
    st.subheader("📁 رفع ملف PDF")
    
    uploaded_file = st.file_uploader(
        "اختر ملف PDF للتحويل",
        type=['pdf'],
        help="الحد الأقصى لحجم الملف: 200 ميجابايت"
    )
    
    if uploaded_file is not None:
        # Display file information
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**اسم الملف:** {uploaded_file.name}")
            st.info(f"**حجم الملف:** {file_size_mb:.2f} ميجابايت")
        
        # Validate file size
        if file_size_mb > 200:
            st.error("❌ حجم الملف كبير جداً. الحد الأقصى المسموح: 200 ميجابايت")
            return
            
        # Validate PDF file
        st.subheader("🔍 التحقق من صحة الملف")
        
        with st.spinner("جاري التحقق من صحة ملف PDF..."):
            file_bytes = uploaded_file.getvalue()
            is_valid, error_message, page_count = validate_pdf_file(file_bytes)
        
        if not is_valid:
            st.error(f"❌ {error_message}")
            return
            
        # Display PDF information
        st.success(f"✅ ملف PDF صحيح - يحتوي على {page_count} صفحة")
        
        # Get additional PDF info
        pdf_info = get_pdf_info(file_bytes)
        
        with col2:
            if pdf_info and pdf_info.get('title'): # تأكد أن pdf_info ليس None
                st.info(f"**العنوان:** {pdf_info['title']}")
            if pdf_info and pdf_info.get('author'): # تأكد أن pdf_info ليس None
                st.info(f"**المؤلف:** {pdf_info['author']}")
                
        # Estimate conversion time
        estimated_time = estimate_conversion_time(page_count)
        st.info(f"⏱️ **الوقت المتوقع للتحويل:** {estimated_time}")
        
        st.markdown("---")
        
        # Conversion section
        st.subheader("🔄 تحويل الملف")
        
        if st.button("🚀 بدء التحويل", type="primary", use_container_width=True):
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update progress
                progress_bar.progress(25)
                status_text.text("جاري تحضير الملف للتحويل...")
                
                # Convert PDF to DOCX
                # تمرير BytesIO object بدلاً من المسار
                success, docx_bytes, error_message = convert_pdf_to_docx(
                    file_bytes, 
                    uploaded_file.name # تمرير اسم الملف الأصلي
                )
                
                progress_bar.progress(75)
                status_text.text("جاري إنهاء عملية التحويل...")
                
                if success and docx_bytes:
                    progress_bar.progress(100)
                    status_text.text("تم التحويل بنجاح! ✅")
                    
                    # Success message
                    st.success("🎉 تم تحويل الملف بنجاح!")
                    
                    # Generate output filename
                    output_filename = get_output_filename(uploaded_file.name)
                    
                    # Download button
                    st.download_button(
                        label="📥 تحميل ملف Word",
                        data=docx_bytes,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary",
                        use_container_width=True
                    )
                    
                    # Additional information
                    st.info(f"📁 **اسم الملف المحول:** {output_filename}")
                    st.info(f"📊 **حجم الملف المحول:** {len(docx_bytes) / (1024 * 1024):.2f} ميجابايت")
                    
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ فشل في تحويل الملف: {error_message}")
                    
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")
                
    else:
        # Instructions when no file is uploaded
        st.info("👆 يرجى رفع ملف PDF لبدء عملية التحويل")
        
        # Additional help section
        with st.expander("💡 نصائح للاستخدام"):
            st.markdown("""
            **للحصول على أفضل النتائج:**
            
            1. **جودة الملف:** تأكد من أن ملف PDF غير تالف وقابل للقراءة
            2. **حجم الملف:** الملفات الأصغر تتحول بشكل أسرع
            3. **نوع المحتوى:** النصوص العادية تتحول بشكل أفضل من الصور
            4. **التنسيق:** قد يتغير التنسيق المعقد قليلاً بعد التحويل
            
            **أنواع الملفات المدعومة:**
            - ملفات PDF فقط (.pdf)
            - الحد الأقصى للحجم: 200 ميجابايت
            """)
            
        with st.expander("❓ الأسئلة الشائعة"):
            st.markdown("""
            **س: هل البيانات آمنة؟**
            ج: نعم، جميع الملفات تتم معالجتها محلياً ولا يتم حفظها على الخادم.
            
            **س: ما هي أنواع الملفات المدعومة؟**
            ج: حالياً ندعم تحويل ملفات PDF إلى Word (DOCX) فقط.
            
            **س: لماذا فشل التحويل؟**
            ج: قد يفشل التحويل إذا كان الملف تالفاً أو محمياً بكلمة مرور.
            
            **س: هل يمكن تحويل ملفات محمية؟**
            ج: لا، الملفات المحمية بكلمة مرور غير مدعومة حالياً.
            """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
        أداة تحويل PDF إلى Word - آمنة وسريعة
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
