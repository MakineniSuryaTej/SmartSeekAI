import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.models import get_llm
from agents.resume_parser import ResumeParser as rp
from langchain_core.messages import SystemMessage, HumanMessage

MODEL_NAME = "GPT4o"
resume_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'Resume.pdf')

job_description = """
Role Description
This is a full-time remote role for an AI ML Engineer at Marvis Inc. The AI ML Engineer will be responsible for tasks such as pattern recognition, working with neural networks, analyzing statistics, and implementing algorithms on a day-to-day basis.

Qualifications
Skills in Pattern Recognition and Neural Networks
Strong background in Computer Science
Experience working with Statistics and Algorithms
Experience with machine learning frameworks like TensorFlow or PyTorch
Proficiency in programming languages like Python, Java, or C++
Strong problem-solving and analytical skills
Master's or PhD in Computer Science, AI, or related field
Experience in developing AI/ML solutions in a professional setting"""

prompt = """
Analyze the following job description and my current resume. Optimize my resume for ATS by incorporating relevant keywords, skills, and experiences from the job posting. Rewrite each section to highlight my qualifications that best match the role requirements. Ensure the formatting is ATS-friendly, using a chronological structure and standard section headings. Quantify achievements where possible and use action verbs to describe responsibilities. Limit the resume to two pages maximum. Here's the job description: {} And here's my current resume: {}

The output should strictly follow this JSON format:
updated_resume = {{
    "summary": "#my summary information",
    "skills": ["#list of my skills"],
    "experience": {{
        "company1": {{
            "name": "#Name of company 1",
            "title": "#My job title in the company 1",
            "time": "#Time worked or still working",
            "info": ["#3-5 bullet points on what I have done"]
        }},
        "company2": {{
            "name": "#Name of company 2",
            "title": "#My job title in the company 2",
            "time": "#Time worked or still working",
            "info": ["#3-5 bullet points on what I have done"]
        }}
    }},
    "projects": {{
        "project1": {{
            "name": "#Name of project 1",
            "time": "#Time worked or still working",
            "info": ["#3-5 bullet points on what I have done"]
        }},
        "project2": {{
            "name": "#Name of project 2",
            "time": "#Time worked or still working",
            "info": ["#3-5 bullet points on what I have done"]
        }}
    }},
    "Education": {{
        "Education1": {{
            "name": "#Name of the college",
            "time": "#Timeline",
            "field": "#Name of the field",
            "GPA": "#GPA score"
        }},
        "Education2": {{
            "name": "#Name of the college",
            "time": "#Timeline",
            "field": "#Name of the field",
            "GPA": "#GPA score"
        }}
    }},
    "Certifications": {{
        "certificate1": {{
            "name": "#Name of the certificate",
            "time": "#time",
            "issuedby": "#name of the issuer"
        }}
    }}
}}

Please provide only the updated JSON object as output.
"""


def automate_site():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    driver.get("https://app.jobscan.co/resume-builder/start")

    username_element = wait.until(EC.presence_of_element_located((By.ID, "email")))
    username_element.send_keys("baces83662@losvtn.com")

    password_element = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_element.send_keys("Beena&1973" + Keys.ENTER)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'card') and .//div[contains(text(), 'Create a new resume')]]")))
    element.click()

    skip_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and text()=' Skip ']")))
    skip_element.click()

    modern_professional_template = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Modern Professional')]")))
    modern_professional_template.click()

    continue_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'AppButton')]")))
    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
    time.sleep(1)
    continue_button.click()

    time.sleep(15)
    driver.quit()

def get_updated_resume(information):
    llm = get_llm("GPT4o")
    messages = [
        SystemMessage("You are an expert assistant for tailoring resumes."),
        HumanMessage(prompt.format(job_description, information))
    ]
    return llm.invoke(messages).content



resume_information = rp.extract_resume(resume_path)
print("INFORMATION READ")
updated_resume_information = get_updated_resume(resume_information)
print(updated_resume_information)
#automate_site()


