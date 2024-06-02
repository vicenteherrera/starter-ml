import os
import openai
import langchain
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI() # instantiate the model

prompt = "What is BTC" # create the prompt

response = llm(prompt) # invoke OpenAI LLM

print(response) # output the response
