import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import dotenv_values

CONFIG_FILE = os.getenv("CONFIG_FILE")
if CONFIG_FILE == None or CONFIG_FILE == "":
    CONFIG_FILE = "config/env.txt"

print(f"Using CONFIG_FILE={CONFIG_FILE}")

app = Flask(__name__)

config = dotenv_values(CONFIG_FILE)

if not "OPENAI_API_KEY" in config:
    print("OPENAI_API_KEY config not found")
    exit()

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
    app.run(host='0.0.0.0', port=3000)
