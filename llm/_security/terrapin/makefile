SHELL := /bin/bash

# Torch based models (.bin) require online connection so transformers library
# convert them, you never can just download files for offline use
# MODEL=lysandre/arxiv-nlp
# MODEL_EXT=*.bin
# REVISION=refs/pr/1

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL_EXT=*.safetensors
REVISION=main

DIR=$(shell basename $$(pwd))
CONTAINER_IMAGE=quay.io/vicenteherrera/python-dev-shell
CONTAINER_TAG=3.11.7-${DIR}

CONFIG_FILE=$(shell for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "")

all: requirements install_python install required_python download clone-build-terrapin size help

help:
	@echo ""
	@echo "HELP"
	@echo ""
	@echo "# Create attestation digest file"
	@echo "make run-create-terrapin-attest"
	@echo ""
	@echo "# Validate attestation digest file"
	@echo "make run-validate-terrapin-attest"
	@echo ""

code:
	poetry run code .

clone-build-terrapin:
	rm -rf ./terrapin-go
	git clone --depth 1 https://github.com/fkautz/terrapin-go.git
	cd terrapin-go && git fetch --depth 1 origin d97e69f43a2170e42cb7b79671111d65bc53bf13
	cd terrapin-go && git checkout d97e69f43a2170e42cb7b79671111d65bc53bf13
	cd terrapin-go && go build -o ../terrapin ./cmd/terrapin
	rm -rf ./terrapin-go

# run ----------------------------------------------------------------

run: run-offline-local

run-offline-local:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

# Set model main file as an example, you should loop through all files
MODEL_FILE=.cache/huggingface/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/fe8a4ea1ffedaf415f4da2f062534de366a451e6/model.safetensors

run-create-terrapin-attest:
	@echo "Creating attestation for ${MODEL_FILE}"
	./terrapin attest \
			-input "${MODEL_FILE}" \
			-output attestations/model.safetensors.attestation

run-validate-terrapin-attest:
	@echo "Validating attestation for ${MODEL_FILE}"
	./terrapin validate \
    -input "${MODEL_FILE}" -attestations \
    attestations/model.safetensors.attestation

# download ----------------------------------------------------------------

download: download-local-py

download-local:
	source "${CONFIG_FILE}" ||: && \
	HF_HOME='./.cache/huggingface/' \
	poetry run huggingface-cli download --token=$$HUGGINGFACE_TOKEN \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"

download-local-py:
	source "${CONFIG_FILE}" ||: && \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./build/model_download.py

# requirements ----------------------------------------------------------------

requirements:
	which pyenv
	which poetry
	which go

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

delete: delete_venv delete_local_huggingface delete_terrapin

delete_venv:
	poetry env remove --all ||:

delete_local_huggingface:
	rm -r ./.cache/huggingface/hub ||:

delete_terrapin:
	rm -rf ./terrapin-go

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of ./bin"
	@du -sh ./bin/ ||:
	@echo "Size of models in ./.cache/huggingface/"
	@du -sh ./.cache/huggingface/ ||:



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
