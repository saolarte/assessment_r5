from typing import List
import strawberry

from .resolvers import get_books
from .schema import Book, BookList
from schemas import LookUpFilters




@strawberry.type
class Query:
    @strawberry.field
    def books(get_from: str = "google",
             keyword: str = None, 
              title: str = None, 
              author: str = None, 
              category: str = None,  
              publisher: str= None) -> BookList:
        filters = LookUpFilters(keyword=keyword,
                                title=title, 
                                author=author,
                                pusblisher=publisher,
                                category=category
                                )
        books, source = get_books(filters=filters, get_from=get_from)
        return BookList(items=books, source=source)
        