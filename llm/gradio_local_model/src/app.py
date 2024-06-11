import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import gradio as gr
from dotenv import dotenv_values
import os

# Based on: https://insights.sei.cmu.edu/blog/creating-a-large-language-model-application-using-gradio/

config = next((dotenv_values(f"{p}env.txt") for p in ('', '../', '../../') if os.path.exists(f"{p}env.txt")), {})

model="togethercomputer/RedPajama-INCITE-Chat-3B-v1" # Model
dtype = torch.float16 if torch.cuda.is_available() else torch.float32 # Set precision based on CPU or GPU available
tokenizer = AutoTokenizer.from_pretrained(model, token=config["HUGGINGFACE_TOKEN"])
model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=dtype, token=config["HUGGINGFACE_TOKEN"])

# Process question from user through model
def ask(text):
  inputs = tokenizer(text, return_tensors='pt').to(model.device)
  input_length = inputs.input_ids.shape[1]
  outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.7, do_sample=True,
                           return_dict_in_generate=True)
  tokens = outputs.sequences[0, input_length:]
  print(tokenizer.decode(tokens))
  return tokenizer.decode(tokens)

# Gradio interface
with gr.Blocks() as server:
  with gr.Tab("LLM Inferencing"):
    model_input = gr.Textbox(label="Your Question:", 
                             value="What's the most famous fantasy book?", interactive=True)
    ask_button = gr.Button("Ask")
    model_output = gr.Textbox(label="The Answer:", 
                              interactive=False, value="Answer goes here...")
  ask_button.click(ask, inputs=[model_input], outputs=[model_output])

server.launch()
