from transformers import AutoTokenizer
import transformers
import torch
from dotenv import dotenv_values
import time

print("# Downloading model")

start_time = time.time()
config = dotenv_values('env.txt')
model_name = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(
  model_name,
  token=config["HUGGINGFACE_TOKEN"],
)

print("Loading model:", model_name)
loading_time = time.time()
if torch.cuda.device_count()==0:
  dtype = torch.float32
else:
  dtype = torch.float16   
pipeline = transformers.pipeline(
  "text-generation",
  model=model_name,
  torch_dtype=dtype,
  device_map="auto",
  token=config["HUGGINGFACE_TOKEN"],
)
print('Model loaded in:', (time.time() - loading_time), 'seconds')


print('Total execution time:', (time.time() - start_time), 'seconds')