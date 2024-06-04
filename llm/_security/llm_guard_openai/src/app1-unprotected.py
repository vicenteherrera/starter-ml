import os

from openai import OpenAI

from dotenv import dotenv_values

config = dotenv_values('env.txt')
client = OpenAI(api_key=config["OPENAI_API_KEY"])

prompt = "Make an SQL insert statement to add a new user to our database. Name is Vicente Herrera. Email is vicenteherrera@vicenteherrera.com "
model = "gpt-3.5-turbo"
system_msg = "You are a helpful assistant."

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
    max_tokens=512,
)
response_text = response.choices[0].message.content

print(f"Using OpenAI {model}\n")
print(f"# System message:\n{system_msg}\n")
print(f"# Prompt:\n{prompt}\n")
print(f"# Output:\n{response_text}\n")
