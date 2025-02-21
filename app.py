import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import os
from datetime import datetime

# Alternative font setup using DejaVu (commonly available on Linux)
def setup_font():
    try:
        pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
        return True
    except Exception as e:
        st.error(f"Font registration error: {str(e)}")
        return False

# Initialize font before proceeding
if not setup_font():
    st.stop()

# Title
st.title("Bảng hỏi đánh giá mức độ chấp nhận can thiệp BAI")

# Input fields
ptid = st.text_input("PTID:")
date = st.date_input("Ngày hoàn thành")

st.header("MỨC ĐỘ CHẤP NHẬN CAN THIỆP BAI")

# Define questions
questions = [
    "Nhìn chung, bạn có thích can thiệp BAI không?",
    "Bạn có thích tham dự các buổi can thiệp BAI không?",
    "Bạn có hài lòng với các dịch vụ can thiệp BAI không?",
    "Bạn có thích học can thiệp BAI không?",
    "Bạn có thấy rằng những kỹ năng bạn học được trong can thiệp BAI là hữu ích không?",
    "Bạn có cảm thấy các cấu phần của can thiệp BAI có ý nghĩa với bạn không?",
    "Bạn có cảm thấy thoải mái khi đặt câu hỏi cho tư vấn viên của mình không?",
    "Bạn có cảm thấy tư vấn viên đã lắng nghe những mối quan tâm và câu hỏi của bạn không?",
    "Bạn có cảm thấy hài lòng với khả năng của tư vấn viên trong can thiệp BAI không?",
    "Bạn có cảm thấy tư vấn viên đã giải quyết mọi câu hỏi hay thắc mắc của bạn về can thiệp BAI không?",
    "Tư vấn viên có quan tâm đến bạn không?",
    "Tư vấn viên có sẵn sàng khi bạn cần nói chuyện với họ không?",
    "Bạn có cảm thấy rằng bạn có thể tin tưởng tư vấn viên của bạn không?",
    "Bạn có cảm thấy rằng người cung cấp của bạn đủ năng lực để cung cấp can thiệp BAI không?",
    "Bạn có cảm thấy rằng bạn hiểu cách mọi thứ được giải thích trong can thiệp BAI không?",
]

# Multiple-choice options
options = ["Không", "Một chút", "Vừa phải", "Rất nhiều"]

# Create response dictionary
responses = {}
for i, question in enumerate(questions, 1):
    responses[f"q{i}"] = st.radio(question, options, index=0)

# PDF Export Function
def export_pdf():
    try:
        pdf_filename = "BangHoiDanhGia.pdf"
        c = canvas.Canvas(pdf_filename)
        
        try:
            c.setFont("DejaVu", 12)
        except Exception as e:
            st.error("Error setting font. Falling back to default font.")
            c.setFont("Helvetica", 12)
        
        c.drawString(100, 800, f"PTID: {ptid}")
        c.drawString(100, 780, f"Ngày hoàn thành: {date}")
        
        y = 750
        for i, (key, value) in enumerate(responses.items(), 1):
            c.drawString(100, y, f"{i}. {questions[i-1]}: {value}")
            y -= 20  # Move down for the next line
        
        c.save()
        with open(pdf_filename, "rb") as f:
            st.download_button("Tải xuống PDF", f, file_name=pdf_filename)
    
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")

def save_response():
    # Create a dictionary with the response data
    response_data = {
        'PTID': ptid,
        'Date': date,
    }
    
    # Add all question responses
    for i, (key, value) in enumerate(responses.items(), 1):
        response_data[f'Question_{i}'] = value
    
    # Convert to DataFrame
    df_new = pd.DataFrame([response_data])
    
    # File paths
    csv_file = 'responses.csv'
    excel_file = 'responses.xlsx'
    
    try:
        # Handle CSV file
        if os.path.exists(csv_file):
            df_existing = pd.read_csv(csv_file)
            df_updated = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_updated = df_new
        df_updated.to_csv(csv_file, index=False)
        
        # Try to save Excel file if openpyxl is available
        try:
            if os.path.exists(excel_file):
                df_existing = pd.read_excel(excel_file)
                df_updated = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_updated = df_new
            df_updated.to_excel(excel_file, index=False)
        except ImportError:
            st.warning("Excel export not available. Data saved to CSV only.")
        
        return True
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
        return False

# Export and Save buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Xuất PDF"):
        export_pdf()

with col2:
    if st.button("Lưu phản hồi"):
        if ptid.strip() == "":
            st.error("Vui lòng nhập PTID trước khi lưu")
        else:
            if save_response():
                st.success("Đã lưu phản hồi thành công!")
