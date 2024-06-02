# Import the required libraries
import streamlit as st
from phi.assistant import Assistant
from phi.tools.hackernews import HackerNews
from phi.llm.openai import OpenAIChat
from dotenv import dotenv_values
import os

# Based on: https://github.com/Shubhamsaboo/awesome-llm-apps/blob/main/multi_agent%2Fresearch_agent.py
# https://openai.com/index/disrupting-deceptive-uses-of-AI-by-covert-influence-operations/

def __main__():

    # Set OpenAI API key
    config = dotenv_values('env.txt')
    os.environ["OPENAI_API_KEY"] = config['OPENAI_API_KEY']
    # If we try to pass the key as a parameter, some internal calls are made without it and it fails.
    # Setting it as environment guarantees that every call uses the api key.

    # Set up the Streamlit app
    st.title("Multi-Agent AI Researcher 🔍🤖")
    st.caption("This app allows you to research top stories and users on HackerNews and write blog posts, reports and social posts on that.")

    # Create instances of the Assistant
    story_researcher = Assistant(
        name="HackerNews Story Researcher",
        role="Researches hackernews stories and users.",
        tools=[HackerNews()],
    )

    user_researcher = Assistant(
        name="HackerNews User Researcher",
        role="Reads articles from URLs.",
        tools=[HackerNews()],
    )

    hn_assistant = Assistant(
        name="Hackernews Team",
        team=[story_researcher, user_researcher],
        llm=OpenAIChat(
            model="gpt-4o",
            max_tokens=1024,
            temperature=0.5
        )
    )

    # Input field for the report query
    query = st.text_input("Enter your report query")

    if query:
        # Get the response from the assistant
        response = hn_assistant.run(query, stream=False)
        st.write(response)

if __name__ == '__main__':
  __main__()