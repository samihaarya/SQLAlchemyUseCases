from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from book_store.db import db_engine

metadata = db_engine.get_metadata()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    book_code = Column(Integer)

