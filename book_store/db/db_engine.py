from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

engine = None
session = None


def get_engine():
    global engine
    db_url = 'postgresql://postgres:dockets@localhost:5432/book_store_db'
    engine = create_engine(db_url, echo=True, future=True)
    return engine


def get_session() -> sessionmaker:
    global session
    if not session:
        session = sessionmaker(engine, expire_on_commit=False, future=True)
    return session


def get_metadata():
    metadata = MetaData()
    return metadata
