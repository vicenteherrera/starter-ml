from openai import OpenAI
from dotenv import dotenv_values
import os

config = next((dotenv_values(f"{p}env.txt") for p in ('', '../', '../../') if os.path.exists(f"{p}env.txt")), {})
client = OpenAI(api_key=config["OPENAI_API_KEY"])

system="You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."
user="Compose a poem that explains the concept of recursion in programming."

print("System message:")
print(system)
print("User message:")
print(user)

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": system},
    {"role": "user", "content": user}
  ]
)

print(completion.choices[0].message.content)
