install:
	@echo "Installing dependencies"
	python -m pip install --upgrade pip
	python -m pip install .
	@echo "Configuring environment variables"
	python -c \
		'from django.core.management.utils import get_random_secret_key; \
	       	print(f"SECRET_KEY={get_random_secret_key()}")' > .env

vhub/database/db.sqlite3:
	python manage.py migrate

run: vhub/database/db.sqlite3
	python manage.py runserver

develop:
	python -m pip install poetry
	poetry install


test: vhub/database/db.sqlite3
	@echo "Running the tests"
	poetry run python manage.py test
