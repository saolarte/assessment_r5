from datetime import datetime, date
from typing import List, Union
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator



class BaseBook(BaseModel):
    model_config = ConfigDict(from_attributes = True, populate_by_name = True)
    
    title: str
    subtitle: str
    authors: Union[None, List[str]] = None
    categories: Union[None, List[str]] = None
    publishedDate: Union[None, date] = Field(serialization_alias="published_date")
    description: str
    publisher: str

    @field_validator("publishedDate", mode="before")
    def parse_published_date(cls, value):
        formats = ["%Y", "%Y-%m","%Y-%m-%d"]
        for format in formats:
            try:
                date = datetime.strptime(str(value), format).date()
                return date
            except ValueError:
                pass


class InputBook(BaseBook):
    bookId: Union[None, str] = Field(serialization_alias="book_id")

class Book(BaseBook):
    bookId: Union[None, str] = Field(validation_alias="book_id", serialization_alias="id")



class BookList(BaseModel):
    items: List[Book]
    source: str


class LookUpFilters(BaseModel):
    keyword: Union[str, None] = None
    author: Union[str, None] = None
    title: Union[str, None] = None
    publisher: Union[str, None] = None
    category: Union[str, None] = None


class InsertParameters(BaseModel):
    book_id: str
    source: str