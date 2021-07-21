from typing import List

from book_store.dao.user_dao import UserDao
from book_store.db import db_engine
from book_store.dto.user import User


class UserService:
    def __init__(self):
        self.user_dao = UserDao()
        self.engine = db_engine.get_engine()
        self.session = db_engine.get_session()

    def create_user(self, user: User):
        # check if user present in db else create user and return id
        with self.session() as session:
            with session.begin():
                user_found = self.user_dao.get_user(user.name, user.phone, session)
                if user_found:
                    raise Exception('user already exists')
                else:
                    self.user_dao.add_user_with_transaction(user, session)


    def get_user(self, name: str, phone: str):
        with self.engine.connect() as connection:
            response = self.user_dao.get_user(name, phone, connection)
            return response

    # def delete_user(self, name: str, phone: str):
    def get_all_users(self):
        with self.engine.connect() as connection:
            with connection.begin():
                users: List[User] = self.user_dao.get_all_users(connection)
                return users

    def delete_user(self, name: str, phone: str):
        with self.engine.connect() as connection:
            self.user_dao.delete_user(user_name=name, phone=phone, connection=connection)
            response = 'user deleted successfully'
            return response

