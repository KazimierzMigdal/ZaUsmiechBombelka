# Generated by Django 2.1.5 on 2020-03-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messanger_system', '0002_message_parent_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]