# Generated by Django 2.1.5 on 2020-04-02 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0022_product_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_for',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]
