from django.urls import path

from .views import UserListCreateView, UserUpdateDestroyView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='get_create_users'),
    path('/<int:id>', UserUpdateDestroyView.as_view(), name='update_delete_user')
]
