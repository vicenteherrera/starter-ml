# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

model_name = os.environ["MODEL"]
model_revision = os.environ["REVISION"]
# model_ext = os.environ["MODEL_EXT"]

# https://stackoverflow.com/questions/64001128/load-a-pre-trained-model-from-disk-with-huggingface-transformers
# cache_dir=YOURPATH, local_files_only=True

tokenizer = AutoTokenizer.from_pretrained(model_name, revision=model_revision)
model = AutoModelForCausalLM.from_pretrained(model_name, revision=model_revision)

