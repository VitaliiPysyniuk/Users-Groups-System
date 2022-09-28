from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from .models import GroupModel
from .serializers import GroupSerializer


class GroupListCreateView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing groups, with optional filtering.

    post:
    Create a new group instance.
    """
    queryset = GroupModel.objects.all().order_by('id')
    serializer_class = GroupSerializer


class GroupUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    """
    patch:
    Partly update the group with the given id.

    delete:
    Delete the group with the given id.
    """
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'id'



