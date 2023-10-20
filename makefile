
all: jupyter

jupyter:
	poetry run jupyter-lab

update:
	poetry update