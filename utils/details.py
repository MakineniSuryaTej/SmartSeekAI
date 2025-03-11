class Details:
    email = "login mail"
    password = "login password"

    personal_info = {
        "name": "Surya Tej Makineni",
        "email": "makinenisuryatej@gmail.com",
        "phone": "xxxxxxxxxxx",
        "url": "https://www.linkedin.com/in/makinenisuryatej/",
        "city": "Wichita",
        "region": "Kansas",
        "postalCode": "67208",
        "countryCode": "US"
    }

    education = {
        "Education1": {
            "institution": "Wichita State University",
            "studyType": "Masters",
            "area": "Computer Science",
            "startdate": {
                "month": 8,
                "year": 2022
            },
            "enddate": {
                "month": 5,
                "year": 2024
            },
            "score": 3.97
        },
        "Education2": {
            "institution": "Prasad V Potluri Siddartha Institute of Technology",
            "studyType": "Bachelor of Technology",
            "area": "Computer Science",
            "startdate": {
                "month": 7,
                "year": 2018
            },
            "enddate": {
                "month": 5,
                "year": 2022
            },
            "score": 3.77
        }
    }

    certificates = {
        "Certificate1": {
            "name": "AWS Certified Cloud Practitioner",
            "issuer": "Amazon Web Services",
            "date":"8 May 2024",
            "url": "https://cp.certmetrics.com/amazon/en/public/verify/credential/c0c0a58042ed466db3c2f9092a9a6c7c"
        },
        "Certificate2": {
            "name": "Graduate Certificate in Computational Data Science",
            "issuer": "Wichita State University",
            "date":"8 April 2024",
            "url": "link"
        }
    }

    job_description = """About the job
DAIN is seeking an exceptional AI Developer to help build the future of autonomous AI systems.

We're developing breakthrough technologies that will fundamentally transform how AI agents 

communicate and operate at scale.



Core Responsibilities:

•⁠ ⁠Architect and deploy sophisticated AI solutions using Anthropic, OpenAI, and Gemini 

APIs

•⁠ ⁠Implement advanced RAG techniques for enhanced model responses with real-time 

data

•⁠ ⁠Design scalable APIs and backend systems for seamless AI model integration

•⁠ ⁠Develop end-to-end solutions using TypeScript, React, and Node.js

•⁠ ⁠Optimize performance and implement robust error-handling for AI applications

•⁠ ⁠Collaborate across teams to integrate AI functionality into existing services

Required Qualifications:

•⁠ ⁠Proven experience building applications with OpenAI and/or Anthropic APIs

•⁠ ⁠Advanced TypeScript proficiency (frontend & backend)

•⁠ ⁠Strong Next.js expertise

•⁠ ⁠Deep understanding of LLMs, function calling, and RAG techniques

•⁠ ⁠Experience with agent frameworks (Langchain, GraphLang, Vercel AI SDK)

•⁠ ⁠Track record integrating enterprise-grade APIs

•⁠ ⁠Familiarity with automation platforms (Zapier, UiPath)

•⁠ ⁠Strong background in advanced AI concepts (memory architectures, knowledge graphs, 

embeddings)

•⁠ ⁠At least one shipped production-level AI application

•⁠ ⁠Intermediate to advanced cloud platform skills (AWS/Azure/GCP)

•⁠ ⁠Solid Git and CI/CD experience

Optional Skills:

•⁠ ⁠LLM fine-tuning experience

•⁠ ⁠SDK development in enterprise environments

•⁠ ⁠Advanced cloud architecture expertise"""

    prompt = """
    You are an expert resume tailor with deep knowledge of Applicant Tracking Systems (ATS), resume optimization, and modern hiring practices. Your task is to transform the provided resume content to perfectly match the job description while maintaining truthfulness and authenticity.

    ## INSTRUCTIONS:

    1. Analyze the job description carefully, identifying:
    - Required technical skills and keywords
    - Desired soft skills and competencies
    - Industry-specific terminology
    - Company values and culture indicators
    - Required years of experience and qualifications

    2. Review the provided resume content and restructure it to:
    - Prioritize relevant experience and skills that match the job requirements and skills from my experience and projects
    - Use exact keyword matches from the job description where truthful and appropriate
    - Quantify achievements with metrics (numbers, percentages, dollar amounts)
    - Focus on accomplishments rather than responsibilities
    - Ensure bullet points follow the STAR method (Situation, Task, Action, Result) or PAR method (Problem, Action, Result)

    3. Optimize content for ATS parsing:
    - Use strong action verbs to begin bullet points
    - Remove first-person pronouns
    - Ensure consistent tense (past tense for previous roles, present for current)
    - Eliminate irrelevant information
    - Tailor skills section to exactly match required and preferred skills

    4. Apply these essential resume best practices:
    - Create a compelling professional summary (4-5 lines) highlighting key qualifications
    - Limit experience descriptions to 4-5 impactful bullet points per role
    - Limit project descriptions to 4-5 impactful bullet points per project
    - Ensure all information is truthful and accurate
    - Emphasize recent (last 5-7 years) and relevant experience
    - Remove outdated technologies unless specifically requested

    ## CRITICAL RULES:

    - NEVER fabricate experience, qualifications, or skills
    - ALWAYS maintain truthfulness while optimizing presentation
    - Use industry-standard terminology
    - Keep all bullet points concise and focused (under 2 lines each)
    - Every bullet point should demonstrate value and impact, not just responsibilities

    ## RESPONSE FORMAT:

    You MUST return your response in the exact JSON format below. Do not include any explanations or text outside of this JSON structure:

    {
        "title": "Only the Job title as specified in job description",
        "summary": "Compelling professional summary tailored to the job description",
        "skills": ["# List of skills based on the above INSTRUCTIONS and skills from my projects and experience"],
        "Experience": {
            "Experience1": {
                "position": "Job title",
                "name": "Company name",
                "location": "City, State",
                "Start Date": {
                    "month": 1,
                    "year": 2020
                },
                "End Date": {
                    "month": 12,
                    "year": 2023
                },
                "info": [
                    "# Create 4-5 bullet points by following the above INSTRUCTIONS"
                ]
            },
            "Experience2": {
                "position": "Previous job title",
                "name": "Previous company name",
                "location": "City, State",
                "Start Date": {
                    "month": 1,
                    "year": 2018
                },
                "End Date": {
                    "month": 12,
                    "year": 2020
                },
                "info": [
                    "# Create 4-5 bullet points by following the above INSTRUCTIONS"
                ]
            }
        },
        "Projects": {
            "Project1": {
                "name": "Project name",
                "startdate": {
                    "month": 1,
                    "year": 2022
                },
                "enddate": {
                    "month": 6,
                    "year": 2022
                },
                "info": [
                    "# Create 4-5 bullet points by following the above INSTRUCTIONS"
                ]
            },
            "Project2": {
                "name": "Another project name",
                "startdate": {
                    "month": 8,
                    "year": 2021
                },
                "enddate": {
                    "month": 12,
                    "year": 2021
                },
                "info": [
                    "# Create 4-5 bullet points by following the above INSTRUCTIONS"
                ]
            }
        }
    }
    IMPORTANT: Ensure all date values are integers, not strings. The output MUST be valid JSON that can be parsed by standard JSON parsers. Maintain the exact structure shown above, including the exact naming of fields.
    """
    human_prompt = """
    INPUT:
    Job Description:
    {0}
    Current Resume Information:
    {1}
    """