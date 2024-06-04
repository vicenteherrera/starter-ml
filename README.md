
# starter-ml

Introductory examples for using Machine Learning, Large Language Modles (LLM) and making them secure.

## Examples

Each example has a README.md file explaining it. Continue reading here first for general instructions.

* [devpi](llm/devpi): Use `devpi` to cache and serve PiPY packages locally.
* [jupyter_ml](llm/jupyter_ml): Lightweight way to use Jupyter Notebooks locally
* llm.
  * [simple_openai](llm/simple_openai): Call OpenAI endpoint with prompt
  * [simple_local_model](llm/simple_local_model): Download and call local LLM with prompt
  * [rag_langchain_openai](llm/rag_langchain_openai): Prepare document for Retrieval Augmented Generation (RAG) in a vector DB and prompt it using OpenAI.
  * [gradio_openai](llm/gradio_openai): Use OpenAI with custom Gradio chat UI.
  * [gradio_local_model](llm/gradio_local_model): Use local LLM with custom Gradio chat UI.
  * [streamlit_openai_agents](llm/streamlit_openai_agents): Use several agents to employ tools with OpenAI.
  * [containerize_model](llm/containerize_model): Create the most secure and slimmest container for a local model.
  * [client_server_openai](llm/client_server_openai): Create a server LLM endpoint for OpenAI, and a client to connect to it using Streamlit chat UI.
  * _security
    * [simple_garak](llm/_security/simple_garak): Scan OpenAI and local models with Garak vuln analysis.
    * [llm_guard_openai](llm/_security/llm_guard_openai): Test LLM Guard mitigation with OpenAI endpoint.

## Prerequisites

The examples make extensive use of `pyenv` and `poetry` to achieve repeatible environments. Check the [starter-python](https://github.com/vicenteherrera/starter-python) repository on how to install these requirements.

All examples except `simple_openai` rely on `pyenv` and `poetry` and a fixed `poetry.lock` file to provide perfectly repeatable environments. When you open a terminal within _Visual Studio Code_, it tries to activate the virtual environment. As this project has many virtual environments if you install all of them, it may confuse it, so if you plan to run commands through the Visual Studio Code terminal, it's best to open just the example directory with Code to do so.

On Linux for some local models, before you install a specific Python version, you need to install the `libffi` package with: `sudo apt-get install libffi-dev`.

Examples have a `makefile` with several targets, most of the time just executing `make` will setup and install everything, as well as execute the main example in the directory.


## API Keys:

Some examples download models from Huggingface, if you create a free account and [setup an API key token](https://huggingface.co/docs/hub/en/security-tokens), you will ensure you are not throttled when doing so.

Other examples require a paid [OpenAI](https://platform.openai.com/account/api-keys
) API key, make sure you have introduced your payment methond with them, and have bought some initial credits.



## Troubleshooting

### libcudnn.so

```console
libcudnn.so.8: cannot open shared object file: No such file or directory
```
* Make sure to install the latest `torch` library that works with CUDA driver on Windows native or WSL.
* Despite what you read elsewhere, you must not install any NVIDIA GPU Linux driver within WSL 2 for Windows, the native Windows driver will handle things.

### _ctypes

```console
ModuleNotFoundError: No module named '_ctypes'
```
* You have to install `libffi-devel` before installing the specific python version
  `sudo apt-get install libffi-dev`  
* Reinstall after that the PyEnv Python version in the project folder with:
```console
pyenv uninstall $(cat .python-version)
pyenv install $(cat .python-version)
```

### Errors while installing a specific Python version with PyEnv

On Linux, if some prerequisite libraries like bz2, lza, tkinter, etc are not present, you will see some error messages while installing a specific Python version. But as these examples do not use them, everything will work. In case you want them check [starter-python](https://github.com/vicenteherrera/starter-python) repository for instructions
