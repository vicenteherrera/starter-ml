SHELL := /bin/bash

CONTAINER_IMAGE=quay.io/vicenteherrera/test-llm-frontend
CONTAINER_TAG=streamlit-0.0.1

all: requirements install_python install required_python run size

run: run_frontend

run_frontend:
	@echo "Execute also server on another terminal with: cd ../backend && make run"
	poetry run streamlit run ./src/frontend.py

code:
	poetry run code .

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

delete: delete_venv

delete_venv:
	poetry env remove --all ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:

# Container targets ------------------------------------------

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

container-build:
	@echo "Building container image without model"
	${RUNSUDO} docker build . -f build/containerfile \
		-t ${CONTAINER_IMAGE}:${CONTAINER_TAG} \
		--build-arg USER_ID="$$(id -u)" \
		--build-arg YOUR_ENV="production"

container-run:
	${RUNSUDO} docker run \
		-e SERVER_URL=http://localhost:3000/ask \
		-it \
		${CONTAINER_IMAGE}:${CONTAINER_TAG}

container-push:
	${RUNSUDO} docker push ${CONTAINER_IMAGE}:${CONTAINER_TAG}
