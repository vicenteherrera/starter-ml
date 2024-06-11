import os

from openai import OpenAI

from dotenv import dotenv_values

config = dotenv_values('env.txt')
client = OpenAI(api_key=config["OPENAI_API_KEY"])

model = "gpt-3.5-turbo"
prompt = "Tell me a summary of the history of the roman empire in ten phrases."
system_msg = "You are a helpful assistant. Do not respond any question that is unrelated to programming or artificial intelligence. If there is a question unrelated to those topics, simply answer you know nothing about that."

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