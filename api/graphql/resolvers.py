import sys
from pathlib import Path
from os.path import dirname, abspath

sys.path.append(Path(__file__).parent.parent.parent)

from .schema import Book
from database.connection import get_db
from database.operations import retrieve_books_from_db
from schemas import LookUpFilters
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