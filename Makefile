.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with ruff"
	@echo "lint-fix - fix any safe fixable style issues with ruff"
	@echo "format - format files with ruff"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python and report in the console"
	@echo "coverage - check code coverage quickly with the default Python and generate an html report"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "django-upgrade - run django-upgrade targetting the minimum supported version of Django"
	@echo "pyupgrade - run pyupgrade targetting the minimum supported version of Python"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

format:
	uv run ruff format

test:
	uv run pytest

test-all:
	tox

coverage:
	uv run pytest --cov --cov-report=term-missing

coverage-html:
	uv run pytest --cov --cov-report=html

django-upgrade:
	 uv run django-upgrade src/*/*.py tests/*.py --target-version 5.2

pyupgrade:
	uv run pyupgrade src/drf_dromedary/*.py tests/*.py --py311-plus
	
# release: clean
# 	python setup.py sdist upload

# sdist: clean
# 	python setup.py sdist
# 	ls -l dist