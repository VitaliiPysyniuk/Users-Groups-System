import pytest
from django.urls import reverse
import json

from .test_models import groups_test_data
from ..models import GroupModel
from utils import url_reverse_with_query_params
#
#
# @pytest.fixture()
# def create_default_group():
#     GroupModel.objects.create(name='Default group', description='Default group description')
#
#
# @pytest.mark.django_db
# @pytest.mark.usefixtures('create_default_group')
# def test_get_all_groups_view(client):
#     url = reverse('get_create_groups')
#
#     response = client.get(url)
#     data = response.data
#
#     assert response.status_code == 200
#     assert isinstance(data, list)
#     assert len(data) == 1
#     assert data[0]['id'] == 1
#
#
# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'group_data,expected_id', [
#         (groups_test_data[0], 2),
#         (groups_test_data[1], 3),
#     ]
# )
# def test_create_new_group_view_with_correct_data(group_data, expected_id, client):
#     url = reverse('get_create_groups')
#
#     response = client.post(url, data=group_data)
#     data = response.data
#
#     assert response.status_code == 201
#     assert data['id'] == expected_id
#     assert data['name'] == group_data['name']
#     assert data['description'] == group_data['description']
#
#
# @pytest.mark.django_db
# @pytest.mark.usefixtures('create_default_group')
# def test_create_new_group_view_with_not_correct_data(client):
#     url = reverse('get_create_groups')
#     new_group_data = {'name': 'Default group', 'description': 'Default group description'}
#
#     response = client.post(url, data=new_group_data)
#
#     assert response.status_code == 400
#
#
# @pytest.mark.django_db
# def test_update_group_with_correct_data(client):
#     new_group = GroupModel.objects.create(name='Group 3', description='Group 3 description')
#     url = reverse('update_delete_group', kwargs={'id': new_group.id})
#
#     response = client.patch(url,
#                             data=json.dumps({'name': 'Group 4', 'description': 'Group 4 description'}),
#                             content_type='application/json')
#     data = response.data
#
#     assert response.status_code == 200
#     assert data['id'] == new_group.id
#     assert data['name'] == 'Group 4'
#     assert data['description'] == 'Group 4 description'
#
#
# @pytest.mark.django_db
# @pytest.mark.usefixtures('create_default_group')
# def test_update_group_with_not_correct_data(client):
#     new_group = GroupModel.objects.create(name='Group 3', description='Group 3 description')
#     url = reverse('update_delete_group', kwargs={'id': new_group.id})
#
#     response = client.patch(url, data=json.dumps({'name': 'Default group'}), content_type='application/json')
#
#     assert response.status_code == 400
#
#
# @pytest.mark.django_db(reset_sequences=True)
# @pytest.mark.usefixtures('create_default_group')
# def test_delete_user_with_correct_data(client):
#     url = reverse('update_delete_group', kwargs={'id': 1})
#
#     response = client.delete(url)
#
#     assert response.status_code == 204
#
#
# @pytest.mark.django_db(reset_sequences=True)
# def test_delete_group_with_not_correct_data(client):
#     url = reverse('update_delete_group', kwargs={'id': 1})
#
#     response = client.delete(url)
#
#     assert response.status_code == 404


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('fill_database')
def test_get_all_groups_with_members_number_in_query_params(client):
    base_url = reverse('get_create_groups')
    query_params = {
        'with_members_number': True
    }
    url = url_reverse_with_query_params(base_url, query_params)

    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 5
    assert 'members_number' in data[0]


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('fill_database')
@pytest.mark.parametrize('params,expected', [
    ({'members_number__lt': 1}, 0),
    ({'members_number__lt': 2}, 0),
    ({'members_number__lt': 3}, 2),
    ({'members_number__lt': 4}, 4),
    ({'members_number__lt': 5}, 4),
    ({'members_number__lt': 6}, 5),
    ({'members_number__gt': 1}, 5),
    ({'members_number__gt': 2}, 3),
    ({'members_number__gt': 3}, 1),
    ({'members_number__gt': 4}, 1),
    ({'members_number__gt': 6}, 0),
    ({'members_number': 1}, 0),
    ({'members_number': 2}, 2),
    ({'members_number': 3}, 2),
    ({'members_number': 4}, 0),
    ({'members_number': 5}, 1),
    ({'members_number__gt': 2, 'members_number__lt': 6}, 3),
    ({'members_number__gt': 3, 'members_number__lt': 5}, 0),
    ({'members_number__gt': 1, 'members_number__lt': 3}, 2),
])
def test_groups_filtering_by_members_number_in_query_params(params, expected, client):
    base_url = reverse('get_create_groups')
    query_params = {
        'with_members_number': True
    }
    query_params.update(params)
    url = url_reverse_with_query_params(base_url, query_params)

    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == expected


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('fill_database')
@pytest.mark.parametrize('params,expected', [
    ({'name': 'Group 1'}, 1),
    ({'name': 'Group1'}, 0),
    ({'name__startswith': 'Group'}, 5),
    ({'name__startswith': 'group'}, 0),
])
def test_groups_filtering_by_name_in_query_params(params, expected, client):
    base_url = reverse('get_create_groups')
    url = url_reverse_with_query_params(base_url, params)

    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == expected