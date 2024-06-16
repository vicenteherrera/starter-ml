SHELL := /bin/bash

# Torch based models (.bin) require online connection so transformers library
# convert them, you never can just download files for offline use
# MODEL=lysandre/arxiv-nlp
# MODEL_EXT=*.bin
# REVISION=refs/pr/1

#  "stabilityai/stable-diffusion-2-1", revision="refs/pr/22", use_safetensors=True

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
COMMIT=ce0c99637bf2aba3265ec4675b50eadb26ac5a21
MODEL_DIR=./.cache/huggingface/hub/${MODEL}

CONTAINER_IMAGE=quay.io/vicenteherrera/llm-test

CONFIG_FILE=$(shell for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "")


all: requirements install_python install required_python download size

help:
	@echo ""
	@echo "HELP"
	@echo ""
	@echo "# Prepare local requirements"
	@echo "make"
	@echo ""
	@echo "# Run model locally"
	@echo ""
	@echo "make run"
	@echo ""
	@echo "# Run container with code, mount local folder with model"
	@echo "make container-run-no-model"
	@echo ""


code:
	poetry run code .

# run ----------------------------------------------------------------

run: run-offline-local

run-offline-local:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL_DIR="${MODEL_DIR}" \
	poetry run python ./src/app.py

run-offline-local-bin:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL_DIR="${MODEL_DIR}" \
	./bin/dist/app

# download ----------------------------------------------------------------

download: download-local-git-https

download-local-git-ssh: config_exists
	@make -s git-prepare
	git clone --depth 1 git@hf.co:${MODEL} "${MODEL_DIR}"
	@make -s git-finish

download-local-git-https: config_exists
	@make -s git-prepare
	git clone --depth 1 https://huggingface.co/${MODEL} "${MODEL_DIR}"
	@make -s git-finish

git-prepare: config_exists
	@echo "Cloning ${MODEL} commit ${COMMIT}"
	git lfs install
	rm -rf "${MODEL_DIR}"

git-finish:
	cd "${MODEL_DIR}" && \
	git fetch --depth 1 origin "${COMMIT}" && \
	git -c advice.detachedHead=false checkout "${COMMIT}"
	rm -rf "${MODEL_DIR}"/.git

# Generate requirements hashes and compile -----------------------------------------

generate-base-req:
	@poetry run pip-compile --generate-hashes base_requirements/poetry.in -o base_requirements/poetry.out
	@poetry run pip-compile --generate-hashes base_requirements/pyinstaller.in -o base_requirements/pyinstaller.out
	@poetry run pip-compile --generate-hashes base_requirements/nuitka.in -o base_requirements/nuitka.out

compile:
	@mkdir -p bin && cd bin  && \
	time poetry run pyinstaller --onefile pyinstaller ../src/app.py

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

delete_huggingface:
	rm -r $$HOME/.cache/huggingface/hub ||:

