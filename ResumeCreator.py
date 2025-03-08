import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.models import get_llm
from utils.details import Details
from agents.resume_parser import ResumeParser as rp
from langchain_core.messages import SystemMessage, HumanMessage

MODEL_NAME = "GPT4o"
resume_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'Resume.pdf')

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

def select_date(label_text, month, year, wait, driver):
    date_input = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{label_text}']/following-sibling::div[@data-test='dateInput']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
    time.sleep(1)
    try:
        date_input.click()
    except:
        driver.execute_script("arguments[0].click();", date_input)  # JavaScript click as fallback
    month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "(//select)[1]")))
    month_select = Select(month_dropdown)
    month_select.select_by_value(str(month))
    year_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "(//select)[2]")))
    year_select = Select(year_dropdown)
    year_select.select_by_value(str(year))

def add_experience(exp, wait, driver):
    form = ["position", "name", "location"]
    for id in form:
        element = wait.until(EC.presence_of_element_located((By.ID, id)))
        element.send_keys("sent "+id)
    
    select_date("Start Date", 2, 2023, wait, driver)
    select_date("End Date", 11, 2025, wait, driver)

    add_highlights_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "addButton")))
    add_highlights_button.click()

    texts = ["point 1", "point 2", "point 3"]
    for index, text in enumerate(texts):
        textarea = wait.until(EC.presence_of_element_located((By.XPATH, f"//textarea[@name='$highlight[{index}]']")))
        textarea.send_keys(text + (Keys.ENTER if index<len(texts)-1 else ""))
    
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    continue_button.click()

def add_education(education, wait, driver):
    form = ["institution", "studyType", "area", "score"]
    for id in form:
        element = wait.until(EC.presence_of_element_located((By.ID, id)))
        element.send_keys(education[id])
    select_date("Start Date", education["startdate"]["month"], education["startdate"]["year"], wait, driver)
    select_date("End Date", education["enddate"]["month"], education["enddate"]["year"], wait, driver)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    continue_button.click()

def add_skills(skills, wait):
    core_skills_section = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Core Skills']")))
    core_skills_section.click()
    time.sleep(1)

    for skill in skills:
        skill_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add a skill...']")))
        skill_input.send_keys(skill + Keys.ENTER)
        time.sleep(1)

def add_certifications(certificates, wait, driver):
    # Navigate to the Certificates section
    certificates_section = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Certificates']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", certificates_section)
    certificates_section.click()
    time.sleep(1.5)  # Allow section to expand
    
    # For each certificate in the dictionary
    for cert_key, cert_data in certificates.items():
        print(f"Adding certificate: {cert_key}")
        
        # Find the "Add Certificate" button
        add_button_xpath = "//button[contains(., 'Add Certificate')]"
        add_certificate_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_certificate_button)
        add_certificate_button.click()
        
        # Wait for the new certificate section to fully load and expand
        time.sleep(2)  # Increased wait time
        
        # Find the most recently opened certificate section
        open_sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'collapsible') and contains(@class, 'open')]")
        if not open_sections:
            print("No open certificate sections found!")
            continue
            
        open_section = open_sections[-1]  # Get the last (most recently added) open section
        
        # Fill in certificate details
        try:
            # Handle name field
            if "name" in cert_data:
                name_inputs = open_section.find_elements(By.ID, "name")
                if name_inputs:
                    name_input = name_inputs[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", name_input)
                    name_input.clear()
                    name_input.send_keys(cert_data["name"])
                else:
                    print("Name input not found!")
            
            # Handle issuer field
            if "issuer" in cert_data:
                issuer_inputs = open_section.find_elements(By.ID, "issuer")
                if issuer_inputs:
                    issuer_input = issuer_inputs[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", issuer_input)
                    issuer_input.clear()
                    issuer_input.send_keys(cert_data["issuer"])
                else:
                    print("Issuer input not found!")
            
            # Handle URL field
            if "url" in cert_data:
                url_inputs = open_section.find_elements(By.ID, "url")
                if url_inputs:
                    url_input = url_inputs[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", url_input)
                    url_input.clear()
                    url_input.send_keys(cert_data["url"])
                else:
                    print("URL input not found!")
            
            # Handle date field with more robust approach
            if "date" in cert_data:
                # Find date field using multiple strategies
                date_inputs = open_section.find_elements(By.XPATH, ".//input[@type='text' and @readonly]")
                
                if not date_inputs:
                    print("No date inputs found in this section!")
                    continue
                
                # Get the date input - likely the one near a "Date" label
                date_input = None
                for input_elem in date_inputs:
                    # Try to find a nearby "Date" label
                    parent = input_elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'inputWrapper')]")
                    labels = parent.find_elements(By.XPATH, ".//label")
                    for label in labels:
                        if "Date" in label.text:
                            date_input = input_elem
                            break
                    if date_input:
                        break
                
                # If we still can't find it, take the first readonly input
                if not date_input and date_inputs:
                    date_input = date_inputs[0]
                
                if not date_input:
                    print("Could not identify date input field!")
                    continue
                
                print(f"  Setting date: {cert_data['date']}")
                
                # Try multiple click strategies
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_input)
                time.sleep(0.5)
                
                # First try JavaScript click
                driver.execute_script("arguments[0].click();", date_input)
                time.sleep(1)
                
                # Check if calendar appeared
                calendars = driver.find_elements(By.CLASS_NAME, "flatpickr-calendar")
                if not calendars or not any(cal.is_displayed() for cal in calendars):
                    # Try regular click if JS click didn't work
                    try:
                        date_input.click()
                        time.sleep(1)
                    except:
                        print("Failed to click date input!")
                
                # Check again if calendar appeared
                calendars = driver.find_elements(By.CLASS_NAME, "flatpickr-calendar")
                if not calendars or not any(cal.is_displayed() for cal in calendars):
                    print("Calendar did not appear after clicking date input!")
                    # Try a different approach - send a Tab key to move focus, then Space to activate
                    try:
                        date_input.send_keys(Keys.TAB)
                        time.sleep(0.5)
                        date_input.send_keys(Keys.SPACE)
                        time.sleep(1)
                    except:
                        print("Alternative click method also failed")
                        continue
                
                # One more check for calendar
                calendars = driver.find_elements(By.CLASS_NAME, "flatpickr-calendar")
                if not calendars or not any(cal.is_displayed() for cal in calendars):
                    print("Could not open calendar - skipping date for this certificate")
                    continue
                
                # Calendar is now open - get the displayed one
                calendar = next(cal for cal in calendars if cal.is_displayed())
                
                # Parse the date
                parts = cert_data["date"].split(" ")
                day = parts[0]
                month = parts[1]
                year = parts[2]
                
                # Select month from dropdown
                try:
                    month_dropdown = calendar.find_element(By.CLASS_NAME, "flatpickr-monthDropdown-months")
                    Select(month_dropdown).select_by_visible_text(month)
                    time.sleep(0.5)
                except:
                    print("Failed to select month")
                
                # Enter year
                try:
                    year_input = calendar.find_element(By.CLASS_NAME, "numInput.cur-year")
                    year_input.clear()
                    year_input.send_keys(year)
                    year_input.send_keys(Keys.ENTER)
                    time.sleep(0.5)
                except:
                    print("Failed to enter year")
                
                # Find and click the day
                try:
                    # Get all day elements in the current month view
                    day_buttons = calendar.find_elements(By.XPATH, 
                        ".//span[contains(@class, 'flatpickr-day') and not(contains(@class, 'prevMonthDay')) and not(contains(@class, 'nextMonthDay'))]")
                    
                    # Find the one with matching text
                    for btn in day_buttons:
                        if btn.text.strip() == str(int(day)):
                            btn.click()
                            break
                    else:
                        print(f"Day {day} not found in calendar!")
                except Exception as e:
                    print(f"Error selecting day: {str(e)}")
                
                # Wait for calendar to close
                time.sleep(1)
                
        except Exception as e:
            print(f"Error filling certificate {cert_key}: {str(e)}")
        
        # Wait between certificates
        time.sleep(2)


