from schemas import Book

def serialize_books_output(source, books):
    if source=="google":
        return serialize_from_google_api(books)
    elif source=="internal_db":
        return serialize_from_db(books)
    elif source=="openlibrary":
        return serialize_from_openlibrary_api(books)


def serialize_from_google_api(books):
    return [
            Book(
                bookId=book["id"],
                title=book["volumeInfo"]["title"],
                subtitle=book["volumeInfo"].get("subtitle", ""),
                authors=book["volumeInfo"].get("authors", []),
                categories=book["volumeInfo"].get("categories", []),
                publishedDate=book["volumeInfo"].get("publishedDate", ""),
                publisher=book["volumeInfo"].get("publisher", ""),
                description=book["volumeInfo"].get("description", "")
            )
            for book in books]


def serialize_from_db(books):
    return [
            Book(
                bookId=book.book_id,
                title=book.title,
                subtitle=book.subtitle,
                authors=[author.name for author in book.authors],
                categories=[category.name for category in book.categories],
                publishedDate=book.published_date,
                publisher=book.publisher,
                description=book.description
            )
            for book in books]


def serialize_from_openlibrary_api(books):
    serialized_books = []
    for book in books:
        book_object = Book(
            bookId=book["key"],
            title=book["title"],
            subtitle=book.get("subtitle", ""),
            authors=book.get("author_name", []),
            categories=book.get("subject", []),
            publishedDate=book.get("first_publish_year", ""),
            publisher=get_book_publisher(book),
            description= get_book_description(book)
        )
        serialized_books.append(book_object)
    return serialized_books


def get_book_description(book):
    description = ""
    if "first_sentence" in book.keys():
            description = " ".join(book["first_sentence"])
    return description

def get_book_publisher(book):
    publisher = ""
    if "publisher" in book.keys():
        publisher = book["publisher"][0]
    return publisher

