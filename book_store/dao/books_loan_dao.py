from sqlalchemy import select, insert
from sqlalchemy.engine import Result

from book_store.common.filter import Filter
from book_store.db.page import Page
from book_store.dto.book_loan import BookOnLoan


class BooksLoanDao:
    def add_book_on_loan_with_transaction(self, book_loan: BookOnLoan, session):
        session.add(book_loan)
        session.flush()
        return book_loan.loan_book_id

    def add_book_on_loan(self, book_loan: BookOnLoan, connection):
        stmt = insert(BookOnLoan).values(book_loan)
        response = connection.execute(stmt)
        val = response.inserted_primary_key[0]
        return val

    def get_loan_books(self, conn):
        stmt = select(BookOnLoan)
        result = conn.execute(stmt)
        response = []
        for row in result:
            response.append(dict(row))
        return response

    def get_paginated_loan_books(self, page: Page, filters: Filter, session):
        stmt = select(BookOnLoan)
        stmt = filters.apply_filters(stmt, BookOnLoan, BookOnLoan.loan_book_id)
        page.calculate_pagination_totals(stmt, session)
        stmt = page.make_paged(stmt)

        result: Result = session.execute(stmt)
        page.elements = []
        for row in result:
            page.elements.append(dict(row))
        return page
