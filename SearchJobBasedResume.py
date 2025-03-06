import os
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from langchain_openai import ChatOpenAI
import asyncio
from utils.models import get_llm
from utils.prompts import Prompts
from agents.resume_parser import ResumeParser
from agents.search_jobs import SearchJobs
from langchain import hub
from langchain.agents import tool
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import create_react_agent, AgentExecutor

MODEL_NAME = "GPT4o"
resume_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'Resume.pdf')


browser = Browser(
    config=BrowserConfig(
        headless=True,
        chrome_instance_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
)


@tool
def read_resume(path: str) -> str:
    """Reads the resume from the given path and returns the resume text"""
    try:
        text = ResumeParser.extract_resume(path)
        return text
    except FileNotFoundError:
        return f"Error: Resume file not found at path: {path}"
    except Exception as e:
        return f"Error reading resume: {str(e)}"


@tool
def extract_keydetails(text: str = "") -> str:
    """Analyzes and extracts the key information from the text and returns that text"""
    if not text:
        return "Error: No resume text provided for analysis"
    key_details = ResumeParser.analyze_resume(text=text)
    return key_details


llm = get_llm(MODEL_NAME)
tools = [read_resume, extract_keydetails]
prompt_template = hub.pull("hwchase17/react")
query = Prompts.task1_agent_prompt.format(resume_path)


async def main():
    """TASK 1 Resume Parsing"""
    agent = create_react_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    task1_result = agent_executor.invoke({"input": query})
    print(task1_result["output"])
    information = task1_result["output"]

    """TASK 2 Job Search based on resume"""
    job_search_results = await SearchJobs.search_jobs(information=information, browser=browser)
    parsed_jobs = SearchJobs.parse_results(job_search_results)
    
    print(parsed_jobs)

if __name__ == '__main__':
    asyncio.run(main())