# Generated by Django 2.2.6 on 2019-10-29 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20191029_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo_1',
            field=models.ImageField(upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo_2',
            field=models.ImageField(upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo_3',
            field=models.ImageField(upload_to='product_pics'),
        ),
    ]
