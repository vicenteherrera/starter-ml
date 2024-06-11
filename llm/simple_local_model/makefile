SHELL := /bin/bash

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL_EXT=*.safetensors
REVISION=main

all: requirements install_python install required_python download run size

code:
	poetry run code .

# run ----------------------------------------------------------------

run: run-offline-local

run-online-local:
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

run-offline-local:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

# download ----------------------------------------------------------------

download: download-local

download-local:
	source "$$(for p in "env.txt" "../env.txt" "../../env.txt"; do [[ -f "$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	HF_HOME='./.cache/huggingface/' \
	poetry run huggingface-cli download --token=$$HUGGINGFACE_TOKEN \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"

download-local-py:
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./build/model_download.py

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

delete: delete_venv delete_huggingface_home

delete_venv:
	poetry env remove --all ||:

delete_huggingface_local:
	rm -r ./.cache/huggingface/ ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/ ||:
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:
