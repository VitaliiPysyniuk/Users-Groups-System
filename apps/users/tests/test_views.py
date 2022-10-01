import pytest
from django.urls import reverse
from datetime import datetime
import pytz
import json

from .test_models import users_test_data
from ..models import UsedModel
from utils import url_reverse_with_query_params


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


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('fill_database')
@pytest.mark.parametrize('params,expected_ids', [
    ({'email__endswith': 'gmail.com'}, [1, 2]),
    ({'email__endswith': 'ukr.net'}, [3, 5]),
    ({'email__endswith': 'yahoo.com'}, [4]),
    ({'email__endswith': 'yahoo.net'}, []),
    ({'email__startswith': 'user'}, [1, 2, 3, 4, 5]),
    ({'username__startswith': 'user'}, [1, 2, 3, 4, 5]),
    ({'username__startswith': 'user1'}, [1]),
    ({'is_admin': 'True'}, [1, 3, 5]),
    ({'is_admin': 'False'}, [2, 4]),
    ({'created_at__date': datetime(2022, 9, 21, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [1, 3, 5]),
    ({'created_at__date': datetime(2022, 9, 25, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [2]),
    ({'created_at__date': datetime(2022, 9, 29, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [4]),
    ({'created_at__date__lt': datetime(2022, 9, 29, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [1, 2, 3, 5]),
    ({'created_at__date__lt': datetime(2022, 9, 25, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [1, 3, 5]),
    ({'created_at__date__gt': datetime(2022, 9, 28, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [4]),
    ({'created_at__date__gt': datetime(2022, 9, 23, tzinfo=pytz.UTC).strftime("%Y-%m-%d")}, [2, 4]),
    ({'groups__in': '1'}, [1, 2, 5]),
    ({'groups__in': '2'}, [1, 3]),
    ({'groups__in': '3'}, [1, 2, 4]),
    ({'groups__in': '4'}, [3, 4]),
    ({'groups__in': '5'}, [1, 2, 3, 4, 5]),
    ({'groups__in': '1,4'}, [1, 2, 4, 3, 5]),
    ({'groups__in': '2,4'}, [1, 3, 4]),
    ({'email__endswith': 'ukr.net', 'groups__in': '2,3'}, [3]),
    ({'email__endswith': 'yahoo.com', 'groups__in': '4'}, [4]),
])
def test_users_filtering(params, expected_ids, client):
    base_url = reverse('get_create_users')
    url = url_reverse_with_query_params(base_url, params)

    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == len(expected_ids)
    for user in data:
        assert user['id'] in expected_ids
