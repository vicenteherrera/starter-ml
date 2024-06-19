

build:
	python3 -m build

push:
	python3 -m twine upload --skip-existing dist/*

delete:
	rm -r dist/*

publish: build push