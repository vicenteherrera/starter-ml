

build:
	python3 -m build

push:
	python3 -m twine upload --repository pypi dist/*

delete:
	rm -r dist/*

publish: delete build push