
IMAGE_NAME=quay.io/vicenteherrera/python-dev-shell
TAG=3.11.7

all: container-build container-run

build: container-build

generate-base-req:
	@poetry run pip-compile --generate-hashes build/base_requirements/poetry.in -o build/base_requirements/poetry.out
	@poetry run pip-compile --generate-hashes build/base_requirements/pyinstaller.in -o build/base_requirements/pyinstaller.out
	@poetry run pip-compile --generate-hashes build/base_requirements/nuitka.in -o build/base_requirements/nuitka.out

container-build:
	docker build . -f build/containerfile_dev -t ${IMAGE_NAME}:${TAG}

container-run:
	docker run -it \
		-v "$$(pwd)/../":/home/user/starter-ml \
		-u $$(id -u):$$(id -g) \
		${IMAGE_NAME}:${TAG}

container-push:
	docker push ${IMAGE_NAME}:${TAG}

container-pull:
	docker pull ${IMAGE_NAME}:${TAG}

