import streamlit as st
from docxtpl import DocxTemplate
from docx.shared import Cm
import os
import csv
import datetime

def generate_docx(ptid, date_completed, interviewer, responses):
    template = DocxTemplate("(BAI) Bang hoi danh gia tinh chap nhan can thiep BAI.docx")

    context = {
        "PTID": ptid,
        "DATE_COMPLETED": date_completed.strftime("%d/%m/%Y"),
        "INTERVIEWER": interviewer,
    }

    for i, response in enumerate(responses, start=1):
        context[f"AC{i}"] = response

    response_mapping = {"Không": False, "Một chút": True, "Vừa phải": True, "Rất nhiều": True, "Từ chối trả lời": False, "Không biết": False}
    for i, response in enumerate(responses, start=1):
        context[f"CHECK_AC{i}"] = "✓" if response_mapping[response] else "☐"

    template.render(context)
    output_path = "generated_document.docx"
    template.save(output_path)
    return output_path

def save_to_csv(ptid, date_completed, interviewer, responses):
    filename = "survey_responses.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['PTID', 'Date Completed', 'Interviewer'] + [f'AC{i}' for i in range(1, 16)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row_data = {'PTID': ptid, 'Date Completed': date_completed.strftime("%Y-%m-%d"), 'Interviewer': interviewer}
        for i, response in enumerate(responses):
            row_data[f'AC{i+1}'] = response

        writer.writerow(row_data)
    return filename

def main():
    st.title("Generate DOCX with Checkboxes")

    ptid = st.text_input("PTID")
    date_completed = st.date_input("Completion Date")
    interviewer = st.text_input("Interviewer")

    responses = [st.radio(f"Question AC{i}", ["Không", "Một chút", "Vừa phải", "Rất nhiều", "Từ chối trả lời", "Không biết"]) for i in range(1, 16)]

    if not os.path.exists("(BAI) Bang hoi danh gia tinh chap nhan can thiep BAI.docx"):
        st.error("Template file '(BAI) Bang hoi danh gia tinh chap nhan can thiep BAI.docx' not found!")
        return

    if st.button("Generate DOCX and Save Responses"):
        if not ptid or not interviewer:
            st.error("PTID and Interviewer are required fields.")
            return

        docx_path = generate_docx(ptid, date_completed, interviewer, responses)
        st.success("DOCX file generated successfully!")

        csv_path = save_to_csv(ptid, date_completed, interviewer, responses)
        st.success("Responses saved to CSV!")

        with open(docx_path, "rb") as f:
            st.download_button("Download DOCX", f, file_name="survey_results.docx")

        with open(csv_path, "r", encoding='utf-8') as f:
            st.download_button("Download CSV", f, file_name="survey_responses.csv")

if __name__ == "__main__":
    main()
