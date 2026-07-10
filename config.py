import os

from dotenv import load_dotenv

from crewai import LLM


load_dotenv()


llm = LLM(

    model=f'ollama/{os.getenv("MODEL")}',

    base_url="http://localhost:11434"

)
