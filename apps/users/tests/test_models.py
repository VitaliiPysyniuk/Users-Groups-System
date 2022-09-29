import pytest

from ..models import UsedModel

users_test_data = [
    {'email': 'user1@gmail.com', 'username': 'user1'},
    {'email': 'user2@gmail.com', 'username': 'user2', 'is_admin': True},
]


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.parametrize(
    'user_data,expected_is_admin', [
        (users_test_data[0], False),
        (users_test_data[1], True),
    ]
)
def test_user_create(user_data, expected_is_admin):
    new_user = UsedModel.objects.create(**user_data)

    assert new_user.email == user_data['email']
    assert new_user.username == user_data['username']
    assert new_user.is_admin == expected_is_admin
