SHELL := /bin/bash

DIR=$(shell basename $$(pwd))
CONTAINER_IMAGE=quay.io/vicenteherrera/python-dev-shell
CONTAINER_TAG=3.11.7-${DIR}

CONFIG_FILE=$(shell for p in "config/env.txt" "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "") 

all: requirements install_python install required_python download size help

help:
	@echo ""
	@echo "HELP"
	@echo ""
	@echo "# Run Gradio UI with LLM Guard example"
	@echo "make run"
	@echo ""

run: config_exists
	poetry run python ./src/app-protected-no-streaming.py

code:
	poetry run code .

# requirements ----------------------------------------------------------------

requirements:
	which pyenv
	which poetry

config_exists:
	@CHECK="${CONFIG_FILE}" && \
	[ -z "$${CHECK// /}" ] && echo "Error: Config file env.txt not found" && exit 1 ||:
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

download:
	HF_HOME='./.cache/huggingface/' \
	poetry run python ./build/download.py 

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete: delete_venv

delete_venv:
	poetry env remove --all ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry run poetry env info --path 2>/dev/null)
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
	echo "Running container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	${RUNSUDO} docker run -it \
		-p 7860:7860 \
		-v $(shell realpath $$(pwd)/${CONFIG_FILE}):/home/user/$(shell basename $$(pwd))/config/env.txt \
		${CONTAINER_IMAGE}:${CONTAINER_TAG} bash -c "cd ${DIR} && make run"

container-push:
	@echo "Pushing container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	${RUNSUDO} docker push ${CONTAINER_IMAGE}:${CONTAINER_TAG}