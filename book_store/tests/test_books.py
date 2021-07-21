import uuid

import pytest

from book_store.dto.book import Book
from book_store.tests import builder


@pytest.fixture
def base_service():
    from book_store.service.book_service import BookService
    book_service: BookService = BookService()
    yield book_service


def test_add_book(base_service):
    # GIVEN
    book: dict = builder.build_book_dict(author='Peter', title='whatever')
    # book: dict = builder.build_book_dict()

    # WHEN
    response = base_service.add_book(book)
    print(response)
