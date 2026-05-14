.PHONY: test lint type cov complexity all clean install

install:
	pip install -e ".[dev]"

test:
	pytest -v

cov:
	pytest --cov=src --cov-report=term-missing --cov-report=html

lint:
	ruff check src/ tests/

type:
	mypy --strict src/ || true

complexity:
	radon cc src/ -s -a

all: lint type test cov complexity

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -name .coverage -delete
	find . -name "*.db" -delete
	find . -name "rel_*.txt" -delete
