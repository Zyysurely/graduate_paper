# Generated by Django 2.1 on 2018-05-16 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20180516_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='add_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='algorithm',
        ),
    ]
