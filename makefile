all: help

help:
	@echo "'cd' into each directory and run 'make help'"

size:
	@echo "Poetry virtualenvs"
	@du -sh /home/mord/.cache/pypoetry/virtualenvs/ ||:
	@echo "Poetry cache"
	@du -sh /home/mord/.cache/pypoetry/cache/ ||:
	@echo "Poetry artifacts"
	@du -sh /home/mord/.cache/pypoetry/artifacts/ ||:
	@echo "Global Huggingface cache models"
	@du -sh $$HOME/.cache/huggingface/hub ||:
	@echo "Local Huggingface cache models"
	@find . -name .cache -type d -exec du -sh {} +
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:

delete:
	@echo "Delete caches:"
	@echo "Poetry virtualenvs"
	@du -sh /home/mord/.cache/pypoetry/virtualenvs/ ||:
	@echo "Local Huggingface cache models"
	@find . -name .cache -type d -exec du -sh {} +
	@echo "Press enter to continue, control+c to abort"
	@read dummy_var
	@echo "Removing cache directories"
	@rm -r /home/mord/.cache/pypoetry/virtualenvs/ ||:
	@find . -name '.cache' -type d -exec rm -r {} +
