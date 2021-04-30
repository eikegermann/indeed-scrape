#!/usr/bin/env bash

# Setup
pipenv install --dev

# Linting
pipenv run autoflake -r src --recursive --in-place --remove-all-unused-imports --exclude=__init__.py
pipenv run flake8 src
pipenv run isort -rc src
pipenv run black src --line-length=120

# Test coverage
pipenv run pytest --cov=src/todo --cov-report html ${@}

# Type anno coverage
pipenv run mypy .

# Docstring coverage
pipenv run interrogate -c pyproject.toml src