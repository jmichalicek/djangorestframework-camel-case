.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "sdist - package"

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
	flake8 src/djangorestframework_camel_case tests

test:
	uv run pytest

test-all:
	tox

coverage:
	coverage run --source djangorestframework_camel_case setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

django-upgrade:
	 uv run django-upgrade src/*/*.py tests/*.py --target-version 5.2

pyupgrade:
	uv run pyupgrade src/djangorestframework_camel_case/*.py tests/*.py --py311-plus
	
# release: clean
# 	python setup.py sdist upload

# sdist: clean
# 	python setup.py sdist
# 	ls -l dist