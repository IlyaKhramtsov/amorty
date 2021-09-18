install:
	@poetry install

lint:
	@poetry run flake8 amorty
	@poetry run mypy amorty

test:
	@poetry run pytest

coverage:
	poetry run coverage run --source=amorty -m pytest tests
	poetry run coverage report -m

selfcheck:
	@poetry check

check: selfcheck test lint

build: check
	@poetry build

publish:
	@poetry publish -r testpypi

.PHONY: install lint test coverage selfcheck check build publish
