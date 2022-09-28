from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from .models import UsedModel
from .serializers import UserSerializer


class UserListCreateView(ListCreateAPIView):
    queryset = UsedModel.objects.all().order_by('id')
    serializer_class = UserSerializer


class UserUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = UsedModel.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'



