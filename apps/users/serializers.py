from rest_framework.serializers import ModelSerializer

from .models import UsedModel
from ..groups.serializers import GroupSerializer


class UserSerializer(ModelSerializer):
    # groups = GroupSerializer(required=False, many=True)

    class Meta:
        model = UsedModel
        fields = ['id', 'email', 'username', 'is_admin', 'created_at', 'groups']
        extra_kwargs = {'created_at': {'read_only': True}}
