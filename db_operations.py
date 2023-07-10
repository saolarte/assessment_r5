from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from models import Book, Author, Category
from schemas import Book as BookSchema
from schemas import InputBook, LookUpFilters


def create_book(session: Session, input_book):
    serialized_input_book = input_book.model_dump(by_alias=True)

    authors = create_entities(Author, session, serialized_input_book["authors"])
    categories = create_entities(Category, session, serialized_input_book["categories"])
    del(serialized_input_book["authors"])
    del(serialized_input_book["categories"])

    book = Book(**serialized_input_book, authors=authors, categories=categories)

    session.add(book)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        return False, f"Error in INSERT operation: {e.orig}" 
    session.refresh(book)
    return True, book


def create_entities(model, session: Session, names: str):
    entities = []
    for name in names:
        try:
            existing_entity = session.query(model).filter(model.name.ilike(name)).one()
            entities.append(existing_entity)
        except NoResultFound as e:
            new_entity = model(name=name)
            session.add(new_entity) 
            session.commit()
            entities.append(new_entity)
    return entities
            

def retrieve_books_from_db(session: Session, filters: LookUpFilters):
    filters = build_filters(filters)
    books = session.query(Book).filter(*filters).all()
    return books


def build_filters(filters):
    serialized_filters = filters.model_dump(exclude_none=True)
    query_filters = []
    for key, value in serialized_filters.items():
        if key=='author':
            query_filters.append(Book.authors.any(Author.name.ilike(f"%{value}%")))
        if key=='category':
            query_filters.append(Book.categories.any(Category.name.ilike(f"%{value}%")))
        if key=="title":
            query_filters.append(Book.title.ilike(f"%{value}%"))
        if key=='publisher':
            query_filters.append(Book.publisher.ilike(f"%{value}%"))
    return query_filters






