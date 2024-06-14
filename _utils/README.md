# _utils

This directory provides a container image to run all the examples.

Be careful that running the examples will get models inside the running container, which will get huge.

Also examples that already run docker may not work at all.

## Usage

```bash
# Pull and run the pre-made container image
make container-pull container-run

# Build and run your own version of the image locally
make
```