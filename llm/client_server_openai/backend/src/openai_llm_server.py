import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from flask import Flask, request, jsonify

from dotenv import dotenv_values

app = Flask(__name__)

config = next((dotenv_values(f"{p}env.txt") for p in ('', '../', '../../', '../../../') if os.path.exists(f"{p}env.txt")), {})


llm = OpenAI(api_key=config["OPENAI_API_KEY"])

def invoke(prompt):
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
