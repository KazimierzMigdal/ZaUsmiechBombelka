# Generated by Django 2.1.5 on 2020-03-27 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messanger_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parent_msg',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_messages', to='messanger_system.Message', verbose_name='Parent message'),
        ),
    ]