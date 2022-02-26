install:
	@echo "Installing dependencies"
	python -m pip install --upgrade pip
	python -m pip install poetry
	poetry config virtualenvs.in-project true
	poetry install

vhub/database/db.sqlite3:
	poetry run python manage.py migrate

test: vhub/database/db.sqlite3
	@echo "Running the tests"
	poetry run python manage.py test
