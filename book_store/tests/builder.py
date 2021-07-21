import datetime
import uuid

from book_store.dto.book import Book
from book_store.dto.book_loan import BookOnLoan
from book_store.dto.user import User


def build_book_dict(**kwargs) -> dict:
    book: dict = {
        'author': kwargs.get('author', 'Robert'),
        'title': kwargs.get('title', 'Rich dad poor dad'),
        'book_code': kwargs.get('book_code', uuid.uuid4())
    }
    return book


def build_basic_book(**kwargs) -> Book:
    book = Book(
        author=kwargs.get('author', 'Robert'),
        title=kwargs.get('title', 'whatever'),
        book_code=kwargs.get('book_code', uuid.uuid4())
    )
    return book


def build_user_dict(**kwargs) -> dict:
    book: dict = {
        'name': kwargs.get('user_name', 'Samiha'),
        'address': kwargs.get('address', 'Rajpura'),
        'address_zip': kwargs.get('address_zip', '140401'),
        'birthdate': kwargs.get('birthdate', '06-05-1998'),
        'phone': kwargs.get('phone', '9464322369'),
        'email': kwargs.get('email', 'samiha@thomsonreuters.com')
    }
    return book


def build_basic_user(**kwargs) -> User:
    user: User = User(
        name=kwargs.get('user_name', 'Samiha'),
        address=kwargs.get('address', 'Rajpura'),
        address_zip=kwargs.get('address_zip', '140401'),
        birthdate=kwargs.get('birthdate', '06-05-1998'),
        phone=kwargs.get('phone', '9464322369'),
        email=kwargs.get('email', 'samiha@thomsonreuters.com')
    )
    return user


def build_book_loan(**kwargs) -> BookOnLoan:
    loan_book: BookOnLoan = BookOnLoan(
        book_id=kwargs.get('book_id', '6259fea9-8824-4f0b-8644-dde570b4c786'),
        user_id=kwargs.get('user_id', 'cd842080-4c12-4158-a53b-9c471146783e'),
        loan_days=kwargs.get('loan_days', 6),
        loan_date=kwargs.get('loan_date', datetime.date.today())
    )
    return loan_book


def build_full_book_loan_dict(**kwargs) -> dict:
    book: dict = build_book_dict(**kwargs)
    book['book_id'] = uuid.uuid4()
    user: dict = build_user_dict(**kwargs)
    user['user_id'] = uuid.uuid4()
    loan_book: dict = {
        'book_id': book['book_id'],
        'user_id': user['user_id'],
        'loan_days': kwargs.get('loan_days', 6),
        'loan_date': kwargs.get('loan_date', datetime.date.today())
    }
    loan = {
        'user': user,
        'book': book,
        'book_on_loan': loan_book
    }
    return loan


def build_full_book_loan(**kwargs) -> dict:
    book: Book = build_basic_book(**kwargs)
    book.book_id = uuid.uuid4()
    user: User = build_basic_user(**kwargs)
    user.user_id = uuid.uuid4()
    loan_book: BookOnLoan = BookOnLoan(
        book_id=book.book_id,
        user_id=user.user_id,
        loan_days=kwargs.get('loan_days', 6),
        loan_date=kwargs.get('loan_date', datetime.date.today())
    )
    loan = {
        'user': user,
        'book': book,
        'book_on_loan': loan_book
    }
    return loan

