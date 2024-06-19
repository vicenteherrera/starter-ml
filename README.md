
# starter-ml

Introductory examples for using Machine Learning, Large Language Modles (LLM) and making them secure.

## Examples

Each example has a `README.md` file explaining it. Continue reading down this page first for general instructions.

* [_utils](_utils): General utilities, like a container with PyEnv, Poetry and other binaries to use as an instant development shell.
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
    * [pickle](llm/_security/pickle): Shows how pickle binary data format can be insecure.
    * [simple_garak](llm/_security/simple_garak): Scan OpenAI and local models with Garak vuln analysis.
    * [llm_guard_openai](llm/_security/llm_guard_openai): Test LLM Guard mitigation with OpenAI endpoint.
    * [promptfoo](llm/_security/promptfoo): Security evaluation of LLM models.
    * [attestation](llm/_security/attestation): Simple attestation examples using sha1sum digest, gpg, cosign and CycloneDX.
    * [terrapin](llm/_security/terrapin): Model attestation using Terrapin.


## Prerequisites

### Containerized

You have the alternative to use a container image to navigate and test all the examples with all binary pre-requisites met. To do so, use:

bash
```bash
cd _utils
make container-run
```

Some examples have a container with their specific prerequisites installed, including in this case even local open source LLM (they are very big). Run them the same way:

bash
```bash
cd llm/_security/llm_guard_openai
make container-run
```

These containers are not built to be small or very safe, but to be very convenient to run the examples. To check an example containerization with minimal safe containers, check the examples [client_server_openai](llm/client_server_openai) and [containerize_model](llm/containerize_model).

### Install requirements

Most examples rely on `pyenv` and `poetry` and a fixed `poetry.lock` file to provide perfectly repeatable environments. Check the [starter-python](https://github.com/vicenteherrera/starter-python) repository on how to install these requirements.

Examples that download open source models from Huggingface [require git LFS to be installed](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage). By default they employ HTTPS, if you switch them to use SSH (more secure), you have to setup your public key in your Huggingface profile.

On Linux for some local models, before you install a specific Python version, you need to install the `libffi` package with: `sudo apt-get install libffi-dev`.

To run Jupyter server you have to install the `libsqlite3-dev` package. Check the troubleshooting section about that.

Some specific examples may require tools like `cosign`, Git LFS, Docker buildx, or npm. Check each individual example readme file.

## Using Visual Studio Code

When you open a terminal within _Visual Studio Code_, it tries to activate the virtual environment specified by Poetry at that directory. As this repo contains many Poetry definitions it may confuse VSCode. So if you plan to run commands through the Visual Studio Code terminal, it's best to open just the example directory with Code to do so. You can also try to `deactivate` an automatically loaded virtual environment in VSCode terminal.

## API Keys

Some examples download models from Huggingface, if you create a free account and [set up an API key token](https://huggingface.co/docs/hub/en/security-tokens), you will ensure you are not throttled when doing so.

Other examples require a paid [OpenAI](https://platform.openai.com/account/api-keys) API key, make sure you have introduced your payment method with them, and have bought some initial credits.

Copy `sample-env.txt` to `env.txt` and put your API keys there. You could do that on individual examples, or globally with an `env.txt` file on the parent directory where you put all your API keys. Although the file specifies variables prefixing them with `export`, when possible most of the examples don't load them into the environment, but process the file and pick the value to be passed to corresponding function calls.

## Running examples

All examples have a `makefile` with several targets, most of the time just executing `make` will setup and install everything, as well as execute the main example in the directory, or print help on further commands.

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
* Reinstall afterwards the PyEnv Python version in the project folder with:

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
