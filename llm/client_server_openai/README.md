# client_server_openai

Create a server LLM endpoint for OpenAI, and a client to connect to it using Streamlit chat UI.

## Architecture

[ backend ] :3000 <-- [ frontend ] :8501 <-- [ browser ]

* Backend:
  * Connects to OpenAI endpoint
  * Exposes backend:3000/ask
* Fronted:
  * Connects to backend:3000/ask
  * UI with Streamlit
  * Exposes web UI at frontend:8501

## Prerequisites

Copy `env-sample.txt` to `env.txt` in the root of this repo (in this example you can't place it this example's directory), and include your OpenAI API key there.

## How to run

```bash
# Using docker compose
make compose-up

# Using Kubernetes
cd k8s && make

# Using containers
cd backend && make container-build container-run
cd frontend && make container-build container-run

# Using each dir project
cd backend && make run
cd frontend && make run
```

## More information

Based on: 
* https://github.com/madhusudhankonda/langchain-play
* https://mkonda007.medium.com/developing-llm-based-applications-client-server-answer-bot-aab54469879d