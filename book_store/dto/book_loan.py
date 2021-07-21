from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

from book_store.db import db_engine

metadata = db_engine.get_metadata()
Base = declarative_base()


class BookOnLoan(Base):
    __tablename__ = 'books_out_on_loan'

    loan_book_id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    user_id = Column(Integer)
    loan_date = Column(Date)
    loan_days = Column(Integer)
