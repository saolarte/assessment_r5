from schemas import Book

def serialize_books_output(source, books):
    if source=="google":
        return [
            Book(
                id=book["id"],
                title=book["volumeInfo"]["title"],
                subtitle=book["volumeInfo"].get("subtitle", ""),
                authors=book["volumeInfo"].get("authors", []),
                categories=book["volumeInfo"].get("categories", []),
                publishedDate=book["volumeInfo"].get("publishedDate", ""),
                publisher=book["volumeInfo"].get("publisher", ""),
                description=book["volumeInfo"].get("description", "")
            )
            for book in books]
    elif source=="internal_db":
        return [
            Book(
                id=book.id,
                title=book.title,
                subtitle=book.subtitle,
                authors=[author.name for author in book.authors],
                categories=[category.name for category in book.categories],
                publishedDate=book.published_date,
                publisher=book.publisher,
                description=book.description
            )
            for book in books]
        