from typing import Union, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.operations import create_book, retrieve_books_from_db, delete_book_from_database
from google_api import utilities as googleapi_utilities
from openlibrary_api import utilities as openlibrary_utils
from schemas import Book, InputBook, BookList, LookUpFilters, InsertParameters
from utils import serialize_books_output, serialize_from_db, serialize_from_openlibrary_api


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/", response_model=BookList)
async def list_books_handler(get_from: str="google", 
                            keyword:str=None, 
                            author: str=None, 
                            title: str=None, 
                            publisher: str=None, 
                            category: str=None, session: Session = Depends(get_db)):
    output_books = None
    source = ""

    filters = LookUpFilters(keyword=keyword, author=author, title=title, publisher=publisher, category=category)
    books = retrieve_books_from_db(session=session, filters=filters)
    if len(books) > 0:
        output_books = books
        source = "internal_db"
    elif get_from == "google": 
        try:
            output_books = googleapi_utilities.retrieve_books(filters)
            source = "google"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    elif get_from == "openlibrary":
        try:            
            output_books = openlibrary_utils.retrieve_books(filters=filters)
            source = "openlibrary"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    else:
            raise HTTPException(status_code=501, detail=f"source: {get_from} not supported")

    
    serialized_books = serialize_books_output(source, output_books)
    return {"items": serialized_books, "source": source }


@app.post("/book/", status_code=201, response_model=Book)
def create_book_handler(insert_parameters: InsertParameters, session: Session = Depends(get_db)):
    if insert_parameters.source == "openlibrary":
        try:
            filters = LookUpFilters(keyword=insert_parameters.book_id)
            book = openlibrary_utils.get_book(filters)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    elif insert_parameters.source == "google":
        try:
            book = googleapi_utilities.get_book(insert_parameters.book_id)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=501, detail=f"source: {insert_parameters.source} not supported")
    
    serialized_book = serialize_books_output(insert_parameters.source, [book])[0]
    success, return_value = create_book(session=session, input_book=serialized_book)
    if success:
        return serialize_from_db([return_value])[0]
    else:
        raise HTTPException(status_code=409, detail=return_value)


@app.delete("/book/{book_id}")
def delete_book(book_id: str, session: Session = Depends(get_db)):
    result, value = delete_book_from_database(session=session, id=book_id)
    if result:
        return {"book_id": book_id}
    elif result is None:
        raise HTTPException(status_code=404, detail=value)
    else:
        raise HTTPException(status_code=409, detail=value)



