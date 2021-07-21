from sqlalchemy import Column, String, Integer, delete, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from book_store.db import db_engine
from book_store.example.transaction import transactional
# log SQL statements
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()


def print_what_is_in_session(message, transaction: Session = None):
    values = [obj.value for obj in transaction.query(AClass).all()]
    print(message, values)


class AClass(Base):
    __tablename__ = 'a'

    id = Column(Integer, primary_key=True)
    value = Column(String(128))


# create all tables
# Base.metadata.create_all(engine)


@transactional()
def A(transaction: Session = None):
    transaction.add(AClass(value="a1"))
    print("calling function B from the scope of A")
    try:
        B(transaction=transaction)
    except Exception:
        pass
        # transaction.rollback()
    print_what_is_in_session("after B rolled-back: ", transaction)
    transaction.add(AClass(value="a2"))
    print_what_is_in_session("in the end: ", transaction)


@transactional()
def B(transaction: Session = None):
    transaction.add(AClass(value="b1"))
    C(transaction=transaction)
    transaction.add(AClass(value="b2"))


@transactional()
def C(transaction: Session = None):
    transaction.add(AClass(value="c"))
    print_what_is_in_session("before exception: ", transaction)
    # transaction.add(AClass(value="c"))
    raise ValueError(0)


def delete_table_entries():
    engine = db_engine.get_engine()
    Session = db_engine.get_session()
    with Session() as session:
        with session.begin():
            session.query(AClass).delete()
            session.commit()


if __name__ == "__main__":
    delete_table_entries()
    A()
