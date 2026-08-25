.PHONY: install test lint validate demo

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

validate:
	uaf validate-sources

demo:
	python tools/run_synthetic_demo.py

