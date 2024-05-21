
# Using pipx

install_garak:
	pipx install garak

garak-hg-gpt2:
	. ./env.txt && garak --model_type huggingface --model_name gpt2 --probes dan.AutoDANCached

garak-oa-gpt3.5-turbo:
	. ./env.txt && garak --model_type openai --model_name gpt-3.5-turbo --probes dan.AutoDANCached

# Using poetry

all: requirements install_python install download 

run-hg-gpt2:
	. ./env.txt && poetry run garak --model_type huggingface --model_name gpt2 --probes dan.AutoDANCached

run-oa-gpt3.5-turbo:
	. ./env.txt && poetry run garak --model_type openai --model_name gpt-3.5-turbo --probes dan.AutoDANCached

list-probes:
	poetry run garak --list_probes

# -----------------------------------------------------------------------

install_python:
	pyenv install $$(cat .python-version) -s

code:
	poetry run code .

requirements:
	which pyenv
	which poetry

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete:
	poetry env remove python
	rm -r $$HOME/.cache/huggingface/

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/

