# VHub

VHub is an API that permits uploading of vulnerability datasets based on the following pattern of columns:

|ASSET - HOSTNAME|ASSET - IP_ADDRESS|VULNERABILITY - TITLE|VULNERABILITY - SEVERITY|VULNERABILITY - CVSS|VULNERABILITY - PUBLICATION_DATE
-----------------|------------------|---------------------|------------------------|--------------------|--------------------------------

The data are provided by endpoints to handle it and possibly to generate tables and chats to get insights about the vulnerability data.

----
## Pre-requisites

* [Python 3.8+](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation)

---
## Installation

To install the package, clone the repository on github and run the following command:

```
poetry install
```

Next, enter the virtualenv to be able getting access to django, with:

```
poetry shell
```

### Setting up environment variables

Before continue, you need to generate the SECRET_KEY. To do this, rename the file `.env.example` to `.env`, generate the token and put it as value to `SECRET_KEY`.

### Setting up the database

To setup the databse run:

```
python manage.py migrate
```

### Running the API

Finally, run the **Vhub API** with:

```
python manage.py runserver
```

Now, access http://127.0.0.1:8000/api/swagger/ to see the Swagger documentation.

------------------------------------------------

## Running the unit tests
If you want to run the unit tests, run the following command:

```
python manage.py test
```