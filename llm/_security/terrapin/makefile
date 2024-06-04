SHELL := /bin/bash

# Torch based models (.bin) require online connection so transformers library
# convert them, you never can just download files for offline use
# MODEL=lysandre/arxiv-nlp
# MODEL_EXT=*.bin
# REVISION=refs/pr/1

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL_EXT=*.safetensors
REVISION=main

all: requirements install_python install required_python download run-offline-local size

code:
	poetry run code .

# run ----------------------------------------------------------------

run: run-offline-local

run-offline-local:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

# download ----------------------------------------------------------------

download: download-local-py

download-local:
	source env.txt && \
	HF_HOME='./.cache/huggingface/' \
	poetry run huggingface-cli download --token=$$HUGGINGFACE_TOKEN \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"

download-local-py:
	source env.txt && \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./build/model_download.py

# Generate requirements hashes and compile -----------------------------------------

compile:
	@mkdir -p bin && cd bin  && \
	time poetry run pyinstaller --onefile pyinstaller ../src/app.py

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

# Security ---------------------------------------------------

vulnerability-scan:
	trivy filesystem poetry.lock --scanners vuln

digest:
	@DIR="./.cache" && echo "Calculating hash of files in $$DIR"
	find $$DIR -type f -exec sha1sum "$$PWD"/{} \; 
	@DIR="./.cache" && echo "Calculating global hash of $$DIR"
	find $$DIR -type f \( -exec sha1sum "$$PWD"/{} \; \) | awk '{print $1}' | sort | sha1sum

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete: delete_venv delete_local_huggingface delete_bin

delete_venv:
	poetry env remove --all ||:

delete_local_huggingface:
	rm -r ./.cache/huggingface/hub ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of ./bin"
	@du -sh ./bin/ ||:
	@echo "Size of models in ./.cache/huggingface/"
	@du -sh ./.cache/huggingface/ ||:
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:
	@echo "Container images"
	@${RUNSUDO} docker image ls
