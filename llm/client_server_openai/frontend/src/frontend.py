import streamlit as st
import requests
import os

SERVER_URL = os.getenv("SERVER_URL")
if SERVER_URL == None or SERVER_URL == "":
    SERVER_URL = "http://127.0.0.1:3000/ask"
print(f"Using SERVER_URL={SERVER_URL}")

# Streamlit header
st.header("Got a question for me?")
user_question = st.text_input("Ask your question:")

# Function to ask user a question and get an answer from the microservice
def ask_user():
    if user_question:
        # Call the Flask API endpoint to get the answer
        response = requests.post(
            SERVER_URL,
            json={"question": user_question}
        )
        answer = response.json().get("answer", "No answer found.")
        st.write(answer)

# Main function
if __name__ == '__main__':
    ask_user()
