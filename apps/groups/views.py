from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from .models import GroupModel
from .serializers import GroupSerializer


class GroupListCreateView(ListCreateAPIView):
    queryset = GroupModel.objects.all().order_by('id')
    serializer_class = GroupSerializer


class GroupUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'id'



