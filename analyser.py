from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def analyser_resume(api_key,resume,job_description):
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    
    client=genai.Client(api_key=api_key)

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )    
    chunks=splitter.split_text(resume)
    
    relevant_resume="".join(chunks[:3])

    prompt=PromptTemplate(
    input_variables=["resume","job_description"],
    template="""
    Analyse this resume against te job  description.
    Give response in this exact format:
    ATS SCORE: (give a number out of 100)
            
    STRENGTHS:(list 3 strengths)
            
    MISSING KEYWORDS:(list missing keywords)
            
    INTERVIEW QUESTIONS:(list 3 possible interview questions)
            
    SUGGESTIONS:(list 3 improvement suggestions)
    Resume:{resume}
    Job Description:{job_description}
    """
    )
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt.format(resume=relevant_resume,job_description=job_description)
    )
    return response.text
