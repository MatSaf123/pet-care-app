# Generated by Django 3.2 on 2021-05-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210503_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=None, max_length=100, unique=True),
        ),
    ]
