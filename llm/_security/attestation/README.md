# attestation

This directory includes several examples related to attestation for machine learning.

## Requirements

You can run a container for a shell with all requirements installed with:
```bash
make run-container
```

It won't work to check signatures of a container unless you setup a docker-in-docker environment in the host.

To run directly, for `cosign` examples, you need the [cosign binary installed](https://github.com/sigstore/cosign?tab=readme-ov-file#installation). For `CycloneDX` examples you need [it's cli installed](https://github.com/CycloneDX/cyclonedx-cli).

## Usage

```bash
# Download model with GIT using HTTPS and sparse checkout a specific commit
make download
# You can switch it to SSH if you set up your public key in Huggingface

HELP

# Download model
make download

# DIGEST SHA1SUM

# Generate model digest SHA256
make run-generate-digest

# Tamper with the model, so you see an error on validation
make run-tamper-model

# Validate model files with stored digest
make run-validate-digest

# GPG

# Validate model files with gpg detached signatures
make run-validate-gpg

# CYCLONEDX

# Generate an CycloneDX BOM file from model
make run-mlbom-generate

# Verify the signature of the reference CycloneDX BOM file provided
make run-mlbom-verify-sign

# Conventional diff the generated and reference CycloneDX BOM files
make run-mlbom-diff-with-reference

# COSIGN

# Validate model files with cosign detached signatures
make run-cosign-verify

# Verify signed container with inference code using public key and cosign against online rekor
make container-pull run-container-verify-key

```

There are also additional targets used to generate the digests and sign the model files, the  and container.

## Limitations of the current tooling

* `sha1sum` doesn't have a standard way to store generated digest, so a script is implemented here where the output is captured in a text file for later verification.
* `sha1sum`, `gpg` and `cosign` don't process a full directory, so a script is implemented here to itereate on each file to generate an individual detached hash/signature file. This won't detect missing files from the downloaded model. In the case of sha1sum, an additional script takes all digest for the files of the directory, and generates a hash of that, so in that case it's having the full content of the directory is tracked.
* `gpg` and `cosign` can sign inline the model files, adding a modification to each one, so they are stored that way and when they get retrieved, the signature is checked and that part of the file removed when loaded in memory. As current ML libraries can't do that, we have to store the signatures in a separate directory which is not as secure.
* `cosign` should add the signature to the container image so it's pushed to the registry alognside it, but that fails at least on quay.io registry.
* `CycloneDX cli` can generate digest of all the files in a directory as a BOM XML document, and sign the document. But its "diff" function only considers known versions of software packages, so it doesn't consider the digest of the files to report if they have been modified, so regular bash `diff` has been used.

## Check also

Check [terrapin](../terrapin/README.md) example to learn about using that tool for attestation.

## More information

* Bill of Materials (AI/ML BOM)
  * [MLBOM 101 (video)](https://drive.google.com/file/d/1mEWlTLq2tzsvNXlMe8xOub2CguqBsxXf/view)
  * [SPDX AI](https://spdx.dev/learn/areas-of-interest/ai/)
  * [CycloneDX cli](https://github.com/CycloneDX/cyclonedx-cli)
  * [Artificial Intelligence Bill-of-Materials (AI BOMs): Ensuring AI Transparency and Traceability](https://becomingahacker.org/artificial-intelligence-bill-of-materials-ai-boms-ensuring-ai-transparency-and-traceability-82322643bd2a)
  * [Manifest AIBOM (MLBOM) Wiki](https://github.com/manifest-cyber/aibom)
  * [Securing the LLM stack](https://blogs.cisco.com/learning/securing-the-llm-stack)

* Model cards
  * [Huggingface model cards](https://huggingface.co/blog/model-cards)
  * [Huggingface model card template](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/modelcard_template.md)
  * [Huggingface model card writting tool](https://huggingface.co/spaces/huggingface/Model_Cards_Writing_Tool)
  * [IBM AI Factsheets](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/factsheets-model-inventory.html?context=cpdaas)
