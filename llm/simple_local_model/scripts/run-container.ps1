
$MODEL="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
$MODEL_NAME="TinyLlama--TinyLlama-1.1B-Chat-v1.0"
$SNAPSHOT="fe8a4ea1ffedaf415f4da2f062534de366a451e6"
$MODEL_DIR="./.cache/huggingface/hub/models--${MODEL_NAME}/snapshots/$SNAPSHOT"
$CONTAINER_IMAGE="quay.io/vicenteherrera/test-llm"
$CACHE="$env:USERPROFILE\.cache"

docker run -it `
	-e MODEL_DIR="${MODEL_DIR}" `
	-v ${CACHE}:/app/.cache:ro `
	${CONTAINER_IMAGE}:no-model
