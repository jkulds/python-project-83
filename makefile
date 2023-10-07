dev:
	poetry run flask --app page_analyzer:app run --debug

install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest

PORT ?= 8000
start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app