# Generated by Django 2.1.5 on 2020-04-02 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messanger_system', '0005_auto_20200401_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Product'),
        ),
    ]
