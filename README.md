# VHub

VHub is an API that permits uploading of vulnerability datasets based on the following pattern of columns:

|ASSET - HOSTNAME|ASSET - IP_ADDRESS|VULNERABILITY - TITLE|VULNERABILITY - SEVERITY|VULNERABILITY - CVSS|VULNERABILITY - PUBLICATION_DATE
-----------------|------------------|---------------------|------------------------|--------------------|--------------------------------

The data are provided by endpoints to handle it and possibly to generate tables and chats to get insights about the vulnerability data.

----
## Pre-requisites

* [Python 3.8+](https://www.python.org/downloads/)

---
## Installation

To install the package, run the following command:

```
make install
```

### Running the API

Finally, run the **Vhub API** with:

```
make run
```

Now, access http://127.0.0.1:8000/api/swagger/ to see the Swagger documentation.

------------------------------------------------

## Running the unit tests
If you want to run the unit tests, run the following command:

```
make test
```
