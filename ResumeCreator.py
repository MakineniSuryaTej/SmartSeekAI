import os
import time
import json
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

def select_date(label_text, month, year, wait, driver):
    date_input = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{label_text}']/following-sibling::div[@data-test='dateInput']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
    time.sleep(1)
    try:
        date_input.click()
    except:
        driver.execute_script("arguments[0].click();", date_input)  
    month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "(//select)[1]")))
    month_select = Select(month_dropdown)
    month_select.select_by_value(str(month-1))
    year_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "(//select)[2]")))
    year_select = Select(year_dropdown)
    year_select.select_by_value(str(year))

def add_projects(projects, wait, driver):
    # print(projects)
    projects_section = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Projects']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", projects_section)
    projects_section.click()
    time.sleep(1.5)

    for pro_key, pro_data in projects.items():
        #print(pro_key)
        #print(pro_data)
        add_button_xpath = "//button[contains(., 'Add Project')]"
        add_project_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_project_button)
        add_project_button.click()
        time.sleep(1)

        open_sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'collapsible') and contains(@class, 'open')]")
        open_section = open_sections[-1]
        if "name" in pro_data:
            name_inputs = open_section.find_elements(By.ID, "name")
            name_input = name_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", name_input)
            name_input.clear()
            name_input.send_keys(pro_data["name"])
        
        if "startdate" in pro_data:
            month, year = pro_data["startdate"]["month"], pro_data["startdate"]["year"]
            date_inputs = open_section.find_elements(By.XPATH, ".//div[@data-test='dateInput']")

            start_date_input = date_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_date_input)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", start_date_input)
            time.sleep(1.5)

            month_dropdowns = driver.find_elements(By.XPATH, "//select[option[text()='January']]")
            month_dropdown = month_dropdowns[0]
            Select(month_dropdown).select_by_value(str(month-1))            
            year_dropdown = month_dropdown.find_element(By.XPATH, "../select[2]")
            Select(year_dropdown).select_by_value(str(year))
            driver.execute_script("arguments[0].click();", open_section)
        
        if "enddate" in pro_data:
            month, year = pro_data["enddate"]["month"], pro_data["enddate"]["year"]
            date_inputs = open_section.find_elements(By.XPATH, ".//div[@data-test='dateInput']")

            start_date_input = date_inputs[1]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_date_input)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", start_date_input)
            time.sleep(1.5)

            month_dropdowns = driver.find_elements(By.XPATH, "//select[option[text()='January']]")
            month_dropdown = month_dropdowns[0]
            Select(month_dropdown).select_by_value(str(month-1))            
            year_dropdown = month_dropdown.find_element(By.XPATH, "../select[2]")
            Select(year_dropdown).select_by_value(str(year))
            driver.execute_script("arguments[0].click();", open_section)
        
        if "info" in pro_data:
            add_highlights_buttons = open_section.find_elements(By.XPATH, ".//button[contains(., 'Add Highlights')]")
            
            if add_highlights_buttons:
                add_highlights_button = add_highlights_buttons[0]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_highlights_button)
                time.sleep(1)
                try:
                    add_highlights_button.click()
                except:
                    driver.execute_script("arguments[0].click();", add_highlights_button)
                
                time.sleep(1)
                open_sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'collapsible') and contains(@class, 'open')]")
                open_section = open_sections[-1]
                
                for index, text in enumerate(pro_data["info"]):
                    try:
                        textareas = open_section.find_elements(By.XPATH, f".//textarea[@name='$highlight[{index}]']")
                        if textareas:
                            textarea = textareas[0]
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textarea)
                            textarea.clear()
                            textarea.send_keys(text + Keys.ENTER) # (Keys.ENTER if index<len(pro_data["info"])-1 else "")
                            
                        else:
                            textarea = wait.until(EC.presence_of_element_located((By.XPATH, f".//textarea[contains(@name, '$highlight[{index}]')]")))
                            textarea.send_keys(text + Keys.ENTER) #+ (Keys.ENTER if index<len(pro_data["info"])-1 else "")
                        time.sleep(1)
                    except Exception as e:
                        print(f"Could not find textarea for highlight {index}: {str(e)}")
                        try:
                            all_textareas = open_section.find_elements(By.XPATH, ".//textarea")
                            if len(all_textareas) > index:
                                all_textareas[index].send_keys(text + (Keys.ENTER if index<len(pro_data["info"])-1 else ""))
                                print(f"Used alternative method for highlight {index}")
                        except:
                            print(f"All attempts failed for highlight {index}")
                
                highlight_rows = open_section.find_elements(By.CSS_SELECTOR, "div.inputRow.list-group-item")
                last_index = len(highlight_rows)  # Get the index of the last row
                # Construct CSS selector for delete icon of last highlight space
                delete_icon_selector = f"div.inputRow.list-group-item:nth-child({last_index}) > svg.svg-inline--fa.fa-trash-can.icon"
                delete_icon = open_section.find_element(By.CSS_SELECTOR, delete_icon_selector)

                # Scroll into view and click the delete icon
                driver.execute_script("arguments[0].scrollIntoView();", delete_icon)
                time.sleep(1)  # Allow time for scrolling animation if needed
                delete_icon.click()
            else:
                print("Could not find 'Add Highlights' button in the current project section")

