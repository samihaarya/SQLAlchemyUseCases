from typing import List

from sqlalchemy import select, and_, delete, insert
from sqlalchemy.sql import Select

from book_store.dto.user import User


class UserDao:
    def add_user_with_transaction(self, user: User, transaction):
        transaction.add(user)

    def add_user(self, user: User, connection):
        stmt = insert(User).values(user)
        response = connection.execute(stmt)
        val = response.inserted_primary_key[0]
        return val

    def get_user(self, user_name: str, phone: str, connection):
        stmt: Select = select(User).where(and_(
            User.name == user_name, User.phone == phone
        ))
        result = connection.execute(stmt)
        return result.scalars().one_or_none()

    def get_all_users(self, connection):
        query = select(User)
        result = connection.execute(query)
        response: List[User] = []
        for row in result:
            response.append(User(row))
        return response

    def delete_user(self,  user_name: str, phone: str, connection):
        query = delete(User).where(and_(
            User.user_name == user_name, User.phone == phone))
        # query = delete(User).where(User.user_name == user_name)
        connection.execute(query)

    def get_user_by_id(self, user_id, connection):
        stmt = select(User).where(User.user_id == user_id)
        result = connection.execute(stmt)
        response = None
        for row in result:
            response = dict(row)
        return response
