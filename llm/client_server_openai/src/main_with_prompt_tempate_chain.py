import os
import openai
import langchain
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI() # instantiate the model

# Another version of prompt template
movie_prompt_template = PromptTemplate(
    template="What is the synopsis of the movie {movie_name}",
    input_variables=["movie_name"]
)

# Let's create a chain
chain = LLMChain(llm=llm, prompt=movie_prompt_template)

# Execute the chain
response = chain.run("Avatar")

print(response) # output the response
