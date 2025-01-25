.PHONY: help clean test lint format check docs build env all
.DEFAULT_GOAL := help

help:  ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} \
	/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

##@ Primary Commands
all: clean check test docs build  ## Run all checks and tests

##@ Development
env:  ## Create the development environment (with all extras)
	pip install -e '.[dev,test,docs]'
	pip install nox

clean: ## Clean up build artifacts and caches
	nox -s clean

##@ Testing
test: ## Run tests
	nox -s tests

test-coverage: ## Run tests with coverage report
	nox -s tests report

##@ Code Quality
lint: ## Run linting
	nox -s lint

type: ## Run type checking
	nox -s type

check: lint type ## Run all code quality checks

##@ Documentation
docs: ## Build documentation
	nox -s docs

docs-serve: ## Serve documentation locally
	cd docs && python -m http.server --directory _build/html

docs-clean: ## Clean documentation build
	nox -s clean

##@ Building
build: clean ## Build the package
	pip install build
	python -m build
