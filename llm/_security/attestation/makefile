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
GPG_DIR=$(shell pwd)/gpg

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
	@echo "# Tamper with the model, so you see an error on validation"
	@echo "make run-tamper-model"
	@echo ""
	@echo "# Validate model files with stored digest"
	@echo "make run-validate-digest"
	@echo ""
	@echo "# Validate model files with gpg detached signatures"
	@echo "make run-validate-gpg"
	@echo ""
	@echo "# Validate model files with cosign detached signatures"
	@echo "make run-cosign-verify"
	@echo ""
	@echo "# Generate an CycloneDX BOM file from model"
	@echo "make run-mlbom-generate"
	@echo ""
	@echo "# Verify the signature of the reference CycloneDX BOM file provided"
	@echo "make run-mlbom-verify-sign"
	@echo ""
	@echo "# Conventional diff the generated and reference CycloneDX BOM files"
	@echo "make run-mlbom-diff-with-reference"
	@echo ""
	@echo "# Verify signed container with inference code using public key and cosign against online rekor"
	@echo "make container-pull run-container-verify-key"

# run ----------------------------------------------------------------

run-tamper-model:
	echo -n '   ' >> ${MODEL_DIR}/config.json

# sha1sum digest

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

# gpg

run-gpg-sign:
	@echo "Gpg sign individual files for ${MODEL} into ${GPG_DIR}" && \
	mkdir -p ${GPG_DIR}/${MODEL} && \
	cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f | xargs -I {} sh -c 'echo "{}" && gpg --output ${GPG_DIR}/{}.sig --yes --detach-sign {}' +

run-gpg-verify:
	@echo "Gpg sign individual files for ${MODEL} into ${GPG_DIR}" && \
	mkdir -p ${GPG_DIR}/${MODEL} && \
	cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f | xargs -I {} sh -c 'echo "{}" && gpg --verify ${GPG_DIR}/{}.sig {}' +

# cyclonedx

run-mlbom-generate:
	mkdir -p mlbom/${MODEL}
	cyclonedx add files --no-input \
		--output-format xml \
		--exclude /.git/** \
		--base-path .cache/huggingface/hub/ \
		--output-file mlbom/${MODEL}/mlbom.xml

run-mlbom-analyze:
	cyclonedx analyze --input-format xml \
		--input-file mlbom/${MODEL}/mlbom.xml \
		--multiple-component-versions

run-mlbom-validate:
	cyclonedx validate --input-format xml \
		--input-file mlbom/${MODEL}/mlbom.xml \
		--fail-on-errors

run-mlbom-reference-sign:
	cp mlbom/${MODEL}/mlbom.xml mlbom/${MODEL}/mlbom-reference.xml
	cyclonedx sign bom mlbom/${MODEL}/mlbom.xml \
		--key-file $$HOME/.ssh/mlbom.key

run-mlbom-reference-verify-sign:
	cyclonedx verify all mlbom/${MODEL}/mlbom-reference.xml \
		--key-file ./pubkeys/mlbom.pub

run-mlbom-diff:
	diff mlbom/${MODEL}/mlbom-reference.xml mlbom/${MODEL}/mlbom.xml

# Cosign model

run-cosign-sign:
	export OUTPUT_DIR="$(shell pwd)/cosign" && \
	mkdir -p $$OUTPUT_DIR/${MODEL} && \
	cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f | xargs -I {} sh -c 'echo "{}" && COSIGN_PASSWORD="changeme" cosign sign-blob --key $$HOME/.ssh/cosign.key --output-signature $$OUTPUT_DIR/{}.sig {} --yes' +

run-cosign-verify:
	export OUTPUT_DIR="$(shell pwd)/cosign" && \
	export PUBKEY="$(shell pwd)/pubkeys/cosign.pub" && \
	cd "./.cache/huggingface/hub/" && \
	find ${MODEL} -type f | xargs -I {} sh -c 'echo "{}" && cosign verify-blob --key $$PUBKEY --signature $$OUTPUT_DIR/{}.sig {}' +

# Cosign container

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

# Utilities

mlbom-keygen:
	cyclonedx keygen \
		--private-key-file $$HOME/.ssh/mlbom.key \
		--public-key-file pubkeys/mlbom.pub

cosign-generate-key-pair:
	cosign generate-key-pair
	mv cosign.key $$HOME/.ssh
	mv cosign.pub ./pubkeys

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

#  ----------------------------------------------------------------

container-run:
	${RUNSUDO} docker run -it \
		-v "$$(pwd)/../attestation":/home/user/attestation \
		-u $$(id -u):$$(id -g) \
		quay.io/vicenteherrera/python-dev-shell:3.11.7 \
		sh -c "cd attestation && make help && /bin/bash"

size:
	@echo "Size of models in ./.cache/huggingface/"
	@du -sh ./.cache/huggingface/ ||:


