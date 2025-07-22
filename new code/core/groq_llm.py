import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class GroqLLM:
    def __init__(self, model_name="llama3-70b-8192", temperature=0):
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=1024,
            max_retries=2
        )

    def generate(self, messages):
        return self.llm.invoke(messages).content
