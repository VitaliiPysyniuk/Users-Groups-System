# Generated by Django 4.1.1 on 2022-09-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmodel',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
