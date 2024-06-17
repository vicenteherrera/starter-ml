SHELL := /bin/bash

# Torch based models (.bin) require online connection so transformers library
# convert them, you never can just download files for offline use
# MODEL=lysandre/arxiv-nlp
# MODEL_EXT=*.bin
# REVISION=refs/pr/1

#  "stabilityai/stable-diffusion-2-1", revision="refs/pr/22", use_safetensors=True

MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
COMMIT=ce0c99637bf2aba3265ec4675b50eadb26ac5a21
MODEL_DIR=./.cache/huggingface/hub/${MODEL}

DIGEST_DIR=$(shell pwd)/digest

CONTAINER_IMAGE=quay.io/vicenteherrera/test-llm
CONTAINER_TAG=no-model
CONTAINER_SHA=sha256:c0528e2f4bc9cd1381cdc4ad8d6cd35e4d1d2defe70572d85eb94f13a55fef22

SIGNER_ID=vicenteherrera@vicenteherrera.com
SIGNER_OIDC=https://accounts.google.com

CONFIG_FILE=$(shell for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "")

all: help

help:
	@echo ""
	@echo "HELP"
	@echo ""
	@echo "# Download model"
	@echo "make download"
	@echo ""
	@echo "# Generate model digest SHA256"
	@echo "make run-generate-digest"
	@echo ""
	@echo "# Tamper with the model"
	@echo "make run-tamper-model"
	@echo ""
	@echo "# Validate model files with stored digest"
	@echo "make run-validate-digest"
	@echo ""
	@echo "# Verify signed container with public key using cosign against online rekor"
	@echo "make container-pull run-container-verify-key"
# run ----------------------------------------------------------------

run-container-sign-keyless: container-pull
	@echo "Siging keyless container image ${CONTAINER_IMAGE}@${CONTAINER_SHA}"
	cosign sign ${CONTAINER_IMAGE}@${CONTAINER_SHA}

run-container-verify-keyless: container-pull
	@echo "Verifying keyless signature for container image ${CONTAINER_IMAGE}@${CONTAINER_SHA}"
	cosign verify \
		--certificate-identity ${SIGNER_ID} \
		--certificate-oidc-issuer ${SIGNER_OIDC} \
		${CONTAINER_IMAGE}@${CONTAINER_SHA}

run-container-sign-key: container-pull
	@echo "Siging container image ${CONTAINER_IMAGE}@${CONTAINER_SHA}"
	cosign sign --key $$HOME/.ssh/cosign.key \
		${CONTAINER_IMAGE}@${CONTAINER_SHA}

run-container-verify-key: container-pull
	@echo "Verifying keyless signature for container image ${CONTAINER_IMAGE}@${CONTAINER_SHA}"
	cosign verify \
		--key cosign.pub \
		${CONTAINER_IMAGE}@${CONTAINER_SHA}

run-tamper-model:
	echo -n '   ' >> ${MODEL_DIR}/config.json

run-generate-digest:
	@echo "Calculating hash of individual files for ${MODEL} into ${DIGEST_DIR}" && \
	mkdir -p ${DIGEST_DIR}/${MODEL} && \
	cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f | xargs -I {} sh -c 'sha1sum {} | tee ${DIGEST_DIR}/{}.digest'

	@echo ""
	@echo "Calculating hash of global directory for ${MODEL}"
	@cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f \( -exec sha1sum {} \; \) | awk '{print $1}' | sort | sha1sum | tee ${DIGEST_DIR}.digest

run-validate-digest:
	@echo "Validating hash of individual files for ${MODEL} into ${DIGEST_DIR}" && \
	mkdir -p ${DIGEST_DIR}/${MODEL} && \
	cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f | xargs -I {} sh -c '[ "$$(sha1sum {})" = "$$(cat ${DIGEST_DIR}/{}.digest)" ] && echo "[ Valid ] {}" || echo "[*ERROR*] {}"'
	@echo ""
	@echo "Calculating hash of global directory for ${MODEL}"
	@cd "./.cache/huggingface/hub/" && \
	[ "$$(find ${MODEL} -type f \( -exec sha1sum {} \; \) | awk '{print $1}' | sort | sha1sum)" = "$$(cat ${DIGEST_DIR}.digest)" ] && echo "[ Valid ] ${DIGEST_DIR}.digest" || echo "[*ERROR*] ${DIGEST_DIR}.digest"
	

run-model-sign:
	for FILE in ".cache/huggingface/hub/${MODEL}"/*; do \
  	cosign sign-blob --key $$HOME/.ssh/cosign.key "$$FILE" \
			--output-signature "signatures/$$FILENAME.sig" \
		; \
	done

run-model-verify:
	for FILE in ".cache/huggingface/hub/${MODEL}"/*; do \
  	cosign verify-blob --key cosign.pub --signature "signatures/$$FILE.sig" "$$FILE" ; \
	done




cosign-generate-key-pair:
	cosign generate-key-pair
	cp cosign.* $$HOME/.ssh
	rm cosign.key

container-pull:
	docker pull ${CONTAINER_IMAGE}:${CONTAINER_TAG}

container-sha:
	docker images --no-trunc --quiet ${CONTAINER_IMAGE}:${CONTAINER_TAG}

# download ----------------------------------------------------------------

download: download-local-git-https

download-local-git-ssh:
	@make -s git-prepare
	git clone --depth 1 git@hf.co:${MODEL} "${MODEL_DIR}"
	@make -s git-finish

download-local-git-https:
	@make -s git-prepare
	git clone --depth 1 https://huggingface.co/${MODEL} "${MODEL_DIR}"
	@make -s git-finish

git-prepare:
	@echo "Cloning ${MODEL} commit ${COMMIT}"
	git lfs install
	rm -rf "${MODEL_DIR}"

git-finish:
	cd "${MODEL_DIR}" && \
	git fetch --depth 1 origin "${COMMIT}" && \
	git -c advice.detachedHead=false checkout "${COMMIT}"
	rm -rf "${MODEL_DIR}"/.git

# Requirements ----------------------------------------------------------------

config_exists:
	@[ ! -z "${CONFIG_FILE}" ] || ( echo "Error: Config file env.txt not found" && exit 1 )
	@echo "Config file found at ${CONFIG_FILE}"

# Libraries utilities ----------------------------------------

delete: delete_local_huggingface

delete_venv:
	poetry env remove --all ||:

delete_local_huggingface:
	rm -r ./.cache/huggingface/hub ||:

size:
	@echo "Size of models in ./.cache/huggingface/"
	@du -sh ./.cache/huggingface/ ||:


