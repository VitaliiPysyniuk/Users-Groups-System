from rest_framework.serializers import ModelSerializer, IntegerField

from .models import GroupModel


class GroupSerializer(ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ['id', 'name', 'description']


class GroupWithExtraFieldSerializer(ModelSerializer):
    members_number = IntegerField()

    class Meta:
        model = GroupModel
        fields = ['id', 'name', 'description', 'members_number']
