from transformers import AutoTokenizer
import transformers
import torch
import time
import os

def __main__():

  model_name = os.environ["MODEL"]
  model_revision = os.environ["REVISION"]

  print("# Executing model '" + model_name + "' revision '" + model_revision + "'")

  start_time = time.time()

  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  print('Using device:', device)
  if device.type == 'cuda':
      for i in range(torch.cuda.device_count()):
        print(f"CUDA GPU {i}: {torch.cuda.get_device_name(i)}")

  tokenizer = AutoTokenizer.from_pretrained(model_name, revision=model_revision)

  print("Loading model:", model_name)
  loading_time = time.time()
  dtype = torch.float16 if torch.cuda.is_available() else torch.float32 
  pipeline = transformers.pipeline(
    "text-generation", model=model_name, revision=model_revision
    torch_dtype=dtype, device_map="auto",
  )
  print('Model loaded in:', (time.time() - loading_time), 'seconds')

  prompt="What are the best papers on AI security?\n"
  print('Sending prompt:\n' , prompt)
  prompt_time = time.time()
  sequences = pipeline(
    prompt, do_sample=True, top_k=10,
    num_return_sequences=1, max_length=200,
    eos_token_id=tokenizer.eos_token_id,
  )
  for seq in sequences:
    print(f"Result: {seq['generated_text']}")
  print('Answer generated in:', (time.time() - prompt_time), 'seconds')

  print('Total execution time:', (time.time() - start_time), 'seconds')

if __name__ == '__main__':
  __main__()