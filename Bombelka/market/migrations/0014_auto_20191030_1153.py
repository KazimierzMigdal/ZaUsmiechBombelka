# Generated by Django 2.2.6 on 2019-10-30 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0013_auto_20191030_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Dodaj opis produktu (będzie widoczna na stronie z detalami produktu): '),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo_1',
            field=models.ImageField(default='default_1.jpg', upload_to='product_pics', verbose_name='Dodaj zdjęcie widoczne na stronie marketu: '),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo_2',
            field=models.ImageField(default='default_1.jpg', upload_to='product_pics', verbose_name='Dodaj zdjęcie ubranka na tle(zdjęcie będzie widoczne na stronie z detalami produktu): '),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo_3',
            field=models.ImageField(default='default_1.jpg', upload_to='product_pics', verbose_name='Dodaj zdjęcie ubranka na dziecku(zdjęcie będzie widoczne na stronie z detalami produktu, zalecamy zamalować twarz dziecka): '),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.TextField(max_length=100, verbose_name='Dodaj nazwę produktu ( będzie widoczna na stronie marketu): '),
        ),
    ]
