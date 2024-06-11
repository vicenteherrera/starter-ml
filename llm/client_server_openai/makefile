
all: requirements install_python install required_python run size

run:
	@echo "To run the server, use: make run_server"
	@echo "To run the client, use: make run_client"

run_server:
	@echo "Execute also client on another terminal with: make run_client"
	@poetry run python ./src/openai_llm_server.py

run_client:
	@echo "Execute also server on another terminal with: make run_server"
	@poetry run streamlit run ./src/openai_llm_client.py

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

delete: delete_venv

delete_venv:
	poetry env remove --all ||:

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:
