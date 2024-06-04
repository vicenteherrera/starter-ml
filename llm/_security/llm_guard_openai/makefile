
all: requirements install_python install required_python size help

help:
	@echo ""
	@echo "# User discloses private information to AI endpoint (OpenAI)"
	@echo "make run-unprotected   # Discloses private information"
	@echo "make run-protected     # Private information is filtered"
	@echo "# User queries information out of context"
	@echo "make run-no-injection2 # No injection"
	@echo "make run-unprotected2  # With prompt injection"
	@echo "make run-protected2    # Prompt injection is blocked"

run-unprotected:
	poetry run python ./src/app1-unprotected.py 

run-protected:
	poetry run python ./src/app1-protected.py

run-no-injection2:
	poetry run python ./src/app2-no-injection.py 

run-unprotected2:
	poetry run python ./src/app2-unprotected.py 

run-protected2:
	poetry run python ./src/app2-protected.py 



code:
	poetry run code .

# requirements ----------------------------------------------------------------

requirements:
	which pyenv
	which poetry

install_python: upgrade_pyenv
	pyenv install $$(cat .python-version) -s

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

delete: delete-venv delete-huggingface-home

delete-venv:
	poetry env remove --all ||:

delete-huggingface-home:
	rm -r $$HOME/.cache/huggingface/ ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:

vulnerability-scan:
	trivy filesystem poetry.lock --scanners vuln

