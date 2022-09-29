from django.urls import path

from .views import GroupListCreateView, GroupUpdateDestroyView

urlpatterns = [
    path('', GroupListCreateView.as_view(), name='get_create_groups'),
    path('/<int:id>', GroupUpdateDestroyView.as_view(), name='update_delete_group')
]
