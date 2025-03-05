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