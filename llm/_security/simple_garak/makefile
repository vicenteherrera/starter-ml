SHELL := /bin/bash

# Using poetry

all: requirements install_python install help

help:
	@echo ""
	@echo "HELP"
	@echo "Evaluate 'Do Anything Now' probes on local GPT2 open source model from Huggingface:"
	@echo "make run-hg-gpt2"
	@echo "Evaluate 'Do Anything Now' probes on OpenAI GPT-3.5-turbo:"
	@echo "make run-oa-gpt3.5-turbo"

run-hg-gpt2:
	source "$$(for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	HF_HOME='./.cache/huggingface' \
	poetry run garak --model_type huggingface --model_name gpt2 --probes dan

run-oa-gpt3.5-turbo:
	source "$$(for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	HF_HOME='./.cache/huggingface' \
	poetry run garak --model_type openai --model_name gpt-3.5-turbo --probes dan

list-probes:
	poetry run garak --list_probes

# Using pipx

install_garak:
	pipx install garak

garak-hg-gpt2:
	source "$$(for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	HF_HOME='./.cache/huggingface' \
	garak --model_type huggingface --model_name gpt2 --probes dan

garak-oa-gpt3.5-turbo:
	source "$$(for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	HF_HOME='./.cache/huggingface' \
	garak --model_type openai --model_name gpt-3.5-turbo --probes dan


# requirements ----------------------------------------------------------------

requirements:
	which pyenv
	which poetry

install_python: upgrade_pyenv
	pyenv install $$(cat .python-version) -s

upgrade_pyenv:
	cd $$HOME/.pyenv && git pull

required_python:
	@PVPOETRY="$$(poetry run python --version)" && \
	PVPOETRY=$${PVPOETRY#"Python "} && \
	PV="$$(cat .python-version)" && \
	if [ "$$PVPOETRY" != "$$PV" ]; then \
		echo "**Error, Python version mismatch" && \
		echo ".python-version file: $$PV" && \
		echo "poetry run python --version: $$PVPOETRY" && \
		echo "Run make refresh and check your pyenv path configuration" && \
		exit 1; \
	fi

refresh: delete_venv
	pyenv uninstall -f $$(cat .python-version)
	pyenv install $$(cat .python-version)
	rm poetry.lock
	poetry install --no-root

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete: delete-venv delete-huggingface-home

delete-venv:
	poetry env remove --all ||:

delete-huggingface-home:
	rm -r $$HOME/.cache/huggingface/ ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/ ||:
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:

