import os
import openai
import langchain
from dotenv import load_dotenv
from langchain.llms import OpenAI

from flask import Flask, request, jsonify

app = Flask(__name__)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def invoke(prompt):

    llm = OpenAI() # instantiate the model
    
    response = llm(prompt) # invoke OpenAI LLM

    print(response) # output the response
    
    return response


# Exposing the endpoint 
@app.route('/ask', methods=['POST'])
def ask():
    
    # Fetch the question from the user's request
    prompt = request.json.get('question')

    # Invoke the model function 
    response = invoke(prompt)

    # Return response
    return jsonify({"answer": response})


# Run the Flask app
if __name__ =='__main__':
    app.run(port=3000)
