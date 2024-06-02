import os
import openai
import langchain
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI() # instantiate the model

# A simple version of prompt template
prompt_template = PromptTemplate.from_template("What is BTC")
response = llm(prompt_template.format()) # invoke OpenAI LLM
print(response) # output the response

# Another version of prompt template
movie_prompt_template = PromptTemplate(
    template="What is the synopsis of the movie {movie_name}",
    input_variables=["movie_name"]
)
movie_prompt = movie_prompt_template.format(movie_name="The Godfather")

response2 = llm(movie_prompt)

print(response2) # output the response
