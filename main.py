# This is a sample Python script.

from book_store.dto.user import User


def base_method():
    from book_store.service.user_service import UserService
    user_service: UserService = UserService()
    return user_service


def add_user():
    user: User = User(
        name='whatever',
        address='Banglore',
        address_zip='',
        birthdate='',
        phone='78998796887',
        email='whatever@thomsonreuters.com'
    )
    user_service = base_method()
    res = user_service.create_user(user)
    return res


def get_user():
    user_service = base_method()
    user_service.get_user('samiha', '9464322369')



# def print_hi(name):
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_all_user():
    user_service = base_method()
    return user_service.get_all_users()


if __name__ == '__main__':
    response = add_user()
    # get_user()
    # print_hi('PyCharm')
    # response = get_all_user()
    print(response)
