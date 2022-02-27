DB = vhub/database/db.sqlite3


install:
	@echo "Installing dependencies"
	python -m pip install --upgrade pip
	python -m pip install .
	@echo "Configuring environment variables"
	python -c \
		'from django.core.management.utils import get_random_secret_key; \
	       	print(f"SECRET_KEY={get_random_secret_key()}")' > .env

${DB}:
	python manage.py migrate

run: ${DB}
	python manage.py runserver

develop:
	python -m pip install poetry
	poetry install

test: vhub/database/db.sqlite3
	@echo "Running the tests"
	poetry run python manage.py test

build-image:
	@echo "Building the docker image"
	docker build -t vhub/api .

up:
	@echo "Running the built image"
	docker run -d -p 8000:8000 -t vhub/api
