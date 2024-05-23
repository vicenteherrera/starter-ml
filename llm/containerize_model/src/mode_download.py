# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

# PyTorch model
# model_name = "lysandre/arxiv-nlp"

#SafeTensor model
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# from transformers import pipeline
# pipe = pipeline("text-generation", model="lysandre/arxiv-nlp")