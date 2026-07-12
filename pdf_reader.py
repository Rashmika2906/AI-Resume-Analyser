import PyPDF2
def read_pdf(file_path):
    text=""
    with open(file_path,"rb") as file:
        reader=PyPDF2.PdfReader(file)
        for page in reader.pages:
            text +=page.extract_text()
            return text
def analyse_resume(api_key,resume,job_description):
    llm=create_analyser(api_key)
    prompt=PromptTemplate(
    input_variables=["resume","job_description"],
    template="""
    Analyse this resume against the job description.
    Give response in this exat format:"""
)