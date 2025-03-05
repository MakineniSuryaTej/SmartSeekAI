import os
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from langchain_openai import ChatOpenAI
import asyncio
from utils.models import get_llm
from agents.resume_parser import ResumeParser
from langchain import hub
from langchain.agents import tool
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import create_react_agent, AgentExecutor

resume_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'Resume.pdf')
print(resume_path)

"""browser = Browser(
    config=BrowserConfig(
        headless=True,
        chrome_instance_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
)

controller = Controller()

@controller.action("Read the resume")
def read_resume(resume_path: str) -> dict:
    text = ResumeParser.extract_resume(resume_path)
    return {"extracted_content": text, "include_in_memory": True}

@controller.action("Extract the key details from the resume")
def key_details_from_resume(text: str) -> dict:
    key_details = ResumeParser.analyze_resume(text=text)
    return {"extracted_content": key_details, "include_in_memory": True}
"""

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


llm = get_llm("GPT4o")
tools = [read_resume, extract_keydetails]
prompt_template = hub.pull("hwchase17/react")
"""query = f"First, read my resume from {resume_path} using the read_resume function. Then, use the output of read_resume as input for the extract_keydetails function to get the key details. Finally, provide me that key details."
"""
query = f"First, read my resume from {resume_path}. Then, use that resume text to extract the key information from it and provide me that key information."


async def main():

    """agent = Agent(
        task = "Read my resume using read_resume from the resume_path and pass this text to the key_details_from_resume and display the key_details",
        llm = get_llm(llm_name="GPT4o"),
        browser=browser,
        controller=controller,
    )
    await agent.run()
    input('Press Enter to close the browser...')
    await browser.close()"""
    agent = create_react_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_executor.invoke({"input": query})


if __name__ == '__main__':
    asyncio.run(main())