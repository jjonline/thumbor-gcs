PYTHON ?= python

# This script is only used for debugging by the developers of this project during the development process
# For git tag publish, github Action CI will auto publish to pypi.org

.PHONY: build
build:
	 make clean && $(PYTHON) setup.py sdist bdist_wheel

.PHONY: clean
clean:
	 rm -rf ./build ./dist ./*.egg-info

.PHONY: publish
publish:
	 twine upload --repository-url https://upload.pypi.org/legacy/ --username __token__ --password ${PYPI_TOKEN} dist/*
