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
make run-pickletools

# Create a pickle file for a ML model
make run-save-model

# Load a picle file for a ML model
make run-load-model

# Modify existing pickle file to add arbitrary code execution
make run-modify-model run-load-model
```

## More information

* [Python docs: pickle](https://docs.python.org/3/library/pickle.html)
* [Python docs: pickletools](https://docs.python.org/3/library/pickletools.html#module-pickletools)
* [Python pickle tutorial](https://www.datacamp.com/tutorial/pickle-python-tutorial)
* [Guide to Python pickle](https://snyk.io/blog/guide-to-python-pickle/)
* [Audit shows that safetensors is safe and ready to become the default](https://huggingface.co/blog/safetensors-security-audit)
* [New Hugging Face Vulnerability Exposes AI Models to Supply Chain Attacks](https://hiddenlayer.com/research/silent-sabotage/)
* [Use safetensors to avoid malicious AI models](https://medium.com/codenlp/use-safetensors-to-avoid-malicious-ai-models-c94f0fce1215)
* [Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
* [ML model formats and code execution](https://hiddenlayer.com/research/weaponizing-machine-learning-models-with-ransomware/#Overview-of-ML-Model-Serialization-Formats)
* [Example Huggingface repo with unsafe model](https://huggingface.co/star23/baller13/tree/main)
* [Example Huggingface repo with EICAR unsafe model](https://huggingface.co/mcpotato/42-eicar-street/tree/main)
* [Huggingface pickle scanning](https://huggingface.co/docs/hub/en/security-pickle#pickle-scanning)
* [Huggingface malware scanning](https://huggingface.co/docs/hub/en/security-malware)
* [Example compromised pickle defing scanning](https://ctftime.org/writeup/16723)