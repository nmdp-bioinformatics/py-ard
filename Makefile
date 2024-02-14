PROJECT_NAME := $(shell basename `pwd`)
PACKAGE_NAME := pyard

.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr allure_report

lint: ## check style with flake8
    # stop the build if there are Python syntax errors or undefined names \
	  exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 $(PACKAGE_NAME) tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 $(PACKAGE_NAME) --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	pre-commit

behave: clean-test ## run the behave tests, generate and serve report
	- behave -f allure_behave.formatter:AllureFormatter -o allure_report
	allure serve allure_report

pytest: clean-test ## run tests quickly with the default Python
	PYTHONPATH=. pytest

test: clean-test ## run all(BDD and unit) tests
	PYTHONPATH=. pytest
	behave

coverage: ## check code coverage quickly with the default Python
	coverage run --source pyard -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/pyars.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pyars
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

docker-build: ## build a docker image for the service
	docker build --platform=linux/amd64 -t nmdpbioinformatics/pyard-service:latest .

docker: docker-build ## build a docker image and run the service
	docker run --platform=linux/amd64 --rm --name pyard-service -p 8080:8080 nmdpbioinformatics/pyard-service:latest

install: clean ## install the package to the active Python's site-packages
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-tests.txt
	pip install -r requirements-dev.txt
	pip install -r requirements-deploy.txt
	python setup.py install
	pre-commit install

venv: ## creates a Python3 virtualenv environment in venv
	python3 -m venv venv --prompt $(PROJECT_NAME)-venv
	@echo "====================================================================="
	@echo "To activate the new virtual environment, execute the following from your shell"
	@echo "source venv/bin/activate"

activate: ## activate a virtual environment. Run `make venv` before activating.
	@echo "====================================================================="
	@echo "To activate the new virtual environment, execute the following from your shell"
	@echo "source venv/bin/activate"
