from book_store.common.filter import Filter, FilterOperation
from book_store.dao.book_dao import BookDao
from book_store.dao.books_loan_dao import BooksLoanDao
from book_store.dao.user_dao import UserDao
from book_store.db import db_engine
from book_store.db.page import Page
from book_store.dto.book_loan import BookOnLoan


class BooksLoanService:
    def __init__(self):
        self.book_on_loan_dao = BooksLoanDao()
        self.book_dao = BookDao()
        self.user_dao = UserDao()
        self.engine = db_engine.get_engine()
        self.session = db_engine.get_session()

    def add_loan(self, book_on_loan: BookOnLoan):
        with self.session() as session:
            with session.begin():
                response = self.book_on_loan_dao.add_book_on_loan_with_transaction(book_on_loan, session)
                return response

    def add_book_loan_without_transaction(self, loan: dict):
        conn = self.engine.connect()
        self.user_dao.add_user(user=loan['user'], connection=conn)
        conn.commit()
        self.book_dao.add_book(book=loan['book'], connection=conn)
        conn.commit()
        self.book_on_loan_dao.add_book_on_loan(book_loan=loan['book_on_loan'], connection=conn)
        conn.commit()

    def add_book_loan_with_transaction(self, loan: dict):
        with self.session() as session:
            with session.begin():
                self.user_dao.add_user_with_transaction(user=loan['user'], transaction=session)
                self.book_dao.add_book_with_transaction(book=loan['book'], transaction=session)
            with session.begin():
                self.book_on_loan_dao.add_book_on_loan_with_transaction(book_loan=loan['book_on_loan'], session=session)

    def get_loan(self):
        conn = self.engine.connect()
        loan_books = self.book_on_loan_dao.get_loan_books(conn)
        print('loan book- '.format(loan_books))
        for loan_book in loan_books:
            book_id = loan_book.pop('book_id')
            loan_book['book'] = self.book_dao.get_book_by_id(book_id=book_id, connection=conn)
            print('book- '.format(loan_book['book']))
            # user_id = loan_book.get('book_id')
            user_id = loan_book.pop('user_id')
            loan_book['user'] = self.user_dao.get_user_by_id(user_id=user_id, connection=conn)
            print('user- '.format(loan_book['user']))
        return loan_books

    def get_loan_with_transaction(self):
        with self.engine.connect() as conn:
            loan_books = self.book_on_loan_dao.get_loan_books(conn)
            print('loan book-'.format(loan_books))
            for loan_book in loan_books:
                book_id = loan_book.get('book_id')
                loan_book['book'] = self.book_dao.get_book_by_id(book_id=book_id, connection=conn)
                print('book-'.format(loan_book['book']))
                loan_book.pop('book_id')

                user_id = loan_book.get('book_id')
                # user_id = loan_book.pop('user_id')
                loan_book['user'] = self.user_dao.get_user_by_id(user_id=user_id, connection=conn)
                print('user-'.format(loan_book['user']))
                # loan_book.pop('user_id')
            return loan_books

    def get_loan_with_filter_and_pagination(self, params):
        with self.engine.connect() as conn:
            page: Page = self.init_request_page(params=params)
            filters: Filter = self.build_filters(params=params)
            loan_books_page = self.book_on_loan_dao.get_paginated_loan_books(page=page, filters=filters, session=conn)

            loan_books = loan_books_page.elements
            print(f'loan book-'+ str(loan_books_page))

            for loan_book in loan_books:
                print(f'loan book-' + str(type(loan_book)))
                book_id = loan_book.pop('book_id')
                loan_book['book'] = self.book_dao.get_book_by_id(book_id=book_id, connection=conn)
                print('book-'.format(loan_book['book']))

                user_id = loan_book.pop('user_id')
                loan_book['user'] = self.user_dao.get_user_by_id(user_id=user_id, connection=conn)
                print('user-'.format(loan_book['user']))

            return loan_books

    def init_request_page(self, params):
        request_page = Page()
        page_number: int = params['page']
        page_size: int = params['size']
        if page_number:
            request_page.page = page_number
        if page_size:
            request_page.size = page_size
        return request_page

    def build_filters(self, params):
        filter_map = {
            'loanDate': 'loan_date',
            'loanDays': 'loan_days'
        }

        filters = Filter(filter_map)

        filters.add_filter('loanDays', params['loan_days'], FilterOperation.EQUALS)
        filters.add_sort_filters(['loanDate,asc'])
        return filters
