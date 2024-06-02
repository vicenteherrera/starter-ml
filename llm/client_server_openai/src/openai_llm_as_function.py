import os
import openai
import langchain
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask(prompt):

    llm = OpenAI() # instantiate the model
    
    response = llm(prompt) # invoke OpenAI LLM

    print(response) # output the response
    
    return response


res = ask("What is BTC?")
print(res)

