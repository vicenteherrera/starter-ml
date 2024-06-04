
all: requirements upgrade_pyenv install_python install required_python jupyter

jupyter:
	poetry run jupyter-lab

run:
	poetry run python ./starter_ml/hugging-face.py

init:
	poetry run devpi-init

config:
	poetry run devpi-gen-config

gen-secret:
	mkdir -p secret/
	chmod og-w secret/
	poetry run devpi-gen-secret --secretfile ./secret/secretfile

run:
	poetry run devpi-server

run-secret-file:
	poetry run devpi-server --secretfile ./secret/secretfile

run-background:
	supervisord -c gen-config/supervisord.conf

# requirements ----------------------------------------------------------------

install_python:
	pyenv install $$(cat .python-version) -s

requirements:
	which pyenv
	which poetry

upgrade_pyenv:
	cd $$HOME/.pyenv && git pull

required_python:
	@PVPOETRY="$$(poetry run python --version)" && \
	PVPOETRY=$${PVPOETRY#"Python "} && \
	PV="$$(cat .python-version)" && \
	if [ "$$PVPOETRY" != "$$PV" ]; then \
		echo "**Error, Python version mismatch" && \
		echo ".python-version file: $$PV" && \
		echo "poetry run python --version: $$PVPOETRY" && \
		echo "Run make refresh and check your pyenv path configuration" && \
		exit 1; \
	fi

refresh: delete_venv
	pyenv uninstall -f $$(cat .python-version)
	pyenv install $$(cat .python-version)
	rm poetry.lock
	poetry install --no-root

# Libraries utilities ----------------------------------------

install:
	poetry install --no-root

update:
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

delete: delete-venv

delete-venv:
	poetry env remove --all ||:/

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/ ||:
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:
