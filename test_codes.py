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
    


def select_date_from_picker(date, wait, driver):
    # Find the parent div of the date input
    date_wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'inputWrapper') and .//label[text()='Date']]")))

    # Find the input element within the wrapper
    date_input = date_wrapper.find_element(By.XPATH, ".//input[@type='text' and @readonly]")

    # Scroll the element into view and click it using JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
    driver.execute_script("arguments[0].click();", date_input)

    # Wait for the calendar to appear
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "flatpickr-calendar")))

    # Parse the date
    day, month, year = date.split(" ")

    # Select the month
    month_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "flatpickr-monthDropdown-months")))
    driver.execute_script("arguments[0].scrollIntoView(true);", month_dropdown)
    Select(month_dropdown).select_by_visible_text(month)

    # Enter the year
    year_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "numInput.cur-year")))
    year_input.clear()
    year_input.send_keys(year)
    year_input.send_keys(Keys.ENTER)

    # Select the day
    day_xpath = f"//span[@class='flatpickr-day' and text()='{day}']" #f"//span[@class='flatpickr-day' and not(contains(@class, 'prevMonthDay')) and not(contains(@class, 'nextMonthDay')) and text()='{day}']"
    day_button = wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
    day_button.click()

    # Wait for the calendar to close
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "flatpickr-calendar")))


def add_certifications(certificates, wait, driver):
    certificates_section = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Certificates']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", certificates_section)
    certificates_section.click()
    time.sleep(1)

    for certificate in certificates:
        add_certificate_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resume_builder"]/div/div[1]/div[2]/div[2]/div[2]/div/button')))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_certificate_button)
        time.sleep(1)
        add_certificate_button.click()
        time.sleep(1)

        # Wait for the new certificate section to be added and opened
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'collapsible') and contains(@class, 'open')]//form")))

        for id, value in certificates[certificate].items():
            if id == "date":
                print(value)
                select_date_from_picker(value, wait, driver)
            else:
                # Target the most recently added (last) open certificate section
                input_xpath = f"(//div[contains(@class, 'collapsible') and contains(@class, 'open')]//input[@id='{id}'])[last()]"
                input_element = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
                driver.execute_script("arguments[0].scrollIntoView();", input_element)
                input_element.clear() # Clear any existing text
                input_element.send_keys(value)

        time.sleep(1) # Short pause after filling each certificate