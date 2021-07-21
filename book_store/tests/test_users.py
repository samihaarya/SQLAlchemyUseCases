import pytest
from book_store.dto.user import User


@pytest.fixture
def base_service():
    from book_store.service.user_service import UserService
    user_service: UserService = UserService()
    yield user_service


def test_add_user(base_service):
    # GIVEN
    user: User = User(
        name='Samiha',
        address='Rajpura',
        address_zip='140401',
        birthdate='06-05-1998',
        phone='9464322369',
        email='samiha@thomsonreuters.com'
    )
    # WHEN
    base_service.add_user_with_transaction(user)
