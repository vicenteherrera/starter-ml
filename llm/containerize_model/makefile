
# MODEL=lysandre/arxiv-nlp
# MODEL_EXT=*.bin
# REVISION=refs/pr/1

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
MODEL_EXT=*.safetensors
REVISION=main

CONTAINER_IMAGE=quay.io/vicenteherrera/arxiv

all: requirements install_python install download run-offline size

run: run-offline

run-online:
	HF_HOME='./.cache/huggingface/' \
	poetry run python ./src/app.py

run-offline:
	HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
	HF_HOME='./.cache/huggingface/' \
	poetry run python ./src/app.py

download:
	source env.txt && \
	huggingface-cli download --token=$$HUGGINGFACE_TOKEN \
		"${MODEL}" \
		--revision "${REVISION}" \
		--include "${MODEL_EXT}" "*.json" "tokenizer.model" "*.txt"

# -------------------------------------

install_python:
	pyenv install $$(cat .python-version) -s

code:
	poetry run code .

requirements:
	which pyenv
	which poetry
	which huggingface-cli

vulnerability-scan:
	trivy filesystem poetry.lock --scanners vuln

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete: delete_venv delete_local_huggingface

delete_venv:
	poetry env remove python ||:

delete_local_huggingface:
	rm -r ./.cache/huggingface/hub

delete_huggingface:
	rm -r $$HOME/.cache/huggingface/hub

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models in ./.cache/huggingface/"
	@du -sh ./.cache/huggingface/
	@echo "Size of models in $$HOME/.cache/huggingface/hub"
	@du -sh $$HOME/.cache/huggingface/hub

# Container targets ------------------------------------------

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

# https://docs.docker.com/engine/install/debian/#install-using-the-repository

# build the container image

container-build-copy: download
	@echo "Building container image"
	@${RUNSUDO} docker buildx build . -f build/containerfile_copy -t ${CONTAINER_IMAGE} \
	   --build-context huggingface="./.cache/huggingface"

container-build-download:
	@echo "Building container image"
	@${RUNSUDO} source env.txt  && \
	docker buildx build . -f build/containerfile_download -t ${CONTAINER_IMAGE} \
		--secret id=hf_token,env=HUGGINGFACE_TOKEN \
		--build-arg YOUR_HOME="$$HOME" \
		--build-arg MODEL="${MODEL}" \
		--build-arg REVISION="${REVISION}" \
		--build-arg MODEL_EXT="${MODEL_EXT}" \

container-run:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE}

container-vulnerability-scan:
	trivy image ${CONTAINER_IMAGE} --scanners vuln
