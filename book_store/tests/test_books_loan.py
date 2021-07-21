import datetime

import pytest

from book_store.dto.book_loan import BookOnLoan
from book_store.service.books_loan_service import BooksLoanService
from book_store.tests import builder


@pytest.fixture
def base_service():
    loan_book_service: BooksLoanService = BooksLoanService()
    yield loan_book_service


def test_add_loan(base_service):
    # GIVEN
    loan_book: BookOnLoan = BookOnLoan(
        book_id='6259fea9-8824-4f0b-8644-dde570b4c786',
        user_id='cd842080-4c12-4158-a53b-9c471146783e',
        loan_days=2,
        loan_date=datetime.date.today()
    )

    # WHEN
    response = base_service.add_loan(loan_book)
    print(response)


def test_add_book_loan_without_transaction(base_service):
    # GIVEN
    # loan_book: dict = builder.build_full_book_loan_dict(user_name='test3', phone='987321')
    loan_book: dict = builder.build_full_book_loan_dict(user_name='Simon', phone='987654321', title='fault in our stars')
    # loan_book: dict = builder.build_full_book_loan_dict(user_name='test', phone='987654321', title='whatever')

    # WHEN
    response = base_service.add_book_loan_without_transaction(loan_book)
    print(response)


def test_add_book_loan_with_transaction(base_service):
    # GIVEN
    # loan_book: dict = builder.build_full_book_loan(user_name='Sid', phone='987289', title='fault in our stars')
    # loan_book: dict = builder.build_full_book_loan(user_name='Robert', phone='9872859')
    loan_book: dict = builder.build_full_book_loan(user_name='test6', phone='9872', title='abc')

    # WHEN
    response = base_service.add_book_loan_with_transaction(loan_book)
    print(response)


def test_get_book_loan_details(base_service):
    # WHEN
    response = base_service.get_loan()
    # response = base_service.get_loan_with_transaction()
    print(response)


def test_get_book_loan_details_with_transaction(base_service):
    # WHEN
    # response = base_service.get_loan()
    response = base_service.get_loan_with_transaction()
    print(response)


def test_get_loan_with_filter_and_pagination(base_service):
    # GIVEN
    pt = {'page': 0, 'size': 2, 'loan_days': 6}
    # WHEN
    response = base_service.get_loan_with_filter_and_pagination(params=pt)
    print(response)
