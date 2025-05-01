from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Call Gemini Flash
def get_gemini_response(prompt, resume_text, job_desc):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([job_desc, resume_text, prompt])
    return response.text

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("📄 ATS Resume Analyzer (Gemini Flash)")
st.write("Upload your resume and paste the job description. Let the AI evaluate your profile!")

# Input fields
input_text = st.text_area("📌 Job Description", key="input")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF Uploaded Successfully")

# Buttons
submit1 = st.button("🧠 Tell Me About the Resume")
submit2 = st.button("🧩 Missing Keywords")
submit3 = st.button("📊 Percentage Match")

# Prompts
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

# Button Logic
if submit1:
    if uploaded_file:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1, resume_text, input_text)
        st.subheader("📋 Resume Evaluation:")
        st.write(response)
    else:
        st.warning("Please upload the resume.")

elif submit2:
    if uploaded_file:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt2, resume_text, input_text)
        st.subheader("📌 Missing Keywords:")
        st.write(response)
    else:
        st.warning("Please upload the resume.")

elif submit3:
    if uploaded_file:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt3, resume_text, input_text)
        st.subheader("📊 ATS Match Report:")
        st.write(response)
    else:
        st.warning("Please upload the resume.")
