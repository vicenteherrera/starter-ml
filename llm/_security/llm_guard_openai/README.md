# llm_guard_openai

Test LLM-Guard mitigations with an AI endpoint.

This example uses OpenAI for speed. First time you use an example with LLM-Guard, it has to download files for the models to detect prompt injections and other attacks.

## Preparation

Check the main [README.md](../../README.md) for generic prerequisites.

Copy `env-sample.txt` as `env.txt` and put your API keys there.

## Instructions

```bash
# Prepare all requirements, virtual environment, dependencies
make

# Run a query that discloses private information to AI endpoint service
make run-unprotected
# Run the same query, but filter through LLM-Guard to have it anonimized and deanonimize the response
make run-protected

# Run a query for an agent for a specific topic, where the prompt doesn't make the system prompt to deviate
make run-no-injection2
# Use prompt injection to succeed bypassing the system prompt, you may have to run several times
make run-unprotected2
# Use prompt injection, but be blocked by LLM-Guard detecting the attempt
make run-protected2
```


