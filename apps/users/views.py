from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from .models import UsedModel
from .serializers import UserCreateUpdateSerializer, UserListSerializer
from .services import parse_users_query_params


class UserListCreateView(ListCreateAPIView):
    """
    get:
    Return a list of all the existing users, with optional filtering.

    post:
    Create a new user instance.
    """
    serializer_class = UserCreateUpdateSerializer
    queryset = UsedModel.objects.prefetch_related('groups')

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserListSerializer
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Return new queryset based on query parameters if they were set."""
        query_params = self.request.query_params
        if query_params:
            query_params = parse_users_query_params(query_params)
            queryset = self.queryset.filter(**query_params)
            return queryset
        return super().get_queryset()


class UserUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    """
    patch:
    Partly update the user with the given id.

    delete:
    Delete the user with the given id.
    """
    queryset = UsedModel.objects.all()
    serializer_class = UserCreateUpdateSerializer
    lookup_field = 'id'
