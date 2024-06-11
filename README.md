
# starter-ml

Introductory examples for using Machine Learning, Large Language Modles (LLM) and making them secure.

## Examples

Each example has a `README.md` file explaining it. Continue reading down this page first for general instructions.

* [_utils](_utils): General utilities, like a container with PyEnv and Poetry to use as an instant development shell.
* [devpi](llm/devpi): Use `devpi` to cache and serve PiPY packages locally.
* [jupyter_ml](llm/jupyter_ml): Lightweight way to use Jupyter Notebooks locally.
* **llm (Large Language Models)**
  * [simple_openai](llm/simple_openai): Call OpenAI endpoint with prompt.
  * [simple_local_model](llm/simple_local_model): Download and call local LLM with prompt.
  * [rag_langchain_openai](llm/rag_langchain_openai): Prepare document for Retrieval Augmented Generation (RAG) in a vector DB and prompt it using OpenAI.
  * [gradio_openai](llm/gradio_openai): Use OpenAI with custom Gradio chat UI.
  * [gradio_local_model](llm/gradio_local_model): Use local LLM with custom Gradio chat UI.
  * [streamlit_openai_agents](llm/streamlit_openai_agents): Use several agents to employ tools with OpenAI.
  * [containerize_model](llm/containerize_model): Create the most secure and slimmest container for a local model.
  * [client_server_openai](llm/client_server_openai): Create a server LLM endpoint for OpenAI, and a client to connect to it using Streamlit chat UI.
  * _security
    * [simple_garak](llm/_security/simple_garak): Scan OpenAI and local models with Garak vuln analysis.
    * [llm_guard_openai](llm/_security/llm_guard_openai): Test LLM Guard mitigation with OpenAI endpoint.
    * [terrapin](llm/_security/terrapin): Model attestation using Terrapin.

## Prerequisites

All examples except `simple_openai` rely on `pyenv` and `poetry` and a fixed `poetry.lock` file to provide perfectly repeatable environments. Check the [starter-python](https://github.com/vicenteherrera/starter-python) repository on how to install these requirements. 

When you open a terminal within _Visual Studio Code_, it tries to activate the virtual environment. As this project has many virtual environments if you install all of them, it may confuse it, so if you plan to run commands through the Visual Studio Code terminal, it's best to open just the example directory with Code to do so.

On Linux for some local models, before you install a specific Python version, you need to install the `libffi` package with: `sudo apt-get install libffi-dev`.

To run Jupyter you have to install `libsqlite3-dev`. Check the troubleshooting section about that.

You have the alternative to use a container image to navigate and test the examples, use `cd _utils ; make`. 

## API Keys:

Some examples download models from Huggingface, if you create a free account and [setup an API key token](https://huggingface.co/docs/hub/en/security-tokens), you will ensure you are not throttled when doing so.

Other examples require a paid [OpenAI](https://platform.openai.com/account/api-keys) API key, make sure you have introduced your payment methond with them, and have bought some initial credits.

Copy `sample-env.txt` to `env.txt` and put your API keys there. You could do that on individual examples, or globaly with a `env.txt` file on the parent directory where you put all your API keys. Although the file specifies variables prefixing them with `export`, when possible most of the example don't load them into the environment, but process the file and picks the value to be passed to corresponding function calls.

## Running examples

All examples have a `makefile` with several targets, most of the time just executing `make` will setup and install everything, as well as execute the main example in the directory.


## Troubleshooting

### libcudnn.so

```
libcudnn.so.8: cannot open shared object file: No such file or directory
```
* Make sure to install the latest `torch` library that works with CUDA driver on Windows native or WSL.
* Despite what you read elsewhere, you must not install any NVIDIA GPU Linux driver within WSL 2 for Windows, the native Windows driver will handle things.

### _ctypes

```
ModuleNotFoundError: No module named '_ctypes'
```
* You have to install `libffi-devel` before installing the specific python version
  `sudo apt-get install libffi-dev`  
* Reinstall after that the PyEnv Python version in the project folder with:

```bash
pyenv uninstall $(cat .python-version)
pyenv install $(cat .python-version)
```

### ModuleNotFoundError: No module named 'pysqlite2'

If you get this error, probably while running Jupyter, you need to install Sqlite before installing the specific Python version with PyEnv:

```bash
sudo apt-get install libsqlite3-dev
```

If you already had Python installed, you can reinstall it after you update this package, and rebuild the virtual environment with the new binary using:

```bash
make refresh
```


### Errors while installing a specific Python version with PyEnv

On Linux, if some prerequisite libraries like bz2, lza, tkinter, etc are not present, you will see some error messages while installing a specific Python version. But as these examples do not use them, everything will work. In case you want them check [starter-python](https://github.com/vicenteherrera/starter-python) repository for instructions.
