all: help

help:
	@echo "'cd' into each directory and run 'make help'"

size:
	@echo "Size of libraries"
	@du -sh /home/mord/.cache/pypoetry/virtualenvs/
	@echo "Size of devpi cache"
	@du -sh $$HOME/.devpi/server ||:
	@echo "Local cache models"
	@find . -name .cache -type d -exec du -sh {} \;

delete:
	@echo "Delete all virtual environment, devpi cache, and global and all local .cache folders"
	@echo "Press enter to continue, control+c to abort"
	@read dummy_var
	@echo "Removing cache folders"
	@rm -r /home/mord/.cache/pypoetry/virtualenvs/ ||:
	@rm -r $$HOME/.devpi/server ||:
	@find . -name .cache -type d -exec rm -r {} \;