from django.urls import path, include

urlpatterns = [
    path('/users', include('apps.users.urls')),
    path('/groups', include('apps.groups.urls'))
]