delete_bin:
	rm -r ./bin/*

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of ./bin"
	@du -sh ./bin/ ||:
	@echo "Size of models in ./.cache/huggingface/"
	@du -sh ./.cache/huggingface/ ||:
	@echo "Size of models in $$HOME/.cache/huggingface/hub"
	@du -sh $$HOME/.cache/huggingface/hub ||:
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:
	@echo "Container images"
	@${RUNSUDO} docker image ls

# Container targets ------------------------------------------

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

# Vulnerability scan
container-vulnerability-scan:
	trivy image ${CONTAINER_IMAGE} --scanners vuln
# This is super-slow, it never ends

container-validate-base:
	@${RUNSUDO} docker pull gcr.io/distroless/python3-debian12  && \
	${RUNSUDO} /home/vicente/.go/bin/cosign verify gcr.io/distroless/python3-debian12 -\
		--certificate-oidc-issuer https://accounts.google.com \
		--certificate-identity keyless@distroless.iam.gserviceaccount.com

# TODO: Validate each base container image

# Not puting the model in the container ---------------------

# TODO: Add nvidia capabilities https://stackoverflow.com/questions/59691207/docker-build-with-nvidia-runtime

# Build container without model
container-build-no-model:
	@echo "Building container image without model ${CONTAINER_IMAGE}:no-model"
	${RUNSUDO} docker build . -f build/containerfile_no_model \
		-t ${CONTAINER_IMAGE}:no-model \
		--build-arg USER_ID="$$(id -u)" \
		--build-arg YOUR_ENV="production"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:no-model

container-push-no-model:
	@echo "Pushing ${CONTAINER_IMAGE}:no-model"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:no-model

container-build-no-model-bin:
	@echo "Building container image without model compiling binary ${CONTAINER_IMAGE}:no-model-bin"
	${RUNSUDO} docker build . -f build/containerfile_no_model_bin \
		-t ${CONTAINER_IMAGE}:no-model-bin \
		--build-arg USER_ID="$$(id -u)" \
		--build-arg YOUR_ENV="production"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:no-model-bin

container-push-no-model-bin:
	@echo "Pushing ${CONTAINER_IMAGE}:no-model-bin"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:no-model-bin

container-run-no-model:
	@PROJ_HOME=$$PWD  && \
	${RUNSUDO} docker run -it \
		-v "$$PROJ_HOME/.cache":/app/.cache:ro \
		-e MODEL_DIR="${MODEL_DIR}" \
		-u $$(id -u):$$(id -g) \
		${CONTAINER_IMAGE}:no-model

container-run-no-model-bin:
	@PROJ_HOME=$$PWD  && \
	${RUNSUDO} docker run -it \
		-v "$$PROJ_HOME/.cache":/app/.cache:ro \
		-e MODEL_DIR="${MODEL_DIR}" \
		-u $$(id -u):$$(id -g) \
		${CONTAINER_IMAGE}:no-model-bin

# We need to change the container user to have access to the mounted files
# If using an independent volume, this shouldn't be a problem	
# https://forums.docker.com/t/we-cant-push-a-docker-volume-so-now-what/56160/2

# Copy or download the model inside the container ------------------------------------

# Build container by copying model from local folder
container-build-copy: download
	@echo "Building container image copying model ${CONTAINER_IMAGE}:model-copy"
	${RUNSUDO} docker build . -f build/containerfile_copy -t ${CONTAINER_IMAGE}:model-copy \
		--build-arg HF_HOME_LOCAL="$$HF_HOME" \
		--build-arg YOUR_ENV="production" \
		--build-arg MODEL_DIR="${MODEL_DIR}"

# Build container by downloading model inside it
container-build-download:
	@echo "Building container image that downloads model inside ${CONTAINER_IMAGE}:model-copy"
	@source ./env.txt && \
	${RUNSUDO} docker build . -f build/containerfile_download -t ${CONTAINER_IMAGE}:model-copy \
		--secret id=hf_token,env=HUGGINGFACE_TOKEN \
		--build-arg YOUR_HOME="$$HOME" \
		--build-arg MODEL_DIR="${MODEL_DIR}:model-copy"

# Run container with model
container-run-copy-download:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE}:model-download

# Run container with model
container-run-copy:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE}:model-copy

container-push-copy:
	@echo "Pushing ${CONTAINER_IMAGE}:model-copy"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:model-copy

container-push-download:
	@echo "Pushing ${CONTAINER_IMAGE}:model-download"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:model-download

# Test container builds -------------------------------------------------

# Test container build
test-container: test-dummy-sudo test-container-build-no-model test-container-build-copy-home test-container-build-copy-local test-container-build-download test-container-build-download-py
test-dummy-sudo:
	@${RUNSUDO} ls
test-container-build-copy: download container-build-copy container-run-copy
test-container-build-download: container-build-download container-run-download
test-container-build-no-model: download container-build-no-model container-run-no-model
test-container-build-no-model-bin: download container-build-no-model-bin container-run-no-model-bin
