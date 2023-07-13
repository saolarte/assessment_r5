from typing import Union
import strawberry

from fastapi import HTTPException
from .resolvers import add_book
from .schema import Book, InsertParameters


@strawberry.type
class Mutation:
    @strawberry.mutation
    def book(self,  book_id: str, source: str) -> Union[Book, None]:
        parameters = InsertParameters(book_id=book_id, source=source)
        try:
            book = add_book(parameters)
            return book
        except HTTPException:
            return None