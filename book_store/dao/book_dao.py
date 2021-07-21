from sqlalchemy import select, insert

from book_store.dto.book import Book


class BookDao:
    def add_book(self, book: Book, connection):
        stmt = insert(Book).values(book)
        response = connection.execute(stmt)
        val = response.inserted_primary_key[0]
        return val

    def add_book_with_transaction(self, book: Book, transaction):
        transaction.add(book)

    def get_book_by_id(self, book_id, connection):
        stmt = select(Book).where(Book.book_id == book_id)
        result = connection.execute(stmt)
        response = None
        for row in result:
            response = dict(row)
        return response

