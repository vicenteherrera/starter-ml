SHELL := /bin/bash

all: requirements
	make -s install_python install -C ./backend -f ../makefile
	make -s install_python install -C ./frontend -f ../makefile
	@make -s help

run: help

help:
	@echo "To run the backend, use: make run_backend"
	@echo "To run the frontend, use: make run_frontend"

run_backend:
	@echo "Execute also client on another terminal with: make run_frontend"
	@source "$$(for p in "env.txt" "../env.txt" "../../env.txt" "../../../env.txt"; do [[ -f "$$p" ]] && echo "$$p" && break; done || echo "/dev/null")" && \
	cd backend && poetry run python ./src/backend.py

run_frontend:
	@echo "Execute also server on another terminal with: make run_backend"
	cd frontend && poetry run streamlit run ./src/frontend.py

code:
	poetry run code .

container-build:
	cd backend && make -s container-build
	cd frontend && make -s container-build

container-push:
	cd backend && make -s container-push
	cd frontend && make -s container-push


config_exists:
	@[ -f "../../env.txt" ] || ( echo "Error: Config file ../../env.txt not found" && exit 1 )

RUNSUDO := $(shell groups | grep ' docker \|com\.apple' 1>/dev/null || echo "sudo")

compose-up: config_exists
	${RUNSUDO} docker compose up
