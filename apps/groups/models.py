from django.db import models

from ..users.models import UsedModel


class GroupModel(models.Model):
    class Meta:
        db_table = 'groups'

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    users = models.ManyToManyField(UsedModel, related_name='groups')
