# Generated by Django 2.1.5 on 2020-02-18 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0018_auto_20200218_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag_age',
            field=models.IntegerField(choices=[(1, '< 1 miesiąc'), (2, '< 3 miesiące'), (3, '< 6 miesięcy'), (4, '< 1 rok'), (5, '< 1.5 roku'), (6, '< 2 lata'), (7, 'Ponad 2 lata')], default=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag_sex',
            field=models.CharField(choices=[('Boy', 'Chłopca'), ('Girl', 'Dziewczynki'), ('Unisex', 'Zarówno dla chłopca jaki i dziewczynki')], default='Unisex', max_length=6, verbose_name=''),
        ),
    ]
