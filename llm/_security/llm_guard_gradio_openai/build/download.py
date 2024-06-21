import os

from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import Anonymize, PromptInjection, TokenLimit, Toxicity
from llm_guard.output_scanners import Deanonymize, NoRefusal, Relevance, Sensitive
from llm_guard.vault import Vault

# Setup LLm Guard
vault = Vault()
input_scanners = [Anonymize(vault), Toxicity(), TokenLimit(), PromptInjection()]
output_scanners = [Deanonymize(vault), NoRefusal(), Relevance(), Sensitive()]

# Force load LLM as Judge models (already done in "make download")
dummy_prompt = "Dummy prompt"
sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, dummy_prompt)
sanitized_response_text, results_valid, results_score = scan_output(
    output_scanners, sanitized_prompt, dummy_prompt
)
