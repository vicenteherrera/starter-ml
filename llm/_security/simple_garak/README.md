# simple_garak

Scan OpenAI and local models with [Garak]() vuln analysis.

## Preparation

Check the main [README.md](../../README.md) for generic prerequisites.

Copy `env-sample.txt` as `env.txt` and put your API keys there.

## Execution

You can use pipx to install Garak globally, or activate the Poetry virtual environment to have it installed there.

```bash
# Using pipx

## Install Garak with pipx
make install_garak

## Run "Do Anything Now" tests on local GPT2 model, it will be downloaded locally
make garak-hg-gpt2

## Run "Do Anything Now" tests on OpenAI gpt model
make garak-oa


# Using poetry

## Prepare requirements
make

## Run "Do Anything Now" tests on local GPT2 model, it will be downloaded locally
make run-hg-gpt2

## Run "Do Anything Now" tests on OpenAI gpt model
make run-oa
```

##