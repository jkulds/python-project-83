dev:
	poetry run flask --app page_analyzer:app run --debug

install:
	poetry install

build:
	./build.sh

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

PORT ?= 8000
start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app