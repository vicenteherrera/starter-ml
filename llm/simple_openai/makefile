create_venv:
	python3 -m venv .env
	@echo "Activate in Win, with: .env\Scripts\activate"
	@echo "Activate in Bash with: source .env/bin/activate"
	@echo "Activate in Fish with: . .env/bin/activate.fish"

install_req:
	pip install -r requirements.txt

delete:
	rm -rf .env

run:
	python3 ./app.py

size:
	@echo "Size of virtual environment"
	du -sh .env
