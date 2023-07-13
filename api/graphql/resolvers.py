import sys
from pathlib import Path
from os.path import dirname, abspath

sys.path.append(Path(__file__).parent.parent.parent)

from .schema import Book
from database.connection import get_db
from schemas import LookUpFilters, InsertParameters
import utils


def get_books(filters: LookUpFilters, get_from: str):
    iterator = get_db() 
    session = next(iterator)
    source,  books = utils.get_books(session, filters, get_from)
    return [
        Book(
            title=book.title,
            authors=book.authors,
            description=book.description,
            subtitle=book.subtitle,
            publisher=book.publisher,
            categories=book.categories
        )
    for book in books], source


def add_book(insert_parameters: InsertParameters):
    iterator = get_db()
    session = next(iterator)
    success, return_value = utils.store_book(insert_parameters, session)
    return utils.serialize_from_db([return_value])[0]
