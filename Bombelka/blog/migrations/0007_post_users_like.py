# Generated by Django 2.1 on 2020-01-26 22:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_auto_20191028_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
