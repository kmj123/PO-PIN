# Generated by Django 5.2.1 on 2025-07-01 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanionTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='태그명')),
            ],
        ),
    ]
