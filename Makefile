install:
	@poetry install

lint:
	@poetry run flake8 amorty

test:
	@poetry run pytest

coverage:
	poetry run coverage run --source=amorty -m pytest tests
	poetry run coverage report -m

build: lint test
	@poetry build

publish:
	@poetry publish -r testpypi

.PHONY: install lint test coverage build publish