def automate_site():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    driver.get("https://app.jobscan.co/resume-builder/start")

    username_element = wait.until(EC.presence_of_element_located((By.ID, "email")))
    username_element.send_keys(Details.email)

    password_element = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_element.send_keys("Beena&1973" + Keys.ENTER)

    create_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'card') and .//div[contains(text(), 'Create a new resume')]]")))
    create_element.click()

    skip_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and text()=' Skip ']")))
    skip_element.click()

    modern_professional_template = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Modern Professional')]")))
    modern_professional_template.click()

    continue_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'AppButton')]")))
    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
    time.sleep(1)
    continue_button.click()

    title_element = wait.until(EC.presence_of_element_located((By.ID, "label")))
    title_element.send_keys("sent title")

    form1 = ["name", "email", "phone", "url", "city", "region", "postalCode", "countryCode"]
    for id in form1:
        element = wait.until(EC.presence_of_element_located((By.ID, id)))
        element.send_keys(Details.personal_info[id])
    
    summary_element = wait.until(EC.presence_of_element_located((By.ID, "summary")))
    summary_element.send_keys("sent summary")
    
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    continue_button.click()

    add_experience("test", wait, driver)
    add_experience_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Work Experience']]")))
    driver.execute_script("arguments[0].scrollIntoView();", add_experience_button)
    time.sleep(1)
    add_experience_button.click()
    add_experience("test", wait, driver)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
    time.sleep(1)
    continue_button.click()

    add_education(Details.education["Education1"], wait, driver)
    add_education_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Education']]")))
    driver.execute_script("arguments[0].scrollIntoView();", add_education_button)
    time.sleep(1)
    add_education_button.click()
    add_education(Details.education["Education2"], wait, driver)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
    time.sleep(1)
    continue_button.click()

    skills=["python", "c", "java", "react"]
    add_skills(skills, wait)

    add_certifications(Details.certificates, wait, driver)

    time.sleep(30)
    driver.quit()

def get_updated_resume(information):
    llm = get_llm("GPT4o")
    messages = [
        SystemMessage("You are an expert assistant for tailoring resumes."),
        HumanMessage(Details.prompt.format(Details.job_description, information))
    ]
    return llm.invoke(messages).content



#resume_information = rp.extract_resume(resume_path)
#print("INFORMATION READ")
#updated_resume_information = get_updated_resume(resume_information)
#print(updated_resume_information)
automate_site()

