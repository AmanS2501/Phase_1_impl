import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()  # Loads GROQ_API_KEY from .env

class GroqChatModel:
    def __init__(self, model_name="llama3-70b-8192", temperature=0):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY must be set in the .env file.")
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=1024,
            max_retries=2
        )
    def generate_response(self, messages):
        ai_response = self.llm.invoke(messages)
        return ai_response.content
