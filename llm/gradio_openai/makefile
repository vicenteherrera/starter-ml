
all: requirements install_python install run size

run:
	poetry run python ./src/app.py

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

size:
	@echo "Size of libraries"
	@du -sh $$(poetry run poetry env info --path 2>/dev/null)

# Container targets ------------------------------------------

CONTAINER_IMAGE=quay.io/vicenteherrera/llama2

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker ' 1>/dev/null || echo "sudo")

# https://docs.docker.com/engine/install/debian/#install-using-the-repository

.PHONY: container-build
# build the container image
container-build:
	@echo "Building container image"
	@${RUNSUDO} docker buildx build . -f containerfile -t ${CONTAINER_IMAGE} --build-arg YOUR_HOME="$$HOME"

container-run:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE} poetry run python ./src/app.py