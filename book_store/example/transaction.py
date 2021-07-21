import functools

from book_store.db import db_engine

engine = db_engine.get_engine()


def transactional(open_session=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            open_transaction = kwargs.get('transaction')
            if open_transaction and open_transaction.in_transaction():
                return func(*args, **kwargs)
            else:
                if open_session:
                    with open_session.begin():  # start transaction
                        kwargs['transaction'] = open_session
                        return func(*args, **kwargs)
                else:
                    # start a new session and transaction - entry point for a transactional session
                    Session = db_engine.get_session()
                    with Session() as session:
                        with session.begin():  # start transaction
                            kwargs['transaction'] = session
                            return func(*args, **kwargs)
        return wrapper
    return decorator
