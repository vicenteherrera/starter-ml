
all: jupyter

jupyter:
	poetry run jupyter-lab

update:
	@echo "It's ok to receive 'Authorization error accessing https://download.pytorch.org/whl/cu118/tokenizers'"
	poetry update

run_hugging_face:
	poetry run python ./starter_ml/hugging-face.py

show:
	poetry show

info:
	poetry run poetry env info -p

cleanup:
	poetry env remove python
	rm -r $$HOME/.cache/huggingface/

size:
	@echo "Size of libraries"
	@du -sh $$(poetry run poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/

# Container targets ------------------------------------------

CONTAINER_IMAGE=quay.io/vicenteherrera/starter-ml

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker ' 1>/dev/null || echo "sudo")

# https://docs.docker.com/engine/install/debian/#install-using-the-repository

.PHONY: container-build
# build the container image
container-build:
	@echo "Building container image"
	@${RUNSUDO} docker buildx build . -f containerfile -t ${CONTAINER_IMAGE} --build-arg YOUR_HOME="$$HOME" --build-context huggingface="$$HOME/.cache/huggingface"

container-run:
	@${RUNSUDO} docker run -i -t ${CONTAINER_IMAGE} poetry run python ./starter_ml/hugging-face.py