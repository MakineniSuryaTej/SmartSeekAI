controller = Controller()

@controller.action("Read the resume")
def read_resume(resume_path: str) -> dict:
    text = ResumeParser.extract_resume(resume_path)
    return {"extracted_content": text, "include_in_memory": True}

@controller.action("Extract the key details from the resume")
def key_details_from_resume(text: str) -> dict:
    key_details = ResumeParser.analyze_resume(text=text)
    return {"extracted_content": key_details, "include_in_memory": True}


"""query = f"First, read my resume from {resume_path} using the read_resume function. Then, use the output of read_resume as input for the extract_keydetails function to get the key details. Finally, provide me that key details."
"""

"""agent = Agent(
        task = "Read my resume using read_resume from the resume_path and pass this text to the key_details_from_resume and display the key_details",
        llm = get_llm(llm_name="GPT4o"),
        browser=browser,
        controller=controller,
    )
    await agent.run()
    input('Press Enter to close the browser...')
    await browser.close()"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.models import get_llm
from utils.prompts import Prompts
from browser_use import Agent
import asyncio

MODEL_NAME = "GPT4o"

class SearchJobs:
    @staticmethod
    async def search_jobs(information, browser):
        agent = Agent(
            task=Prompts.job_search_prompt.format(information),
            llm=get_llm(MODEL_NAME),
            browser=browser
        )
        history = await agent.run()
        return history

    @staticmethod
    def parse_results(history):
        job_listings = history.split("---")
        parsed_jobs = []
        
        for listing in job_listings:
            if listing.strip():
                job_info = {}
                lines = listing.strip().split("\n")
                for line in lines:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        job_info[key.strip()] = value.strip()
                parsed_jobs.append(job_info)
        return parsed_jobs