SHELL := /bin/bash

DIR=$(shell basename $$(pwd))
CONTAINER_IMAGE=quay.io/vicenteherrera/python-dev-shell
CONTAINER_TAG=3.11.7-${DIR}

CONFIG_FILE=$(shell for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "")

# Using poetry

all: requirements install_python install required_python help

run: help

help:
	@echo ""
	@echo "HELP"
	@echo ""
	@echo "# Create compromised pickle file"
	@echo "make run-save-compromise"
	@echo ""
	@echo "# Load compromised pickle file that reveals secret"
	@echo "make run-load-compromise"
	@echo ""
	@echo "# Examine compromised pickle file without loading or running"
	@echo "make run-pickletools"
	@echo ""

run-pickletools:
	poetry run python -m pickletools data/compromise.bin

run-save-compromise:
	poetry run python ./src/save-compromise.py
	ls data -la

run-load-compromise:
	poetry run python ./src/load-compromise.py

run-save-array:
	poetry run python ./src/save.py
	ls data -la

run-save-pandas:
	poetry run python ./src/save-pandas.py
	ls data -la

run-save-model:
	poetry run python ./src/save-model.py
	ls data -la

run-load-array:
	poetry run python ./src/load.py

run-load-pandas:
	poetry run python ./src/load-pandas.py

run-load-model:
	poetry run python ./src/load-model.py



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
