# Generated by Django 2.1 on 2018-05-16 06:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20180516_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='algorithm',
            field=models.CharField(default=None, max_length=300),
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='开始时间'),
        ),
    ]
