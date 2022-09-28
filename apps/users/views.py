from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from .models import UsedModel
from .serializers import UserCreateUpdateSerializer, UserListSerializer


class UserListCreateView(ListCreateAPIView):
    queryset = UsedModel.objects.all().order_by('id')
    serializer_class = UserCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserListSerializer
        return super().get(request, *args, **kwargs)


class UserUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = UsedModel.objects.all()
    serializer_class = UserCreateUpdateSerializer
    lookup_field = 'id'



