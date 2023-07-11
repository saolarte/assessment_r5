# R5 assessment

## To run locally follow these steps

### Update .env file with provided data
Locate .env in the root of the project and replace values with the ones provided.

### Install dependencies and start virtual environment
```
pipenv install
pipenv shell
```

### Run tests
```
python -m pytest
```

### Run app
```
python run.py
```

### Make requests to the app
Open API UI can be used to perform requests to the api. This is available at the following URL
```
http://localhost:8000/docs
```

