import os
from openai import OpenAI
from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import Anonymize, PromptInjection, TokenLimit, Toxicity
from llm_guard.output_scanners import Deanonymize, NoRefusal, Relevance, Sensitive
from llm_guard.vault import Vault
from dotenv import dotenv_values

config = next((dotenv_values(f"{p}env.txt") for p in ('', '../', '../../', '../../../') if os.path.exists(f"{p}env.txt")), {})
client = OpenAI(api_key=config["OPENAI_API_KEY"])

vault = Vault()
input_scanners = [Anonymize(vault), Toxicity(), TokenLimit(), PromptInjection()]
output_scanners = [Deanonymize(vault), NoRefusal(), Relevance(), Sensitive()]

prompt = "Make an SQL insert statement to add a new user to our database. Name is Vicente Herrera. Email is vicenteherrera@vicenteherrera.com "
model = "gpt-3.5-turbo"
system_msg = "You are a helpful assistant."

sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, prompt)
if any(results_valid.values()) is False:
    print(f"Prompt {prompt} is not valid, scores: {results_score}")
    exit(1)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": sanitized_prompt},
    ],
    temperature=0,
    max_tokens=512,
)
response_text = response.choices[0].message.content
sanitized_response_text, results_valid, results_score = scan_output(
    output_scanners, sanitized_prompt, response_text
)
if any(results_valid.values()) is False:
    print(f"Output {response_text} is not valid and has been blocked, scores: {results_score}")
    exit(1)

print(f"Using OpenAI {model}\n")
print(f"# System message:\n{system_msg}\n")
print(f"# Output scores: {results_score}")
print(f"# Prompt:\n{prompt}\n")
print(f"# Sanitized Prompt:\n{sanitized_prompt}\n")
print(f"# Output:\n{response_text}\n")
print(f"# Sanitized Output:\n{sanitized_response_text}\n")
