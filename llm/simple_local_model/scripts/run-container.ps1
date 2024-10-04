
$MODEL="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
$MODEL_DIR="./.cache/huggingface/hub/${MODEL}"
$CONTAINER_IMAGE="quay.io/vicenteherrera/test-llm"

docker run -it `
		-e MODEL_DIR="${MODEL_DIR}" `
    -v "$env:USERPROFILE/.cache":/app/.cache:ro `
		${CONTAINER_IMAGE}:no-model