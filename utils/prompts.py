class Prompts:
   key_details_extraction_prompt = "Analyze the following resume text and provide a concise summary of the most important skills, experience, and qualifications. Focus on key technical skills, job titles, years of experience, and any standout achievements or metrics. Format the output as a bulleted list that can be easily used by a job search agent to find relevant positions:\n\n{}"

   task1_agent_prompt = "First, read my resume from {}. Then, use that resume text to extract the key information from it and provide me that key information."

   job_details_extraction_prompt  = """
        You are an AI assistant tasked with extracting the key details from the given HTML content of a job posting on a website.

        HTML Content:
        {html}

        Your goal is to analyze the HTML and identify:
        1.  The Job Title
        2.  The Company Name
        3.  The Job Location
        4.  The Job Description

        Return your findings in the following format:

        Job Title: [The Job Title]
        Company Name: [The Company Name]
        Job Location: [The Job Location]
        Job Description: [The Job Description]

        If any of the above is missing, please mark it as "Not Found".
        """

   analyze_job_fit_prompt = """
        You are an AI assistant analyzing a job and identify how well it fits the candidate
        Candidate Resume Information:
        {resume_info}

        Job posting content you extracted from the webpage:
        {job_details}

        Your goal is to:
        1.  Determine how well the job aligns with the candidate's skills and experience.
        2.  Extract the following information for each job:
            *   Job Title
            *   Company Name
            *   Location
            *   A brief explanation of why the job is a good fit (2-3 sentences).

        3.  Present the results in a structured format for each job:

        Job Title: $$Job Title]
        Company: $$Company Name]
        Location: $$Location]
        Match Explanation: $$Brief explanation of why this is a good fit]
        """