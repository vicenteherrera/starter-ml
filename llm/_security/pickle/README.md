# pickle

This example shows how the Pickle data format is insecure

## Requirements

PyEnv and Poetry as described on the main README.md, or just execute a development container shell with:

```bash
make container-run
```

## Usage

```bash
# Create compromised pickle file
make run-save-compromise

# Load compromised pickle file that reveals secret
make run-load-compromise

# Examine compromised pickle file without loading or running
make run-pickletools"
```

## More information

* https://docs.python.org/3/library/pickle.html
* https://docs.python.org/3/library/pickletools.html#module-pickletools
* https://www.datacamp.com/tutorial/pickle-python-tutorial
* https://snyk.io/blog/guide-to-python-pickle/
