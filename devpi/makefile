

install:
	poetry install --no-root

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

delete:
	poetry env remove --all

size:
	@echo "Size of libraries"
	@du -sh $$(poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server