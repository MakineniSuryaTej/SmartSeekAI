import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI


load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env'))

def get_llm(llm_name="GPT3.5"):
    if llm_name == "GPT4o":
        return ChatOpenAI(model="gpt-4o")
    elif llm_name == "GPT4omini":
        return ChatOpenAI(model="gpt-4o-mini")
    else:
        return ChatOpenAI(model="gpt-3.5-turbo")
    
