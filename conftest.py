import pytest

from apps.users.models import UsedModel
from apps.groups.models import GroupModel


@pytest.fixture()
def fill_database():
    group_1 = GroupModel.objects.create(name='Group 1', description='Group 1 description')
    group_2 = GroupModel.objects.create(name='Group 2', description='Group 2 description')
    group_3 = GroupModel.objects.create(name='Group 3', description='Group 3 description')
    group_4 = GroupModel.objects.create(name='Group 4', description='Group 4 description')
    group_5 = GroupModel.objects.create(name='Group 5', description='Group 5 description')

    user_1 = UsedModel.objects.create(email='user1@gmail.com', username='user1')
    user_2 = UsedModel.objects.create(email='user2@gmail.com', username='user2')
    user_3 = UsedModel.objects.create(email='user3@gmail.com', username='user3')
    user_4 = UsedModel.objects.create(email='user4@gmail.com', username='user4')
    user_5 = UsedModel.objects.create(email='user5@gmail.com', username='user5')

    user_1.groups.add(group_1, group_2, group_3, group_5)
    user_2.groups.add(group_1, group_3, group_5)
    user_3.groups.add(group_2, group_4, group_5)
    user_4.groups.add(group_3, group_4, group_5)
    user_5.groups.add(group_1, group_5)
