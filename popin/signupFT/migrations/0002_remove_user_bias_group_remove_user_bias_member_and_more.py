# Generated by Django 5.2.1 on 2025-06-26 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0001_initial'),
        ('signupFT', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bias_group',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bias_member',
        ),
        migrations.AddField(
            model_name='user',
            name='bias_group',
            field=models.ManyToManyField(blank=True, null=True, related_name='fans_group', to='idols.group', verbose_name='최애 그룹'),
        ),
        migrations.AddField(
            model_name='user',
            name='bias_member',
            field=models.ManyToManyField(blank=True, null=True, related_name='fans_member', to='idols.member', verbose_name='최애 멤버'),
        ),
    ]
