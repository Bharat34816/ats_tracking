import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import re
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, resume_text, job_description):
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content([job_description, resume_text, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Missing Keywords")
submit3 = st.button("Percentage Match")


input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an experienced Technical HR professional. Compare the resume against the job description.
List all important keywords or skills that appear in the job description but are missing in the resume.
Return ONLY the missing keywords as a bullet list.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description.
First, output the percentage, then list the missing keywords, and finally provide your overall thoughts.
"""


if submit1:
    if uploaded_file:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_text, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please upload the resume.")

elif submit2:
    if uploaded_file:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_text, input_text)
        st.subheader("Missing Keywords:")
        st.write(response)
    else:
        st.warning(" Please upload the resume.")

elif submit3:
    if uploaded_file:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_text, input_text)
        st.subheader("Percentage Match & Analysis:")
        st.write(response)

        match = re.search(r'(\d+)%', response)
        if match:
            percent = int(match.group(1))
            st.progress(percent)
    else:
        st.warning("⚠️ Please upload the resume.")
