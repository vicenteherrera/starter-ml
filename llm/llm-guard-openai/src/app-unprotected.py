import os

from openai import OpenAI

from dotenv import dotenv_values

config = dotenv_values('env.txt')
client = OpenAI(api_key=config["OPENAI_API_KEY"])

prompt = "Make an SQL insert statement to add a new user to our database. Name is Vicente Herrera. Email is vicenteherrera@vicenteherrera.com "



response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
    max_tokens=512,
)
response_text = response.choices[0].message.content


print(f"# Prompt:\n{prompt}\n")
print(f"# Output:\n{response_text}\n")