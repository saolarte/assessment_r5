from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from  database.connection import Base, engine


book_authors = Table('book_authors', Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True)
)

book_categories = Table('book_categories', Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(String, unique=True, index=True)
    title = Column(String, unique=True, index=True)
    subtitle = Column(String)
    authors = relationship("Author", secondary="book_authors", back_populates='books')
    categories = relationship("Category", secondary="book_categories", back_populates="books")
    published_date = Column(Date)
    description = Column(String)
    publisher = Column(String)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    books = relationship("Book", secondary="book_authors", back_populates='authors')


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    books = relationship("Book", secondary="book_categories", back_populates="categories")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    active = Column(Boolean)

# Create the tables in the database
Base.metadata.create_all(engine)