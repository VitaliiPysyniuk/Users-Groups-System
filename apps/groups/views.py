from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from django.db.models import Count

from .models import GroupModel
from .serializers import GroupSerializer, GroupWithExtraFieldSerializer
from .services import parse_groups_query_params


class GroupListCreateView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing groups, with optional filtering.

    post:
    Create a new group instance.
    """
    queryset = GroupModel.objects.order_by('id')
    serializer_class = GroupSerializer

    def get_queryset(self):
        """Return new queryset based on query parameters if they were set."""
        query_params = dict(self.request.query_params.items())
        with_members_number = query_params.pop('with_members_number', None)

        if with_members_number or [param for param in query_params.keys() if param.startswith('members_number')]:
            self.queryset = GroupModel.objects.values('id', 'name', 'description')\
                .annotate(members_number=Count('users__id')).order_by('id')
            self.serializer_class = GroupWithExtraFieldSerializer

        if query_params:
            query_params = parse_groups_query_params(query_params)
            queryset = self.queryset.filter(**query_params)
            return queryset
        return super().get_queryset()


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



