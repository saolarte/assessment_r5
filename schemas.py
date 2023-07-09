from datetime import datetime, date
from typing import List, Union
from datetime import date
from pydantic import BaseModel, Field, validator



class Book(BaseModel):
    title: str
    subtitle: str
    authors: Union[None, List[str]] = None
    categories: Union[None, List[str]] = None
    publishedDate: Union[None, date] = Field(serialization_alias="published_date")
    description: str
    publisher: str

    @validator("publishedDate", pre=True)
    def parse_published_date(cls, value):
        formats = ["%Y", "%Y-%m","%Y-%m-%d"]
        for format in formats:
            try:
                date = datetime.strptime(value, format).date()
                return date
            except ValueError:
                pass


    class Config:
        from_attributes = True
        populate_by_name = True


class BookList(BaseModel):
    items: List[Book]
    source: str


class LookUpFilters(BaseModel):
    keyword: Union[str, None]
    author: Union[str, None]
    title: Union[str, None]
    publisher: Union[str, None]
    category: Union[str, None]
