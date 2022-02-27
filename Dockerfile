FROM python:3.8
COPY . /app
WORKDIR /app
RUN echo "Installing dependencies"
RUN python -m pip install --upgrade pip
RUN python -m pip install .
RUN echo "Configuring environment variables"
RUN python -c \
		'from django.core.management.utils import get_random_secret_key; \
	       	print(f"SECRET_KEY={get_random_secret_key()}")' > .env

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