def add_experience(exp, wait, driver):
    form = ["position", "name", "location"]
    for id in form:
        element = wait.until(EC.presence_of_element_located((By.ID, id)))
        element.send_keys(exp[id])
    
    select_date("Start Date", exp["Start Date"]["month"], exp["Start Date"]["year"], wait, driver)
    select_date("End Date", exp["End Date"]["month"], exp["End Date"]["year"], wait, driver)

    add_highlights_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "addButton")))
    add_highlights_button.click()

    print(exp["info"])
    texts = exp["info"]
    for index, text in enumerate(texts):
        print(index, text)
        textarea = wait.until(EC.presence_of_element_located((By.XPATH, f"//textarea[@name='$highlight[{index}]']")))
        textarea.send_keys(text + Keys.ENTER)
    
    try:
        time.sleep(2)  # Allow time for any dynamic updates
        
        # Locate the delete icon for the last highlight space
        delete_icon = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#highlights > div.inputRow.list-group-item:last-child > svg.svg-inline--fa.fa-trash-can.icon")
        ))
        
        # Re-check if the element is still valid
        delete_icon = driver.find_element(By.CSS_SELECTOR, "#highlights > div.inputRow.list-group-item:last-child > svg.svg-inline--fa.fa-trash-can.icon")
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_icon)
        time.sleep(1)  # Allow time for scrolling animation
        
        # Use JavaScript to click
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", delete_icon)
        print("Deleted the extra highlight space.")
    except Exception as e:
        print("No extra highlight space to delete or an error occurred:", str(e))
    
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
    time.sleep(1)
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
    certificates_section = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Certificates']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", certificates_section)
    certificates_section.click()
    time.sleep(1.5)
    
    for cert_key, cert_data in certificates.items():
        add_button_xpath = "//button[contains(., 'Add Certificate')]"
        add_certificate_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_certificate_button)
        add_certificate_button.click()
        time.sleep(2)
        
        open_sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'collapsible') and contains(@class, 'open')]")
        if not open_sections:
            print("No open certificate sections found!")
            continue
            
        open_section = open_sections[-1]  
        try:
            if "name" in cert_data:
                name_inputs = open_section.find_elements(By.ID, "name")
                if name_inputs:
                    name_input = name_inputs[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", name_input)
                    name_input.clear()
                    name_input.send_keys(cert_data["name"])
                else:
                    print("Name input not found!")
            if "issuer" in cert_data:
                issuer_inputs = open_section.find_elements(By.ID, "issuer")
                if issuer_inputs:
                    issuer_input = issuer_inputs[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", issuer_input)
                    issuer_input.clear()
                    issuer_input.send_keys(cert_data["issuer"])
                else:
                    print("Issuer input not found!")
            if "url" in cert_data:
                url_inputs = open_section.find_elements(By.ID, "url")
                if url_inputs:
                    url_input = url_inputs[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", url_input)
                    url_input.clear()
                    url_input.send_keys(cert_data["url"])
                else:
                    print("URL input not found!")
            if "date" in cert_data:
                date_inputs = open_section.find_elements(By.XPATH, ".//input[@type='text' and @readonly]")
                if not date_inputs:
                    print("No date inputs found in this section!")
                    continue
                date_input = None
                for input_elem in date_inputs:
                    parent = input_elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'inputWrapper')]")
                    labels = parent.find_elements(By.XPATH, ".//label")
                    for label in labels:
                        if "Date" in label.text:
                            date_input = input_elem
                            break
                    if date_input:
                        break
                if not date_input and date_inputs:
                    date_input = date_inputs[0]
                
                if not date_input:
                    print("Could not identify date input field!")
                    continue

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_input)
                time.sleep(0.5)
                
                driver.execute_script("arguments[0].click();", date_input)
                time.sleep(1)
                
                calendars = driver.find_elements(By.CLASS_NAME, "flatpickr-calendar")
                if not calendars or not any(cal.is_displayed() for cal in calendars):
                    try:
                        date_input.click()
                        time.sleep(1)
                    except:
                        print("Failed to click date input!")

                calendars = driver.find_elements(By.CLASS_NAME, "flatpickr-calendar")
                if not calendars or not any(cal.is_displayed() for cal in calendars):
                    print("Calendar did not appear after clicking date input!")
                    try:
                        date_input.send_keys(Keys.TAB)
                        time.sleep(0.5)
                        date_input.send_keys(Keys.SPACE)
                        time.sleep(1)
                    except:
                        print("Alternative click method also failed")
                        continue

                calendars = driver.find_elements(By.CLASS_NAME, "flatpickr-calendar")
                if not calendars or not any(cal.is_displayed() for cal in calendars):
                    print("Could not open calendar - skipping date for this certificate")
                    continue

                calendar = next(cal for cal in calendars if cal.is_displayed())

                parts = cert_data["date"].split(" ")
                day = parts[0]
                month = parts[1]
                year = parts[2]

                try:
                    month_dropdown = calendar.find_element(By.CLASS_NAME, "flatpickr-monthDropdown-months")
                    Select(month_dropdown).select_by_visible_text(month)
                    time.sleep(0.5)
                except:
                    print("Failed to select month")

                try:
                    year_input = calendar.find_element(By.CLASS_NAME, "numInput.cur-year")
                    year_input.clear()
                    year_input.send_keys(year)
                    year_input.send_keys(Keys.ENTER)
                    time.sleep(0.5)
                except:
                    print("Failed to enter year")

                try:
                    day_buttons = calendar.find_elements(By.XPATH,".//span[contains(@class, 'flatpickr-day') and not(contains(@class, 'prevMonthDay')) and not(contains(@class, 'nextMonthDay'))]")

                    for btn in day_buttons:
                        if btn.text.strip() == str(int(day)):
                            btn.click()
                            break
                    else:
                        print(f"Day {day} not found in calendar!")
                except Exception as e:
                    print(f"Error selecting day: {str(e)}")

                time.sleep(1)
                
        except Exception as e:
            print(f"Error filling certificate {cert_key}: {str(e)}")

        time.sleep(1)


