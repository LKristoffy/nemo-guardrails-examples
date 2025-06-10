.PHONY: all test install dev clean
.EXPORT_ALL_VARIABLES:

PYTHON = python3

-include .env

OPENAI_API_KEY ?=

custom-ml: install
	$(PYTHON) src/examples/custom-ml/demo.py

input-checking:
	cd src/examples/input-checking && $(PYTHON) demo.py

install:
	@echo "Installing/updating production dependencies..."
	@uv sync

test: dev
	pytest

dev: install
	@echo "Installing development dependencies..."
	@uv pip install -e .
	@pre-commit install
	@echo "Package installed. Run 'make test' to run tests."

clean:
	rm -rf .venv __pycache__ .pytest_cache *.egg-info

setup:
	@echo "Setting up environment..."
	@chmod +x setup.sh
	@./setup.sh
	@echo "Environment setup complete."