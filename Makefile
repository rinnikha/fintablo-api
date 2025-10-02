.PHONY: help install install-dev test lint format clean build upload docs

help:		## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:	## Install package in development mode
	pip install -e .

install-dev:	## Install package with development dependencies
	pip install -e .
	pip install -r requirements-dev.txt

test:		## Run tests with coverage
	pytest

lint:		## Run linting tools
	flake8 fintablo_api tests examples
	mypy fintablo_api

format:		## Format code
	black fintablo_api tests examples
	isort fintablo_api tests examples

clean:		## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:		## Build package
	python -m build

upload:		## Upload to PyPI
	python -m twine upload dist/*

docs:		## Generate documentation
	cd docs && make html