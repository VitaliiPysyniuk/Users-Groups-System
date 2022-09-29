import pytest
from datetime import datetime
import pytz

from apps.users.models import UsedModel
from apps.groups.models import GroupModel


@pytest.fixture()
def fill_database():
    group_1 = GroupModel.objects.create(name='Group 1', description='Group 1 description')
    group_2 = GroupModel.objects.create(name='Group 2', description='Group 2 description')
    group_3 = GroupModel.objects.create(name='Group 3', description='Group 3 description')
    group_4 = GroupModel.objects.create(name='Group 4', description='Group 4 description')
    group_5 = GroupModel.objects.create(name='Group 5', description='Group 5 description')

    user_1 = UsedModel.objects.create(email='user1@gmail.com', username='user1', is_admin=True)
    user_1.created_at = datetime(2022, 9, 21, 5, 17, 15, tzinfo=pytz.UTC)
    user_1.save()
    user_2 = UsedModel.objects.create(email='user2@gmail.com', username='user2')
    user_2.created_at = datetime(2022, 9, 25, 10, 50, 4, tzinfo=pytz.UTC)
    user_2.save()
    user_3 = UsedModel.objects.create(email='user3@ukr.net', username='user3', is_admin=True)
    user_3.created_at = datetime(2022, 9, 21, 6, 45, 40, tzinfo=pytz.UTC)
    user_3.save()
    user_4 = UsedModel.objects.create(email='user4@yahoo.com', username='user4')
    user_4.created_at = datetime(2022, 9, 29, 9, 31, 25, tzinfo=pytz.UTC)
    user_4.save()
    user_5 = UsedModel.objects.create(email='user5@ukr.net', username='user5', is_admin=True)
    user_5.created_at = datetime(2022, 9, 21, 11, 51, 0, tzinfo=pytz.UTC)
    user_5.save()

    user_1.groups.add(group_1, group_2, group_3, group_5)
    user_2.groups.add(group_1, group_3, group_5)
    user_3.groups.add(group_2, group_4, group_5)
    user_4.groups.add(group_3, group_4, group_5)
    user_5.groups.add(group_1, group_5)
