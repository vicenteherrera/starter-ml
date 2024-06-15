
IMAGE_NAME=quay.io/vicenteherrera/python-dev-shell
TAG=3.11.7

all: container-build container-run

build: container-build

generate-base-req:
	@poetry run pip-compile --generate-hashes build/base_requirements/poetry.in -o build/base_requirements/poetry.out
	@poetry run pip-compile --generate-hashes build/base_requirements/pyinstaller.in -o build/base_requirements/pyinstaller.out
	@poetry run pip-compile --generate-hashes build/base_requirements/nuitka.in -o build/base_requirements/nuitka.out

# Check if sudo is required to run Docker
RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

container-build:
	${RUNSUDO} docker build . -f build/containerfile_dev \
	--build-arg USER_ID="$$(id -u)" \
	-t ${IMAGE_NAME}:${TAG}

container-run:
	${RUNSUDO} docker run -it \
		-v "$$(pwd)/../":/home/user/starter-ml \
		-u $$(id -u):$$(id -g) \
		${IMAGE_NAME}:${TAG}

container-push:
	${RUNSUDO} docker push ${IMAGE_NAME}:${TAG}

container-pull:
	${RUNSUDO} docker pull ${IMAGE_NAME}:${TAG}

