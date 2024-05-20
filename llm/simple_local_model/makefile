
all: requirements install_python install download run size

run:
	poetry run python ./src/app.py

download:
	poetry run python ./src/model-download.py

install_python:
	pyenv install $$(cat .python-version) -s

code:
	poetry run code .

requirements:
	which pyenv
	which poetry

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete:
	poetry env remove python
	rm -r $$HOME/.cache/huggingface/

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/

# Container targets ------------------------------------------

CONTAINER_IMAGE=quay.io/vicenteherrera/llama2

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker ' 1>/dev/null || echo "sudo")

# https://docs.docker.com/engine/install/debian/#install-using-the-repository

.PHONY: container-build
# build the container image

vulnerability-scan:
	trivy filesystem poetry.lock --scanners vuln

container-build-copy:
	@echo "Building container image"
	@${RUNSUDO} docker buildx build . -f containerfile_copy -t ${CONTAINER_IMAGE} --build-arg YOUR_HOME="$$HOME" --build-context huggingface="$$HOME/.cache/huggingface"

container-build-download:
	@echo "Building container image"
	@${RUNSUDO} docker buildx build . -f containerfile_download -t ${CONTAINER_IMAGE} --build-arg YOUR_HOME="$$HOME" --build-context huggingface="$$HOME/.cache/huggingface"

container-run:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE} poetry run python ./src/app.py

container-vulnerability-scan:
	trivy image ${CONTAINER_IMAGE} --scanners vuln