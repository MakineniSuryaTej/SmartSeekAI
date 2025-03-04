import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.models import get_llm
import PyPDF2
from langchain_openai import ChatOpenAI

llm = get_llm()

class ResumeParser:
    def extract_resume(file_path):
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text

    def analyze_resume(text):
        prompt = f"Extract skills, job titles, and experience from the following resume:\n\n{text}"
        response = llm.invoke(prompt)
        return response.content
    
# print(ResumeParser.analyze_resume(ResumeParser.extract_resume(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'Resume.pdf'))))