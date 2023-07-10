from typing import Union, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db_connection import get_db
from db_operations import create_book, retrieve_books_from_db
from google_api_utilities import retrieve_books, build_query
from schemas import Book, InputBook, BookList, LookUpFilters
from utils import serialize_books_output, serialize_from_db


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/", response_model=BookList)
async def list_books_handler(keyword:str=None, author: str=None, title: str=None, publisher: str=None, category: str=None, session: Session = Depends(get_db)):
    output_books = None
    source = ""

    filters = LookUpFilters(keyword=keyword, author=author, title=title, publisher=publisher, category=category)
    books = retrieve_books_from_db(session=session, filters=filters)
    if len(books) > 0:
        output_books = books
        source = "internal_db"
    else:
        query_parameters = build_query(filters)
        try:
            output_books = retrieve_books(query_parameters)
            source = "google"
        except Exception as e:
            print(e)
        
    serialized_books = serialize_books_output(source, output_books)
    return {"items": serialized_books, "source": source }


@app.post("/book/", status_code=201, response_model=Book)
def create_book_handler(input_book: InputBook, session: Session = Depends(get_db)):
    success, return_value = create_book(session=session, input_book=input_book)
    if success:
        return serialize_from_db([return_value])[0]
    else:
        raise HTTPException(status_code=409, detail=return_value)
