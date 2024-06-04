# terrapin

Create and verify attestations using [Terrapin](https://github.com/fkautz/terrapin-go) Go command-line tool.

# Prerequisites

Check the general prerequisites explained in [the main README.md](../../../README.md)

This instructions assumes you have installed a modern [Go](https://go.dev/doc/install) version.

```console
# Clone source repository and build Terrapin binary from sources
git clone https://github.com/fkautz/terrapin-go.git
cd terrapin-go
go build -o terrapin ./cmd/terrapin
cd ..
```

# Attestations

```console
# Initialize tooling, download model, and test run it
make

# Set model main file as an example, you should loop through all files
MODEL_FILE="/home/mord/code/_vh/starter-ml/llm/_security/terrapin/.cache/huggingface/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/fe8a4ea1ffedaf415f4da2f062534de366a451e6/model.safetensors"

# Create attestation
./terrapin-go/terrapin attest \
    -input "$MODEL_FILE" \
    -output attestations/model.safetensors.attestation

# Validate attestation
./terrapin-go/terrapin validate \
    -input "$MODEL_FILE" -attestations \
    attestations/model.safetensors.attestation

# Repeat with other files like:

MODEL_FILE="/home/mord/code/_vh/starter-ml/llm/_security/terrapin/.cache/huggingface/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/fe8a4ea1ffedaf415f4da2f062534de366a451e6/config.json"

# Create attestation
./terrapin-go/terrapin attest \
    -input "$MODEL_FILE" \
    -output attestations/config.json.attestation

# Validate attestation
./terrapin-go/terrapin validate \
    -input "$MODEL_FILE" -attestations \
    attestations/config.json.attestation

# Verify and echo content
./terrapin-go/terrapin cat \
    -input "$MODEL_FILE" -attestations \
    attestations/config.json.attestation

```





