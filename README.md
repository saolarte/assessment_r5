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

### Make REST requests to the app
To perform requests to the api, Swagger UI can be used, which is available in the following URL
```
http://localhost:8000/docs
```

### Make GraphQL requests to the app
Go to 
```
http://localhost:8000/graphql
```

The following is a sample query to retrieve books that match title and publisher
```
{
  books(title: "sample title", publisher: "sample publisher") {
    items {
      title
      publisher
      
    }
    source
  }
}
```

The following is a sample mutation that stores a new book to database, returning title and authors
```
mutation { book(bookId: "bookid", source: "openlibrary"){
  title
  authors
  }
}
```


