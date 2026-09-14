PROJECT_NAME := $(shell basename `pwd`)
PACKAGE_NAME := pyard
PYARD_VERSION := 2.4.1

.PHONY: help clean clean-test clean-pyc clean-build docs behave lint pytest test coverage docs servedocs release dist docker-build docker install
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

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

lint: ## check style with flake8 and pre-commit
	uv tool run ruff check
	uv run pre-commit run --all-files
	npx @redocly/cli lint api-spec.yaml

behave: clean-test ## run the behave tests, generate and serve report
	- uv run behave -f allure_behave.formatter:AllureFormatter -o allure_report
	uv run allure serve allure_report

pytest: clean-test ## run tests quickly with the default Python
	uv run pytest

test: clean-test ## run all(BDD and unit) tests
	uv run pytest
	uv run behave

coverage: ## check code coverage quickly with the default Python
	uv run coverage run --source pyard -m pytest
	uv run coverage report -m
	uv run coverage html
	@python -m webbrowser htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/pyard.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pyard
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@python -m webbrowser docs/build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	uv publish

dist: clean ## builds source and wheel package
	uv build
	ls -l dist

docker-build: ## build a docker image for the service
	docker build --platform=linux/amd64 -t nmdpbioinformatics/pyard-service:$(PYARD_VERSION).linux-amd64 .
	docker tag nmdpbioinformatics/pyard-service:$(PYARD_VERSION).linux-amd64 nmdpbioinformatics/pyard-service:latest

docker: docker-build ## build a docker image and run the service
	docker run --platform=linux/amd64 --rm --name pyard-service -p 8080:8080 nmdpbioinformatics/pyard-service:$(PYARD_VERSION).linux-amd64

docker-build-local: ## build a local docker image for the service
	docker build --platform=linux/amd64 -t nmdpbioinformatics/pyard-service:$(PYARD_VERSION).linux-amd64 -f Dockerfile-local .
	docker run --platform=linux/amd64 --rm --name pyard-service -p 8080:8080 nmdpbioinformatics/pyard-service:$(PYARD_VERSION).linux-amd64

install: clean ## create the uv-managed environment with all groups and extras
	uv sync --all-extras --group test --group dev
	uv run pre-commit install
	@echo "====================================================================="
	@echo "Environment ready in .venv"
	@echo "Run commands with 'uv run <command>' (e.g. 'uv run pytest')"
