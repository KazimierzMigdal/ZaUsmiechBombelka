# Generated by Django 2.1.5 on 2020-02-18 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0016_auto_20200202_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, verbose_name=''),
        ),
    ]
