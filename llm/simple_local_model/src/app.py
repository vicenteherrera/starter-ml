from transformers import AutoTokenizer
import transformers
import torch
from dotenv import dotenv_values
import time
import os

model_name = os.environ["MODEL"]
model_revision = os.environ["REVISION"]
# model_ext = os.environ["MODEL_EXT"]
print("Run model: " + model_name + ", revision: " + model_revision)

start_time = time.time()
config = next((dotenv_values(f"{p}env.txt") for p in ('', '../', '../../') if os.path.exists(f"{p}env.txt")), {})

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
if device.type == 'cuda':
    for i in range(torch.cuda.device_count()):
      print(f"CUDA GPU {i}: {torch.cuda.get_device_name(i)}")

tokenizer = AutoTokenizer.from_pretrained(
  model_name,
  revision=model_revision,
  token=config["HUGGINGFACE_TOKEN"],
)

print("Loading model:", model_name)
loading_time = time.time()
if not torch.cuda.is_available():
  dtype = torch.float32
else:
  dtype = torch.float16   
pipeline = transformers.pipeline(
  "text-generation",
  model=model_name,
  revision=model_revision,
  torch_dtype=dtype,
  device_map="auto",
  token=config["HUGGINGFACE_TOKEN"],
)
print('Model loaded in:', (time.time() - loading_time), 'seconds')

prompt="I like Galactica and The Expanse TV shows. Can you recomend me other different TV shows I may like in addition to these?\n"
print('Sending prompt:\n' , prompt)
prompt_time = time.time()
sequences = pipeline(
  prompt,
  do_sample=True,
  top_k=10,
  num_return_sequences=1,
  eos_token_id=tokenizer.eos_token_id,
  max_length=200,
)
for seq in sequences:
  print(f"Result: {seq['generated_text']}")
print('Answer generated in:', (time.time() - prompt_time), 'seconds')

prompt="How about some british shows?\n"
print('Sending prompt:\n' , prompt)
prompt_time = time.time()
sequences = pipeline(
  prompt,
  do_sample=True,
  top_k=10,
  num_return_sequences=1,
  eos_token_id=tokenizer.eos_token_id,
  max_length=200,
)
for seq in sequences:
  print(f"Result: {seq['generated_text']}")
print('Answer generated in:', (time.time() - prompt_time), 'seconds')

print('Total execution time:', (time.time() - start_time), 'seconds')