
IMAGE_NAME=quay.io/vicenteherrera/python-dev-shell
TAG=3.11.7

all: container-build container-run

build: container-build

container-build:
	docker build . -f containerfile_dev -t ${IMAGE_NAME}:${TAG}

container-run:
	docker run -it \
		-v "$$(pwd)/../":/home/user/starter-ml \
		-u $$(id -u):$$(id -g) \
		${IMAGE_NAME}:${TAG}

