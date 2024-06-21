# gradio_openai

Use OpenAI with custom Gradio chat UI

# llm_guard_openai

Test LLM-Guard mitigations with an AI endpoint.

Example with a Gradio user interface. This example uses OpenAI for speed. 


## Preparation

To run containerized version with all requirements met, Copy `env-sample.txt` as `env.txt` and put your API key there. Then execute:

```bash
make container-run
```

To manually run locally, check the main [README.md](../../README.md) for generic prerequisites.  Then execute:

```bash
# Prepare prerequisites, virtual environment, download LLM Guard models
make

# Run the Gradio server
make run
```

## Instructions

Different GPT models can be selected, but the prompt injection example provided is a very simple one that will only work on the default model.

The interface offers pre-filled examples for:
* Sending PII (private identifier infornation) to the inference endpoint
* Trying to answer out of context question
* A very simple prompt injection

Check [LLM Guard documentation](https://llm-guard.com/input_scanners/anonymize/) for more information on input and output scanners.
