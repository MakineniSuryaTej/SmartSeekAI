import os
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from langchain_openai import ChatOpenAI
import asyncio
from utils.models import get_llm
from utils.prompts import Prompts
from agents.resume_parser import ResumeParser
from langchain import hub
from langchain.agents import tool
from browser_use.browser.context import BrowserContext
import time
from pathlib import Path

MODEL_NAME = "GPT4o"
resume_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'Resume.pdf')

#Check is the resume exits if not raise error
resume_path_check = Path(resume_path)
if not resume_path_check.exists():
    raise FileNotFoundError(f'You need to set the path to your cv file in the CV variable. CV file not found at {resume_path}')

browser = Browser(
    config=BrowserConfig(
        headless=True,
        chrome_instance_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #Make sure this is the directory
    )
)

controller = Controller()

@controller.action("read_resume")
def read_resume_action(path: str) -> ActionResult: #Need ActionResult
    """Reads the resume from the given path and returns the resume text"""
    try:
        text = ResumeParser.extract_resume(path)
        return ActionResult(extracted_content=text, include_in_memory=True)
    except FileNotFoundError:
        return ActionResult(error=f"Error: Resume file not found at path: {path}", include_in_memory=False)
    except Exception as e:
        return ActionResult(error=f"Error reading resume: {str(e)}", include_in_memory=False)

@controller.action("go_to_url")
async def go_to_url_action(url: str, browser: BrowserContext) -> ActionResult: #Needs to be async and also take the BrowserContext
    """Navigates the browser to the given URL."""
    try:
        await browser.goto(url)
        await asyncio.sleep(5)  # Wait for the page to load
        return ActionResult(extracted_content=f"Navigated to {url}", include_in_memory=True)
    except Exception as e:
        return ActionResult(error=f"Error navigating to {url}: {str(e)}", include_in_memory=False)

@controller.action("click_apply_button")
async def click_apply_button_action(browser: BrowserContext, xpath: str = "//button[contains(text(), 'Apply')]") -> ActionResult: #Need to add BrowserContext
    """Clicks the apply button on the page using xpath."""
    try:
        # Use browser_use to click the button
        apply_button = await browser.locate_single_element(xpath)  # Locate the button
        if apply_button: #Verify that the button loads correctly
            await apply_button.click()  #Click the button
            await asyncio.sleep(5)  # Wait for the application form to load

            return ActionResult(extracted_content="Clicked apply button", include_in_memory=True)
        else:
            return ActionResult(error="Apply button not found with the default XPath.  Inspect the page and provide a better XPath.", include_in_memory=False) #If the button is not found
    except Exception as e:
        return ActionResult(error=f"Error clicking apply button: {str(e)}", include_in_memory=False) #If there's some error


@controller.action("fill_form")
async def fill_form_action(form_details: str, browser: BrowserContext) -> ActionResult:
    """Fills the application form based on the provided details."""
    try:
        # Need a clear set of instructions here
        return ActionResult(extracted_content=f"Form filling logic needs further development, right now form details are {form_details} from read resume", include_in_memory=True)

    except Exception as e:
        return ActionResult(error=f"Error filling form: {str(e)}", include_in_memory=False) #The error of not filling the form


@controller.action("upload_resume")
async def upload_resume_action(browser: BrowserContext, index: int = 0) -> ActionResult:
    """Uploads the resume to the element"""
    path = str(Path(resume_path).absolute())

    dom_el = await browser.get_dom_element_by_index(index)

    if dom_el is None:
        return ActionResult(error=f'No element found at index {index}')

    file_upload_dom_el = dom_el.get_file_upload_element()

    if file_upload_dom_el is None:
        return ActionResult(error=f'No file upload element found at index {index}')

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)

    if file_upload_el is None:
        return ActionResult(error=f'No file upload element found at index {index}')

    try:
        await file_upload_el.set_input_files(path)
        msg = f'Successfully uploaded file "{path}" to index {index}'
        return ActionResult(extracted_content=msg)
    except Exception as e:
        return ActionResult(error=f'Failed to upload file to index {index}')


@controller.action("ask_user")
def ask_user_action(question: str) -> ActionResult:
    """Asks the user a question and captures the response."""
    answer = input(question + "\n")
    return ActionResult(extracted_content=answer, include_in_memory=True)

@tool
def ask_user(question: str) -> str:
    """Asks the user a question and returns the answer."""
    answer = input(question + "\n")
    return answer

async def main():
    job_url = "https://www.linkedin.com/jobs/view/4162739501/?alternateChannel=search&refId=47c32fde-4e2c-471e-b9e1-2b2382e4a1eb&trackingId=TSBI9dz5Q%2F68V9KfMNBMDA%3D%3D"
    task_description = f"""
    Your goal is to apply for the job at this URL: {job_url}.  Follow these steps:
    1. First, read my resume using the 'read_resume' tool, I will provide the path.
    2. Then, go to the job application URL using the 'go_to_url' tool.
    3. Next, click the 'Apply' button using the 'click_apply_button' tool.  If the default xpath is not working, check the page and provide an appropriate one.
    4. Use the 'fill_form' tool to fill the application form with relevant information from my resume.
    5. If there's a resume upload field, use the 'upload_resume' tool to upload my resume, path will be given.  Try different indexes if the first one fails.
    6. If you encounter any questions that you cannot answer from my resume, use the 'ask_user' tool to ask me for the information.

    Resume path: {resume_path}
    """
    #7. Finally, if there is a message then fill the message with information

    llm = get_llm(MODEL_NAME)

    tools = [read_resume_action, go_to_url_action, click_apply_button_action, fill_form_action, upload_resume_action, ask_user] #All of the function to be called
    agent = Agent(
        task=task_description,
        llm=llm,
        browser=browser,
        controller=controller
    )
    await agent.run() #Run the agent


if __name__ == "__main__":
    asyncio.run(main())
