from rest_framework.serializers import ModelSerializer

from .models import UsedModel
from ..groups.serializers import GroupSerializer


class UserCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = UsedModel
        fields = ['id', 'email', 'username', 'is_admin', 'created_at', 'groups']
        extra_kwargs = {'created_at': {'read_only': True}, 'groups': {'required': False}}


class UserListSerializer(UserCreateUpdateSerializer):
    groups = GroupSerializer(many=True)