def automate_site(resume_info):
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
    title_element.send_keys(resume_info["title"])

    form1 = ["name", "email", "phone", "url", "city", "region", "postalCode", "countryCode"]
    for id in form1:
        element = wait.until(EC.presence_of_element_located((By.ID, id)))
        element.send_keys(Details.personal_info[id])
    
    summary_element = wait.until(EC.presence_of_element_located((By.ID, "summary")))
    summary_element.send_keys(resume_info["summary"])
    
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    continue_button.click()

    add_experience(resume_info["Experience"]["Experience1"], wait, driver)
    add_experience_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Work Experience']]")))
    driver.execute_script("arguments[0].scrollIntoView();", add_experience_button)
    time.sleep(1)
    add_experience_button.click()
    add_experience(resume_info["Experience"]["Experience2"], wait, driver)

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

    skills=resume_info["skills"]
    add_skills(skills, wait)

    add_certifications(Details.certificates, wait, driver)

    print(resume_info["Projects"])
    add_projects(resume_info["Projects"], wait, driver)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]")))
    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
    time.sleep(1)
    continue_button.click()

    time.sleep(5)

    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "download-resume")))
    download_button.click()

    pdf_download_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='download-pdf']")))
    pdf_download_option.click()

    time.sleep(30)
    driver.quit()

def get_updated_resume(information):
    llm = get_llm()
    prompt_with_job = Details.human_prompt.replace("{0}", Details.job_description)
    final_prompt = prompt_with_job.replace("{1}", information)
    messages = [
        SystemMessage(Details.prompt),
        HumanMessage(final_prompt)
    ]
    response = llm.invoke(messages).content.replace("json","")
    print(response)
    return json.loads(response)

resume_information = rp.extract_resume(resume_path)
print("INFORMATION READ")
updated_resume_information = get_updated_resume(resume_information)
print(updated_resume_information)
print(type(updated_resume_information))
automate_site(updated_resume_information)
