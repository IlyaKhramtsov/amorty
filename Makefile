install:
	@poetry install

lint:
	@poetry run flake8 amorty

test:
	@poetry run pytest

.PHONY: install lint test
