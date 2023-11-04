
all: jupyter

jupyter:
	poetry run jupyter-lab

update:
	@echo "It's ok to receive 'Authorization error accessing https://download.pytorch.org/whl/cu118/tokenizers'"
	poetry update

show:
	poetry show

info:
	poetry run poetry env info -p

cleanup:
	poetry env remove python
	rm -r $$HOME/.cache/huggingface/

size:
	@echo "Size of libraries"
	@du -sh $$(poetry run poetry env info --path 2>/dev/null)
	@echo "Size of models"
	@du -sh $$HOME/.cache/huggingface/