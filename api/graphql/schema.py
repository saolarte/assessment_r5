from typing import List, Union
from datetime import date
import strawberry

@strawberry.type
class Book:
    title: str
    subtitle: str
    authors: Union[None, List[str]] = None
    categories: Union[None, List[str]] = None
    publishedDate: Union[None, date] = None
    description: str
    publisher: str


@strawberry.type
class BookList:
    items: List[Book]
    source: str


@strawberry.type
class LookUpFilters:
    keyword: Union[str, None] = None
    author: Union[str, None] = None
    title: Union[str, None] = None
    publisher: Union[str, None] = None
    category: Union[str, None] = None


@strawberry.type
class InsertParameters:
    book_id: str
    source: str