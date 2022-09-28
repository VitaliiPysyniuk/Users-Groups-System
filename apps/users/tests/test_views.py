import pytest
from django.urls import reverse
import json

from ..models import UsedModel

users_test_data = [
    {'email': 'user1@gmail.com', 'username': 'user1'},
    {'email': 'user2@gmail.com', 'username': 'user2'},
]


@pytest.fixture()
def create_default_user():
    UsedModel.objects.create(email='default@gmail.com', username='default')


@pytest.mark.django_db
@pytest.mark.usefixtures('create_default_user')
def test_get_all_users_view(client):
    url = reverse('get_create_users')

    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_data,expected_id', [
        (users_test_data[0], 2),
        (users_test_data[1], 3),
    ]
)
def test_create_new_user_view_with_correct_data(user_data, expected_id, client):
    url = reverse('get_create_users')

    response = client.post(url, data=user_data)
    data = response.data

    assert response.status_code == 201
    assert data['id'] == expected_id
    assert data['email'] == user_data['email']
    assert data['username'] == user_data['username']


@pytest.mark.django_db
@pytest.mark.usefixtures('create_default_user')
def test_create_new_user_view_with_not_correct_data(client):
    url = reverse('get_create_users')
    new_user_data = {'email': 'default@gmail.com', 'username': 'default'}

    response = client.post(url, data=new_user_data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_update_user_with_correct_data(client):
    new_user = UsedModel.objects.create(email='user3@gmail.com', username='user3')
    url = reverse('update_delete_user', kwargs={'id': new_user.id})

    response = client.patch(url,
                            data=json.dumps({'is_admin': 'true', 'username': 'user33', 'email': 'user33@gmail.com'}),
                            content_type='application/json')
    data = response.data

    assert response.status_code == 200
    assert data['id'] == new_user.id
    assert data['email'] == 'user33@gmail.com'
    assert data['is_admin'] is True
    assert data['username'] == 'user33'


@pytest.mark.django_db
@pytest.mark.usefixtures('create_default_user')
def test_update_user_with_not_correct_data(client):
    new_user = UsedModel.objects.create(email='user3@gmail.com', username='user3')
    url = reverse('update_delete_user', kwargs={'id': new_user.id})

    response = client.patch(url, data=json.dumps({'email': 'default@gmail.com'}), content_type='application/json')

    assert response.status_code == 400


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('create_default_user')
def test_delete_user_with_correct_data(client):
    url = reverse('update_delete_user', kwargs={'id': 1})

    response = client.delete(url)

    assert response.status_code == 204


@pytest.mark.django_db(reset_sequences=True)
def test_delete_user_with_not_correct_data(client):
    url = reverse('update_delete_user', kwargs={'id': 1})

    response = client.delete(url)

    assert response.status_code == 404
