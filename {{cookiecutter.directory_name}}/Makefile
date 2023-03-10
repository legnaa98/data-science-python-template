# Styling
.PHONY: style
style:
	black .
	python3 -m isort .
	interrogate .

# Cleaning
.PHONY: clean
clean: style
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage

# Setup environment
.PHONY: env
env:
	git init
	pip install --upgrade pip
	python3 -m pip install setuptools wheel
	python3 -m pip install -e .

# Setup dev environment
.PHONY: devenv
devenv:
	git init
	pip install --upgrade pip
	python3 -m pip install setuptools wheel
	python3 -m pip install -e ".[dev]"
	pre-commit autoupdate
	pre-commit install