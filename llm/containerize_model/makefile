SHELL := /bin/bash

# Torch based models (.bin) require online connection so transformers library
# convert them, you never can just download files for offline use
# MODEL=lysandre/arxiv-nlp
# MODEL_EXT=*.bin
# REVISION=refs/pr/1

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL_EXT=*.safetensors
REVISION=main

CONTAINER_IMAGE=quay.io/vicenteherrera/llm-test

all: requirements install_python install required_python download run-offline-local size

code:
	poetry run code .

# run ----------------------------------------------------------------

run: run-offline

run-online-local:
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

run-offline-home:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME="$$HOME/.cache/huggingface/" \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

run-offline-local:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	poetry run python ./src/app.py

run-offline-local-bin:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	MODEL="${MODEL}" REVISION="${REVISION}" \
	./bin/dist/app

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

download-home:
	source "$$(for p in "env.txt" "../env.txt" "../../env.txt"; do [[ -f "$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	HF_HOME="$$HOME/.cache/huggingface/" && \
	poetry run huggingface-cli download --token=$$HUGGINGFACE_TOKEN \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"

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
	@echo "Building container image without model"
	@source ./env.txt && \
	${RUNSUDO} docker build . -f build/containerfile_no_model \
		-t ${CONTAINER_IMAGE}:no-model \
		--build-arg USER_ID="$$(id -u)" \
		--build-arg YOUR_ENV="production" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}

container-build-no-model-bin:
	@echo "Building container image without model with compilation"
	@source ./env.txt && \
	${RUNSUDO} docker build . -f build/containerfile_no_model_bin \
		-t ${CONTAINER_IMAGE}:no-model \
		--build-arg USER_ID="$$(id -u)" \
		--build-arg YOUR_ENV="production" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}"
	@${RUNSUDO} docker image ls ${CONTAINER_IMAGE}

container-run-no-model:
	${RUNSUDO} docker run -it ${CONTAINER_IMAGE}:no-model

container-run-no-model-volume:
	@PROJ_HOME=$$PWD  && \
	${RUNSUDO} docker run -it \
		-v "$$PROJ_HOME/.cache":/app/.cache:ro \
		-u $$(id -u):$$(id -g) \
		${CONTAINER_IMAGE}:no-model
# We need to change the container user to have access to the mounted files
# If using an independent volume, this shouldn't be a problem	
# https://forums.docker.com/t/we-cant-push-a-docker-volume-so-now-what/56160/2



# Copy or download the model inside the container ------------------------------------

# Build container by copying model from home cache folder
container-build-copy-home: download-home
	@echo "Building container image"
	@${RUNSUDO} docker buildx build . -f build/containerfile_copy -t ${CONTAINER_IMAGE} \
		--build-context huggingface="$$HOME/.cache/huggingface" \
		--build-arg HF_HOME_LOCAL="$$HOME/.cache/huggingface" \
		--build-arg YOUR_ENV="production" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}"
# If you do this, you may end up copying extra models unless you first delete HG cache.
# You need buildx to be able to copy files outside current directory.
# https://docs.docker.com/engine/install/debian/#install-using-the-repository

# Build container by copying model from local folder
container-build-copy-local: download-local
	@echo "Building container image"
	@source ./env.txt && \
	${RUNSUDO} docker build . -f build/containerfile_copy -t ${CONTAINER_IMAGE} \
		--build-arg HF_HOME_LOCAL="$$HF_HOME" \
		--build-arg YOUR_ENV="production" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}"

# Build container by downloading model inside it with huggingface-cli
container-build-download:
	@echo "Building container image"
	@source ./env.txt && \
	${RUNSUDO} docker build . -f build/containerfile_download -t ${CONTAINER_IMAGE} \
		--secret id=hf_token,env=HUGGINGFACE_TOKEN \
		--build-arg YOUR_HOME="$$HOME" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}" \
		--build-arg MODEL_EXT="${MODEL_EXT}"

# Build container by downloading model inside it with python code
container-build-download-py:
	@echo "Building container image"
	@source ./env.txt && \
	${RUNSUDO} docker build . -f build/containerfile_download_py -t ${CONTAINER_IMAGE} \
		--secret id=hf_token,env=HUGGINGFACE_TOKEN \
		--build-arg YOUR_HOME="$$HOME" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}" \
		--build-arg MODEL_EXT="${MODEL_EXT}"

# Run container with model
container-run:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE}


# Test container builds -------------------------------------------------

# Test container build
test-container: test-dummy-sudo test-container-build-no-model test-container-build-copy-home test-container-build-copy-local test-container-build-download test-container-build-download-py
test-dummy-sudo:
	@${RUNSUDO} ls
test-container-build-copy-home: delete_huggingface download-home container-build-copy-home container-run
test-container-build-copy-local: delete_local_huggingface download-local container-build-copy-local container-run
test-container-build-download: container-build-download container-run
test-container-build-download-py: container-build-download-py container-run
test-container-build-no-model: delete_local_huggingface download-local container-build-no-model container-run-no-model-volume
