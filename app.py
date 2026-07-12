import streamlit as st
from analyser import analyser_resume
from google import genai
from pdf_reader import read_pdf
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
   page_title="AI Resume Analyser",
   page_icon="💾",
   layout="wide" 
)
if "history" not in st.session_state:
    st.session_state.history=[]

client=genai.Client(api_key=api_key)
st.title("AI Resume Analyser")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf")

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area("Paste job description here", height=200)

st.markdown("---")
if st.button("Analyse Resume",use_container_width=True):
    if uploaded_file and job_description:
        with st.spinner("Analysing your resume..."):
           with open("temp_resume.pdf","wb") as f:
            f.write(uploaded_file.read())
           
           resume= read_pdf("temp_resume.pdf")
        
           result= analyser_resume(
            api_key=api_key,
            resume=resume,
            job_description=job_description
           )
           st.session_state.history.append({
            "date":datetime.now().strftime("%Y-%m-%d %H:%M"),
            "resume":uploaded_file.name,
            "result":result
           })
           st.success("\n----ANALYSIS COMPLETE---")
           st.markdown("---")
           st.subheader("📊 Analysis Result")
           st.write(result)
    else:
        st.warning("Please upload resume and paste job description")
st.markdown("---")
st.subheader("📁 Previous Analyses")
if st.session_state.history:
    for entry in st.session_state.history:
        with st.expander(f"{entry['date']}-{entry['resume']}"):
            st.write(entry['result'])
else:
    st.info("No previous analyses yet!")