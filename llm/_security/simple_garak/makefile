SHELL := /bin/bash

# MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL=gpt2
MODEL_EXT=*.safetensors
REVISION=main

DIR=$(shell basename $$(pwd))
CONTAINER_IMAGE=quay.io/vicenteherrera/python-dev-shell
CONTAINER_TAG=3.11.7-${DIR}

CONFIG_FILE=$(shell for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "")

all: requirements install_python install required_python download help

help:
	@echo ""
	@echo "HELP"
	@echo ""
	@echo "# Evaluate 'Do Anything Now' probes"
	@echo ""
	@echo "# On local open source model ${MODEL} from Huggingface:"
	@echo "make run-hg"
	@echo ""
	@echo "# On OpenAI GPT-3.5-turbo:"
	@echo "make run-oa-gpt3.5-turbo"
	@echo ""

run-hg: config_exists
	source "${CONFIG_FILE}" && \
	HF_HOME='./.cache/huggingface' \
	poetry run garak --model_type huggingface --model_name ${MODEL} --probes dan

run-oa-gpt3.5-turbo: config_exists
	source "${CONFIG_FILE}" && \
	HF_HOME='./.cache/huggingface' \
	poetry run garak --model_type openai --model_name gpt-3.5-turbo --probes dan

list-probes:
	poetry run garak --list_probes

download: download-local

download-local: config_exists
	source "${CONFIG_FILE}" && \
	HF_HOME='./.cache/huggingface/' \
	poetry run huggingface-cli download --token=$$HUGGINGFACE_TOKEN \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"

# requirements ----------------------------------------------------------------

requirements:
	which pyenv
	which poetry

config_exists:
	@[ ! -z "${CONFIG_FILE}" ] || ( echo "Error: Config file env.txt not found" && exit 1 )
	@echo "Config file found at ${CONFIG_FILE}"

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

# Container targets ------------------------------------------

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

container-build:
	@echo "Building container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	${RUNSUDO} docker build . -f build/containerfile_dev \
		--build-arg DIR=${DIR} \
		--build-arg USER_ID="$$(id -u)" \
		-t ${CONTAINER_IMAGE}:${CONTAINER_TAG}
	${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:${CONTAINER_TAG}

container-run: config_exists
	@echo "Running container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	@${RUNSUDO} docker run -it \
		-v "$$(pwd)/${CONFIG_FILE}":/home/user/"$$(basename $$(pwd))"/env.txt \
		${CONTAINER_IMAGE}:${CONTAINER_TAG} bash -c "cd ${DIR} && make help && /bin/bash"

container-run-dev:
	@echo "Running container image with local dir mounted ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	@${RUNSUDO} docker run \
		-v "$$(pwd)":/home/user/"$$(basename $$(pwd))" \
		-u $$(id -u):$$(id -g) \
		-it \
		${CONTAINER_IMAGE}:${CONTAINER_TAG}

container-push:
	@echo "Pushing container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	${RUNSUDO} docker push ${CONTAINER_IMAGE}:${CONTAINER_TAG}
