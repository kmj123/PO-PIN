# Generated by Django 5.2.1 on 2025-07-01 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adpage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='author',
        ),
    ]
