from datetime import datetime, timedelta
from typing import Union, List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from database.connection import get_db
from database.operations import delete_book_from_database
from google_api import utilities as googleapi_utilities
from openlibrary_api import utilities as openlibrary_utils
from schemas import Book, InputBook, BookList, LookUpFilters, InsertParameters, User
from utils import get_books, store_book, serialize_books_output, serialize_from_db
from api.security_utils import validate_token


router = APIRouter()


@router.get("/books/", response_model=BookList)
async def list_books_handler(auth: Annotated[str, Depends(validate_token)], 
                            get_from: str="google", 
                            keyword:str=None, 
                            author: str=None, 
                            title: str=None, 
                            publisher: str=None, 
                            category: str=None, session: Session = Depends(get_db)):
    filters = LookUpFilters(keyword=keyword, 
                            author=author, 
                            title=title, 
                            publisher=publisher, 
                            category=category)
    source, books = get_books(session, filters, get_from)

    
    return {"items": books, "source": source }


@router.post("/book/", status_code=201, response_model=Book)
def create_book_handler(auth: Annotated[str, Depends(validate_token)], 
                        insert_parameters: InsertParameters, 
                        session: Session = Depends(get_db)):
    success, return_value = store_book(insert_parameters, session)
    if success:
        return serialize_from_db([return_value])[0]
    else:
        raise HTTPException(status_code=409, detail=return_value)


@router.delete("/book/{book_id}")
def delete_book(auth: Annotated[str, Depends(validate_token)], book_id: str, session: Session = Depends(get_db)):
    result, value = delete_book_from_database(session=session, id=book_id)
    if result:
        return {"book_id": book_id}
    elif result is None:
        raise HTTPException(status_code=404, detail=value)
    else:
        raise HTTPException(status_code=409, detail=value)
