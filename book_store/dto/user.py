from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from book_store.db import db_engine

metadata = db_engine.get_metadata()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    address_zip = Column(String)
    birthdate = Column(String)
    phone = Column(String)
    email = Column(String)
