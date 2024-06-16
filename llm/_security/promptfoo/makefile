SHELL := /bin/bash

DIR=$(shell basename $$(pwd))
CONTAINER_IMAGE=quay.io/vicenteherrera/promptfoo
CONTAINER_TAG=latest

CONFIG_FILE=$(shell for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "")

all: requirements install_promptfoo

run: run-offline

run-online: config_exists
	source ${CONFIG_FILE} && \
	cd data && \
	promptfoo eval

run-offline: config_exists
	source ${CONFIG_FILE} && \
	cd data && \
	PROMPTFOO_DISABLE_TELEMETRY=1 \
	PROMPTFOO_DISABLE_UPDATE=1 \
	promptfoo eval

run-view:
	promptfoo view -y -p 15500

install_promptfoo:
	npm install -g promptfoo

requirements:
	npm --version

config_exists:
	@[ ! -z "${CONFIG_FILE}" ] || ( echo "Error: Config file env.txt not found" && exit 1 )
	@echo "Config file found at ${CONFIG_FILE}"

# Container targets ------------------------------------------

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

container-build: config_exists
	@echo "Building container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	@source ${CONFIG_FILE} && \
	${RUNSUDO} docker build . -f build/containerfile_dev \
		--secret id=OPENAI_API_KEY,env=OPENAI_API_KEY \
		-t ${CONTAINER_IMAGE}:${CONTAINER_TAG}
	${RUNSUDO} docker image ls ${CONTAINER_IMAGE}:${CONTAINER_TAG}

container-run:
	@echo "Running container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	@${RUNSUDO} docker run -it \
	  -p 15500:15500 \
		${CONTAINER_IMAGE}:${CONTAINER_TAG} sh -c "make run-view"

container-run-dev: config_exists
	@echo "Running container image with local dir mounted ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	@${RUNSUDO} docker run \
		-v "$$(pwd)"/${CONFIG_FILE}:/home/env.txt" \
		-u $$(id -u):$$(id -g) \
		-p 15500:15500 \
		-it \
		${CONTAINER_IMAGE}:${CONTAINER_TAG} /bin/bash

container-push:
	@echo "Pushing container image ${CONTAINER_IMAGE}:${CONTAINER_TAG}"
	${RUNSUDO} docker push ${CONTAINER_IMAGE}:${CONTAINER_TAG}
