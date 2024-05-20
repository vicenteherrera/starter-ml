from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values('env.txt')
client = OpenAI(api_key=config["OPENAI_API_KEY"])

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", 
     "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": 
     "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message.content)