# terrapin

Create and verify attestations using [Terrapin](https://github.com/fkautz/terrapin-go) Go command-line tool.

## Prerequisites

You can run a container with all requirements ready using:

```bash
make container-run
```

Alternative, start checking the general prerequisites explained in [the main README.md](../../../README.md). Additionally you have installed a modern [Go](https://go.dev/doc/install) version to compile terrapin-go from sources.

```bash
# Clone and compile terrapin from source
make clone-compile-terrapin
```

## Create and validate attestations with Terrapin

To create and validate a sha256 attestations of a single model file

```bash
# Initialize tooling, download model. Skip this on container-run.
make

# Create attestation digest file
make run-create-terrapin-attest

# Validate attestation digest file
make run-validate-terrapin-attest
```

## More information

Check [Terrapin](https://github.com/fkautz/terrapin-go) repository for more information.
