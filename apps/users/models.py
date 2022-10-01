from django.db import models


class UsedModel(models.Model):
    class Meta:
        db_table = 'users'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
