from google import genai
from pdf_reader import read_pdf
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client=genai.Client(api_key=api_key)


pdf_path=input("Enter path of your resume here:")
resume=read_pdf(pdf_path)
job_description =input("Paste your job description:")

prompt= f""" 
Analyse this resume against the job description.
Give a match score out of 100and feedback.

Resume= {resume}
Job Description: {job_description}
"""
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n----ANALYSIS RESULT---")
print(response.text)

with open("result.txt","w") as file:
    file.write(response.text)
print("Result saved to result.txt")