class Prompts:
    key_details_extraction_prompt = "Analyze the following resume text and provide a concise summary of the most important skills, experience, and qualifications. Focus on key technical skills, job titles, years of experience, and any standout achievements or metrics. Format the output as a bulleted list that can be easily used by a job search agent to find relevant positions:\n\n{}"

    task1_agent_prompt = "First, read my resume from {}. Then, use that resume text to extract the key information from it and provide me that key information."