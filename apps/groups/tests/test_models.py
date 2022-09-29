import pytest

from ..models import GroupModel

groups_test_data = [
    {'name': 'Group 1', 'description': 'Group 1 description'},
    {'name': 'Group 2', 'description': 'Group 2 description'}
]


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.parametrize('group_data', groups_test_data)
def test_group_create(group_data):
    new_group = GroupModel.objects.create(**group_data)

    assert new_group.name == group_data['name']
    assert new_group.description == group_data['description']
