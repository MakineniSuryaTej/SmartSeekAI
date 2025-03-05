import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.models import get_llm
from utils.prompts import Prompts
import PyPDF2

llm = get_llm()

class ResumeParser:
    def extract_resume(file_path):
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text

    def analyze_resume(text):
        prompt = Prompts.key_details_extraction_prompt.format(text)
        # print("llm invoked")
        response = llm.invoke(prompt)
        return response.content
    
# print(ResumeParser.analyze_resume(ResumeParser.extract_resume(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'Resume.pdf'))))