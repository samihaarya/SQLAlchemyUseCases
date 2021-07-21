from book_store.dao.book_dao import BookDao
from book_store.db import db_engine


class BookService:
    def __init__(self):
        self.book_dao = BookDao()
        self.engine = db_engine.get_engine()
        self.session = db_engine.get_session()

    def add_book(self, book):
        with self.engine.connect() as connection:
            # user_found = self.user_dao.get_user(user.name, user.phone, connection)
            # if user_found:
            #     raise Exception('user already exists')
            # else:
            with connection.begin():
                response = self.book_dao.add_book(book, connection)
                return response

