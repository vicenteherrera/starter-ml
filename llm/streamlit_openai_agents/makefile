
all: requirements install_python install run size

run:
	poetry run streamlit run ./src/app.py

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

delete: delete-venv

delete-venv:
	poetry env remove --all ||:


size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server
